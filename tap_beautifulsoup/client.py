"""Custom client handling, including BeautifulSoupStream base class."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup
from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.streams import Stream

from tap_beautifulsoup.download import download


class BeautifulSoupStream(Stream):
    """Stream class for BeautifulSoup streams."""

    @property
    def site_url(self) -> str:
        """Return the root URL for the stream."""
        return self.config["site_url"]

    @property
    def output_folder(self) -> Path:
        """Return the download folder for the stream."""
        return Path(self.config["output_folder"])

    @property
    def parser(self) -> str:
        """Return the parser for the stream."""
        return self.config["parser"]

    def download(self) -> None:
        """Download the HTML file for the stream."""
        download(self.site_url, self.output_folder)

    def parse_file(self, file: Path) -> str:
        """Parse the HTML file for the stream.

        Args:
            file: Path to the HTML file.

        Returns:
            The parsed content.
        """
        with open(file, encoding="utf-8") as f:
            data = f.read()

        soup = BeautifulSoup(data, features=self.parser)
        text = soup.find_all(attrs=self.top_attrs)
        text = text[0].get_text() if len(text) != 0 else ""
        return "\n".join([t for t in text.split("\n") if t])

    @property
    def top_attrs(self) -> dict:
        """Return the top-level attributes for the stream."""
        return {"role": "main"}

    def get_records(self, context: dict | None) -> Iterable[dict]:
        """Return a generator of record-type dictionary objects.

        The optional `context` argument is used to identify a specific slice of the
        stream if partitioning is required for the stream. Most implementations do not
        require partitioning and should ignore the `context` argument.

        Args:
            context: Stream partition or context dictionary.
        """
        self.download()

        docs = []
        for p in Path(self.output_folder).rglob("*.html"):
            if p.is_dir():
                continue

            text = self.parse_file(p)
            if not text:
                self.logger.warning(f"Could not find {self.top_attrs} in file {p}.")

            record = {
                "source": str(p),
                "page_content": text,
                "metadata": {"source": str(p)},
            }
            docs.append(record)
            yield record

        assert len(docs), f"No documents found in {self.output_folder}"

    schema = th.PropertiesList(
        th.Property("source", th.StringType),
        th.Property(
            "page_content",
            th.StringType,
            description="The page content.",
        ),
        th.Property(
            "metadata",
            th.ObjectType(),
        ),
    ).to_dict()
