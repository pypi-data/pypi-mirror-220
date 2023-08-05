"""MySQL target class."""

from __future__ import annotations

from singer_sdk import typing as th
from singer_sdk.target_base import SQLTarget

from target_mysql.sinks import (
    MySQLSink,
)


class TargetMySQL(SQLTarget):
    """Sample target for MySQL."""

    name = "target-mysql"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "sqlalchemy_url",
            th.StringType,
            secret=True,  # Flag config as protected.
            description="SQLAlchemy connection string",
        ),
        th.Property(
            "driver_name",
            th.StringType,
            default="mysql",
            description="SQLAlchemy driver name",
        ),
        th.Property(
            "username",
            th.StringType,
            secret=True,  # Flag config as protected.
            description="MySQL username",
        ),
        th.Property(
            "password",
            th.StringType,
            secret=True,  # Flag config as protected.
            description="MySQL password",
        ),
        th.Property(
            "host",
            th.StringType,
            description="MySQL host",
        ),
        th.Property(
            "port",
            th.StringType,
            description="MySQL port",
        ),
        th.Property(
            "database",
            th.StringType,
            description="MySQL database",
        ),
        th.Property(
            "lower_case_table_names",
            th.BooleanType,
            description="Lower case table names",
            default=True
        ),
        th.Property(
            "allow_column_alter",
            th.BooleanType,
            description="Allow column alter",
            default=False
        )
    ).to_dict()

    default_sink_class = MySQLSink


if __name__ == "__main__":
    TargetMySQL.cli()
