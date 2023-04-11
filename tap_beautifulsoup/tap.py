"""BeautifulSoup tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_beautifulsoup import streams


class TapBeautifulSoup(Tap):
    """BeautifulSoup tap class."""

    name = "tap-beautifulsoup"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "source_name",
            th.StringType,
            required=True,
            default="sdk-docs",
        ),
        th.Property(
            "site_url",
            th.StringType,
            required=True,
            default="sdk.meltano.com/en/latest/",
        ),
        th.Property(
            "output_folder",
            th.StringType,
            required=True,
            default="output",
        ),
        th.Property(
            "parser",
            th.StringType,
            required=True,
            default="html.parser",
            allowed_values=["html.parser"],
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.BeautifulSoupStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.GenericBSStream(self),
        ]


if __name__ == "__main__":
    TapBeautifulSoup.cli()
