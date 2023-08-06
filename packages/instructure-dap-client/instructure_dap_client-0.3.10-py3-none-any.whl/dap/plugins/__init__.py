from dap.integration.plugin import register_database_plugin_type

from .postgres.plugin import PostgresPlugin


def load() -> None:
    register_database_plugin_type("postgresql", PostgresPlugin)
