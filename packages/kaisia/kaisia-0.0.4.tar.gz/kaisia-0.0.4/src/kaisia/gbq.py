from google.cloud import bigquery
from typing import List
from google.oauth2 import service_account
from rich.console import Console
from rich.table import Table as Tbl

from .config import Config
from .exceptions import TooManyTables
from .cli import Colors
from .auth import SA


class Base:
    def __init__(self, id: str, credential_path: str = ""):
        self.config: Config = Config(id=id)
        self.credentials: service_account.Credentials = SA.credentials(
            path=credential_path
        )
        self.bq_client: bigquery.Client = self._client()

    def _client(self) -> bigquery.Client:
        return bigquery.Client(
            project=self.config.project,
            credentials=self.credentials,
            client_options={"scopes": self.config.BQ_CLIENT_SCOPE},
        )


class Table(Base):
    def __init__(self, id: str, credential_path: str = ""):
        super().__init__(id, credential_path)

    @property
    def schema(self):
        table_ref = self.bq_client.dataset(self.config.dataset).table(self.config.table)
        table = self.bq_client.get_table(table_ref)
        return table.schema


class SchemaCompareMixin:
    def difference(self):
        table1 = set(self.resources[0].schema)
        table2 = set(self.resources[1].schema)
        self.diff = table1.symmetric_difference(table2)


class SchemaReprMixin:
    def to_terminal(self):
        table = Tbl(title="Schema Diff")
        table.add_column("Field", justify="right", style="cyan", no_wrap=True)
        table.add_column("Type", style="magenta")
        table.add_column("Mode", justify="right", style="green")

        repr = [field.to_api_repr() for field in self.diff]
        for i in repr:
            table.add_row(f"{i['name']}", f"{i['type']}", f"{i['mode']}")
        console = Console()
        console.print(table)


class Delta(SchemaReprMixin, SchemaCompareMixin):
    def __init__(self, resources: List[Table]):
        self._resources = self._validate_resources(resources)
        self.difference()

    @property
    def resources(self):
        return self._resources

    def _validate_resources(self, resources: List):
        if len(resources) != 2:
            raise TooManyTables(len(resources))
        return resources


class MakeMigration(Base):
    def __init__(self, config: Config):
        super().__init__(config)
