"""Stream type classes for tap-beautifulsoup."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_beautifulsoup.client import BeautifulSoupStream


class GenericBSStream(BeautifulSoupStream):
    """Define custom stream."""

    name = "page_content"
