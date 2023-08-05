""" Attempt at making some standard Target Tests. """
import io
import json
# flake8: noqa
import os
from contextlib import redirect_stdout
from pathlib import Path

import pytest
import sqlalchemy
from singer_sdk.exceptions import RecordsWithoutSchemaException, MissingKeyPropertiesError
from singer_sdk.testing import sync_end_to_end
from sqlalchemy import create_engine
from sqlalchemy.exc import DataError

from target_mysql.target import TargetMySQL
from target_mysql.tests.samples.aapl.aapl import Fundamentals
from target_mysql.tests.samples.sample_tap_countries.countries_tap import (
    SampleTapCountries,
)

parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tests/"))
config_path = os.path.join(parent_directory, "config.json")

with open(config_path, "r") as f:
    config_data = json.load(f)


@pytest.fixture()
def mysql_config():
    return config_data


@pytest.fixture
def mysql_target(mysql_config) -> TargetMySQL:
    return TargetMySQL(config=mysql_config)


def singer_file_to_target(file_name, target) -> None:
    """Singer file to Target, emulates a tap run
    Equivalent to running cat file_path | target-name --config config.json.
    Note that this function loads all lines into memory, so it is
    not good very large files.
    Args:
        file_name: name to file in .tests/data_files to be sent into target
        target: Target to pass data from file_path into..
    """
    file_path = Path(__file__).parent / Path("./data_files") / Path(file_name)
    buf = io.StringIO()
    with redirect_stdout(buf):
        with open(file_path, "r") as f:
            for line in f:
                print(line.rstrip("\r\n"))  # File endings are here,
                # and print adds another line ending so we need to remove one.
    buf.seek(0)
    target.listen(buf)


def get_engine():
    connection_url = sqlalchemy.engine.url.URL.create(
        drivername="mysql",
        username=config_data["user"],
        password=config_data["password"],
        host=config_data["host"],
        port=config_data["port"],
        database=config_data["database"],
    )

    engine = create_engine(connection_url)

    return engine


def get_row_count(table_name):
    engine = get_engine()
    rowcount = engine.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    return rowcount


def get_table_cols(table_name):
    engine = get_engine()

    # q = f"""
    # SELECT COLUMN_NAME FROM sys.ALL_TAB_COLS
    # WHERE owner='SYSTEM'
    # AND TABLE_NAME='{table_name}'
    # """
    q = f"""
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA='mysql'
    AND TABLE_NAME='{table_name}'
    ORDER BY ORDINAL_POSITION;
    """
    columns = [col[0] for col in engine.execute(q).fetchall()]
    return columns


# TODO should set schemas for each tap individually so we don't collide
# Test name would work well
@pytest.mark.skip(
    reason="TODO: Something with identity, doesn't make sense. external API, skipping"
)
def test_countries_to_mysql(mysql_config):
    tap = SampleTapCountries(config={}, state=None)
    target = TargetMySQL(config=mysql_config)
    sync_end_to_end(tap, target)


# TODO
@pytest.mark.skip("SQLalchemy and object column types don't work well together")
def test_aapl_to_mysql(mysql_config):
    tap = Fundamentals(config={}, state=None)
    target = TargetMySQL(config=mysql_config)
    sync_end_to_end(tap, target)


# this test should throw an exception
def test_record_before_schema(mysql_target):
    with pytest.raises(RecordsWithoutSchemaException) as e_info:
        file_name = "record_before_schema.singer"
        singer_file_to_target(file_name, mysql_target)


# this test should throw an exception
def test_invalid_schema(mysql_target):
    with pytest.raises(Exception) as e_info:
        file_name = "invalid_schema.singer"
        singer_file_to_target(file_name, mysql_target)


# this test should throw an exception
def test_record_missing_key_property(mysql_target):
    with pytest.raises(Exception) as e_info:
        file_name = "record_missing_key_property.singer"
        singer_file_to_target(file_name, mysql_target)


# this test should throw an exception
def test_record_missing_required_property(mysql_target):
    with pytest.raises(Exception) as e_info:
        file_name = "record_missing_required_property.singer"
        singer_file_to_target(file_name, mysql_target)


