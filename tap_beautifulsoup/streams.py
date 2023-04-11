"""Stream type classes for tap-beautifulsoup."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_beautifulsoup.client import BeautifulSoupStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class GenericBSStream(BeautifulSoupStream):
    """Define custom stream."""

    name = "users"
    primary_keys = ["id"]
