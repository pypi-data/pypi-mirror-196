import os
from pgdict import ConnectionConfig, Transaction, Store
from .request import Request

__version__ = "0.0.2"

store = Store(
    ConnectionConfig(
        database=os.getenv("__BOTFLEET__DATABASE"),
        table=os.getenv("__BOTFLEET__TABLE"),
        user=os.getenv("__BOTFLEET__USER"),
        password=os.getenv("__BOTFLEET__PASSWORD"),
        host=os.getenv("__BOTFLEET__HOST"),
        port=os.getenv("__BOTFLEET__PORT"),
    )
)
request = Request()