# TODO test that data is correctly set
# see target-sqllit/tests/test_target_sqllite.py
@pytest.mark.skip(reason="Waiting for SDK to handle this")
def test_column_camel_case(mysql_target, mysql_config):
    file_name = "camelcase.singer"
    singer_file_to_target(file_name, mysql_target)

    table_name = "TEST_CAMELCASE"
    if mysql_config["lower_case_table_names"]:
        table_name = table_name.lower()

    assert get_row_count(table_name) == 2

    assert "CUSTOMER_ID_NUMBER" in get_table_cols(table_name)


# test that data is correctly set
# @pytest.mark.skip(reason="Waiting for SDK to handle this")
def test_special_chars_in_attributes(mysql_target):
    with pytest.raises(MissingKeyPropertiesError) as e_info:
        file_name = "special_chars_in_attributes.singer"
        singer_file_to_target(file_name, mysql_target)


# test that data is correctly set
def test_optional_attributes(mysql_target):
    file_name = "optional_attributes.singer"
    singer_file_to_target(file_name, mysql_target)


# TODO: Test that schema without properties (no columns) fails
def test_schema_no_properties(mysql_target):
    file_name = "schema_no_properties.singer"
    singer_file_to_target(file_name, mysql_target)


# test that data is correct
def test_schema_updates(mysql_target):
    allow_column_alter = False
    if "allow_column_alter" in config_data:
        allow_column_alter = config_data["allow_column_alter"]

    file_name = "schema_updates.singer"
    if allow_column_alter:
        singer_file_to_target(file_name, mysql_target)
    else:
        with pytest.raises(NotImplementedError) as e_info:
            singer_file_to_target(file_name, mysql_target)

# test that data is correct
def test_multiple_state_messages(mysql_target):
    file_name = "multiple_state_messages.singer"
    singer_file_to_target(file_name, mysql_target)


# test that data is correct
# @pytest.mark.skip(reason="TODO")
def test_relational_data(mysql_target):
    file_name = "user_location_data.singer"
    singer_file_to_target(file_name, mysql_target)

    file_name = "user_location_upsert_data.singer"
    singer_file_to_target(file_name, mysql_target)


# test that data is correct
def test_no_primary_keys(mysql_target):
    file_name = "no_primary_keys.singer"
    singer_file_to_target(file_name, mysql_target)

    file_name = "no_primary_keys_append.singer"
    singer_file_to_target(file_name, mysql_target)


# test that data is correct
def test_duplicate_records(mysql_target):
    file_name = "duplicate_records.singer"
    singer_file_to_target(file_name, mysql_target)


# test that data is correct
def test_update_records(mysql_target):
    file_name = "update_records.singer"
    singer_file_to_target(file_name, mysql_target)


# @pytest.mark.skip(reason="Arrays of arrays not supported")
def test_array_data(mysql_target):
    file_name = "array_data.singer"
    singer_file_to_target(file_name, mysql_target)


@pytest.mark.skip(reason="TODO")
def test_encoded_string_data(mysql_target):
    file_name = "encoded_strings.singer"
    singer_file_to_target(file_name, mysql_target)


@pytest.mark.skip(reason="Something about objects not supported")
def test_tap_appl(mysql_target):
    file_name = "tap_aapl.singer"
    singer_file_to_target(file_name, mysql_target)


# @pytest.mark.skip(reason="TODO")
def test_tap_countries(mysql_target):
    file_name = "tap_countries.singer"
    singer_file_to_target(file_name, mysql_target)


def test_missing_value(mysql_target):
    file_name = "missing_value.singer"
    singer_file_to_target(file_name, mysql_target)


# @pytest.mark.skip(reason="TODO")
def test_large_int(mysql_target):
    with pytest.raises(DataError) as e_info:
        file_name = "large_int.singer"
        singer_file_to_target(file_name, mysql_target)


def test_db_schema(mysql_target):
    file_name = "target_schema.singer"
    singer_file_to_target(file_name, mysql_target)


def test_illegal_colnames(mysql_target):
    with pytest.raises(MissingKeyPropertiesError) as e_info:
        file_name = "illegal_colnames.singer"
        singer_file_to_target(file_name, mysql_target)


def test_numerics(mysql_target):
    file_name = "numerics.singer"
    singer_file_to_target(file_name, mysql_target)
