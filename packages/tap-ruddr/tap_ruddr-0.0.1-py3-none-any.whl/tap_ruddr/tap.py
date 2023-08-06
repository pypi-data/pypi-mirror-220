"""ruddr tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_ruddr import streams


class Tapruddr(Tap):
    """ruddr tap class."""

    name = "tap-ruddr"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://www.ruddr.io/api/workspace",
            description="The url for the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The logical run date. Used to filter results.",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.ruddrStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.ClientsStream(self),
            streams.ProjectsStream(self),
            streams.ProjectMembersStream(self),
            streams.ProjectRolesStream(self),
            streams.ProjectTasksStream(self),
            streams.ProjectExpensesStream(self),
            streams.ProjectOtherItemsStream(self),
            streams.TimeEntriesStream(self),
        ]


if __name__ == "__main__":
    Tapruddr.cli()
