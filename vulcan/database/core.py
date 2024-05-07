from typing import Optional, Tuple

from pandas import DataFrame
from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def initialize_default_database(db_file: str = "default.db") -> Engine:
    """
    Initializes a SQLite database engine with a default or specified database file.

    Parameters:
    - db_file: Name of the SQLite database file. Defaults to 'default.db'.

    Returns:
    - SQLAlchemy Engine instance for the SQLite database.
    """
    db_uri = f"sqlite:///output/{db_file}"
    engine = create_engine(db_uri, echo=True, future=True)
    return engine


def initialize_database(
    db_uri: str, connect_args: Optional[dict] = None, **engine_kwargs
) -> Engine:
    """
    Initializes a database engine.

    Parameters:
    - db_uri: Database URI for connection.
    - connect_args: Optional dictionary of connection arguments to be passed to the database.
    - engine_kwargs: Additional keyword arguments to be passed to create_engine.

    Returns:
    - SQLAlchemy Engine instance.
    """
    if connect_args is None:
        connect_args = {}
    engine = create_engine(
        db_uri, echo=True, connect_args=connect_args, **engine_kwargs
    )
    return engine


def execute_queries(
    engine: Engine, table_order: list[str], tables: dict
) -> Tuple[bool, Optional[str]]:
    """
    Executes a list of SQL queries using the given engine.

    Parameters:
    - engine: SQLAlchemy Engine instance.
    - queries: List of SQL query strings to be executed.

    Returns:
    - Tuple of success flag and error message (if any).
    """
    with engine.connect() as conn:
        transaction = conn.begin()
        try:
            for table_name in table_order:
                query = tables[table_name]["query"]
                conn.execute(text(query))
            transaction.commit()
            return True, None
        except SQLAlchemyError as e:
            transaction.rollback()
            return False, e


def reset_database(engine: Engine):
    """
    Resets the database by dropping all tables. Use with caution.
    """
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)


def populate_database(
    db_uri: str,
    table_order: list[str],
    tables: dict,
    dataframe: DataFrame,
    connect_args: Optional[dict] = None,
    **engine_kwargs,
):
    if db_uri:
        engine = initialize_database(db_uri, connect_args, **engine_kwargs)
    else:
        engine = initialize_default_database()
    execute_queries(engine, table_order, tables)
    engine.dispose()
