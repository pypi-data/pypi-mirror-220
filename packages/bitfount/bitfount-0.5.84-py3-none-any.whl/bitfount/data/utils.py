"""Utility functions concerning data."""
from dataclasses import dataclass
import datetime
import hashlib
import json
import logging
from typing import Any, List, Mapping, Optional, Union

import pandas as pd
from pandas.core.dtypes.common import pandas_dtype
import sqlalchemy
from sqlalchemy import create_engine, inspect

from bitfount.data.exceptions import (
    DatabaseMissingTableError,
    DatabaseSchemaNotFoundError,
    DatabaseUnsupportedQueryError,
    DatabaseValueError,
)
from bitfount.types import _DtypesValues

logger = logging.getLogger(__name__)


@dataclass
class DatabaseConnection:
    """Encapsulates database connection information for a `BaseSource`.

    If a `query` is provided or if `table_name` only has one table, the database will be
    queried for the data, after which the database connection will be closed and the
    resulting DataFrame will be used and stored in the `BaseSource`.

    :::danger

    If you are creating a multi-table Pod, ensure that the connection you provide only
    has access to the schemas and tables you wish to share and that this access has
    suitably restricted permissions i.e. `SELECT` only.

    `table_names` limits the Pod schema to only those tables you specify but it does
    not prevent a Modeller from accessing other tables in the schema or indeed other
    tables in other schemas by guessing their names.

    If only a single table is provided or a query is provided to combine multiple tables
    into one table, the Modeller will have no access to the database.

    :::

    Args:
        con: A database URI provided as a string or a SQLAlchemy Engine. This should
            include the database name, user, password, host, port, etc.
        db_schema: The database schema to use. If not provided, the default schema will
            be used.
        query: The SQL query to be executed as a string.
        table_names: Name(s) of SQL table(s) in database.

    Attributes:
        multi_table: Whether or not the database connection is for multiple tables.

    Raises:
        DatabaseMissingTableError: If `schema` (or the default schema if not provided)
            does not contain any tables or any of the specified tables can't be found in
            the schema.
        DatabaseSchemaNotFoundError: If `schema` is provided but can't be found in the
            database.
        DatabaseModificationError: If `query` is provided and contains an 'INTO' clause.
        ValueError: If both `query` and `table_names` are provided.
    """

    con: Union[str, sqlalchemy.engine.base.Engine]
    db_schema: Optional[str] = None
    query: Optional[str] = None
    table_names: Optional[List[str]] = None

    def __post_init__(self) -> None:
        """Initialises the `DatabaseConnection`."""
        self._validated: bool = False

    @property
    def validated(self) -> bool:
        """Whether or not the database connection has been validated."""
        return self._validated

    def validate(self) -> None:
        """Validates the database connection.

        This method is called by the corresponding `validate` method on the
        `DatabaseSource` which wraps the `DatabaseConnection`. The reason this does not
        happen on instantiation is that the `Pod` is responsible for validating the
        connection so that if there is an error, it is raised in the scope of the Pod's
        error handling hooks.

        :::note

        This method does not revalidate the connection if it has already been validated.

        :::
        """
        if self._validated:
            return

        # Create SQLAlchemy engine from database URI
        if isinstance(self.con, str):
            self.con: sqlalchemy.engine.base.Engine = create_engine(self.con)

        self.table_names = self.table_names if self.table_names else []

        inspector = inspect(self.con)

        # Ensure the provided schema exists, if not provided use the default schema
        if self.db_schema:
            schemas = inspector.get_schema_names()
            if self.db_schema not in schemas:
                raise DatabaseSchemaNotFoundError(
                    f"Schema '{self.db_schema}' not found in database."
                )
        self.db_schema: str = (
            self.db_schema if self.db_schema else inspector.default_schema_name
        )

        # Default is that we are dealing with a single table
        self.multi_table: bool = False

        # Raise an error if both query and table_names are provided
        if self.query and self.table_names:
            raise DatabaseValueError("Cannot specify both query and table_names.")

        # If table_names is provided, ensure that the schema contains all of the
        # specified tables
        elif self.table_names:
            db_table_names = inspector.get_table_names(schema=self.db_schema)
            for table in self.table_names:
                if table not in db_table_names:
                    raise DatabaseMissingTableError(
                        f"Table '{table}' not found in schema '{self.db_schema}'."
                    )

            if len(self.table_names) == 1:
                logger.info(
                    f"Single table {self.table_names[0]} provided. Reading data."
                )
            else:
                self.multi_table = True
                logger.info("Restricting schema to only specified tables.")
                logger.warning("Modeller needs to provide query in DataStructure.")

        # Nothing needs to be done here if a query was provided
        elif self.query:
            if "into" in self.query.lower():
                # 'SELECT * INTO' or 'INSERT INTO' would create a new table which is
                # not allowed
                raise DatabaseUnsupportedQueryError(
                    "Invalid query provided. "
                    "'SELECT * INTO' and 'INSERT INTO' are unsupported statements."
                )
            else:
                logger.info("Query provided. Reading data.")
        # If no query or table_names were provided, read all the tables from the schema
        else:
            logger.info(
                "No query or table names provided. "
                "Using all tables in the database for the schema. "
            )
            db_table_names = inspector.get_table_names(schema=self.db_schema)
            if db_table_names:
                self.table_names = db_table_names
            else:
                raise DatabaseMissingTableError(
                    f"No tables found in schema '{self.db_schema}'."
                )
            if len(self.table_names) > 1:
                self.multi_table = True
            logger.warning("Modeller needs to provide query in DataStructure.")

        self._validated = True


def _generate_dtypes_hash(dtypes: Mapping[str, Any]) -> str:
    """Generates a hash of a column name -> column type mapping.

    Uses column names and column dtypes to generate the hash. DataFrame contents
    is NOT used.

    SHA256 is used for hash generation.

    Args:
        dtypes: The mapping to hash.

    Returns:
        The hexdigest of the mapping hash.
    """
    dtypes = {k: str(v) for k, v in dtypes.items()}
    str_rep: str = json.dumps(dtypes, sort_keys=True)
    return _hash_str(str_rep)


def _hash_str(to_hash: str) -> str:
    """Generates a sha256 hash of a given string.

    Uses UTF-8 to encode the string before hashing.
    """
    return hashlib.sha256(to_hash.encode("utf-8")).hexdigest()


def _convert_python_dtypes_to_pandas_dtypes(
    dtype: _DtypesValues, col_name: str
) -> _DtypesValues:
    """Convert the python dtypes to pandas dtypes.

    Used for the schema generation for the `DatabaseSource`.
    """
    if dtype == str:
        return pd.StringDtype()
    # SQLAlchemy is able to infer the dtype of a column from the data in the column
    # and exposes this using the `python_type` attribute which includes types in the
    # python `datetime` standard library.
    elif dtype == datetime.date or dtype == datetime.datetime:
        return pd.StringDtype()
    else:
        try:
            return pandas_dtype(dtype)
        except Exception as e:
            raise ValueError(
                f"Data type {dtype} not recognised for column {col_name}"
            ) from e
