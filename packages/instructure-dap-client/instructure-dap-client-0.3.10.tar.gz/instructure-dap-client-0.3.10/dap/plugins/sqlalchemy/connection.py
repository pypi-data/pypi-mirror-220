from typing import Dict

from sqlalchemy import URL, make_url
from sqlalchemy.exc import NoSuchModuleError
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from ...integration.base_connection import RawDatabaseConnectionWrapper
from ...integration.database_errors import DatabaseProtocolError


def _specify_database_driver(
    original_url: str, dialect_to_driver_mapping: Dict[str, str]
) -> URL:
    try:
        url = make_url(original_url)
        dialect = url.get_dialect().name
        driver = url.get_dialect().driver
        updated_driver = dialect_to_driver_mapping.get(dialect, None)
        if updated_driver is None:
            raise ValueError(f"SQLAlchemy dialect not supported: {dialect}")
        if driver != updated_driver:
            url = url.set(drivername=f"{dialect}+{updated_driver}")
        return url
    except NoSuchModuleError as exc:
        raise DatabaseProtocolError(
            f"unknown database protocol: {url.drivername}"
        ) from exc


class SqlAlchemyConnection(RawDatabaseConnectionWrapper[AsyncConnection]):
    def __init__(
        self, connection_string: str, dialect_to_driver_mapping: Dict[str, str]
    ) -> None:
        database_url = _specify_database_driver(
            connection_string, dialect_to_driver_mapping
        )
        engine = create_async_engine(database_url)
        super().__init__(engine.connect())

    async def commit_impl(self, raw_connection: AsyncConnection) -> None:
        await raw_connection.commit()
