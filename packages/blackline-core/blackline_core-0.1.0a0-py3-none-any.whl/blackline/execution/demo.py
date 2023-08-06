import csv
from datetime import datetime
from pathlib import Path
from sqlite3 import Connection, connect
from typing import List

from blackline.constants import SAMPLE_DATABASE, SAMPLE_PROJECT_NAME
from blackline.models.project_config import ProjectConfig
from blackline.project.init import init_project
from yaml import dump

current_path = Path(__file__).parent.resolve()


def create_demo(path: Path, name: str = SAMPLE_PROJECT_NAME, overwrite: bool = False):
    project_config = init_project(path=path, name=name, overwrite=overwrite)
    root_path = Path(path, name)
    create_database(path=root_path)
    create_adapters(root_path=root_path, project_config=project_config)
    create_catalogue(project_config=project_config)


def create_database(path: Path):
    users = load_users()
    shipments = load_shipments()
    conn = connection(path=path)
    create_user_table(conn=conn, users=users)
    create_shipment_table(conn=conn, shipments=shipments)


def load_users() -> List[List[object]]:
    path = Path(current_path, "seeds", "users.csv")
    with open(str(path), "rt") as f:
        reader = csv.reader(f, dialect=csv.Dialect.delimiter)
        next(reader)
        users = [
            [d[0], d[1], d[2], d[3], bool(d[4]), datetime.strptime(d[5], "%Y:%m:%d")]
            for d in reader
        ]
    return users


def load_shipments() -> List[List[object]]:
    path = Path(current_path, "seeds", "shipments.csv")
    with open(path, "rt") as f:
        reader = csv.reader(f, dialect=csv.Dialect.delimiter)
        next(reader)
        orders = [
            [d[0], d[1], datetime.strptime(d[2], "%Y:%m:%d"), d[3], d[4], d[5], d[6]]
            for d in reader
        ]
    return orders


def connection(path: Path) -> Connection:
    path = Path(path, SAMPLE_DATABASE)
    con = connect(str(path))
    return con


def create_user_table(conn: Connection, users: List[List[object]]):
    with conn:
        cur = conn.execute(
            "CREATE TABLE IF NOT EXISTS user(id, name, email, ip, verified, created_at)"
        )
        cur.executemany("INSERT INTO user VALUES(?, ?, ?, ?, ?, ?)", users)


def create_shipment_table(conn: Connection, shipments: List[List[object]]):
    with conn:
        cur = conn.execute(
            "CREATE TABLE IF NOT EXISTS shipment(id, user_id, order_date, street, postcode, city,status)"  # noqa E501
        )
        cur.executemany("INSERT INTO shipment VALUES(?, ?, ?, ?, ?, ?, ?)", shipments)


def create_adapters(root_path: Path, project_config: ProjectConfig):
    database = Path(root_path, SAMPLE_DATABASE)
    sample_adapter = {
        "profiles": {
            "dev": {
                "type": "sqlite",
                "config": {
                    "connection": {
                        "database": str(database),
                        "uri": True,
                    }
                },
            }
        }
    }
    with open(Path(project_config.adapters_path, "sample_sqlite.yml"), "wt") as f:
        dump(sample_adapter, f)


def create_catalogue(project_config: ProjectConfig):
    sample_catalogue = {
        "user": {
            "datetime_column": "created_at",
            "columns": [
                {
                    "name": "name",
                    "deidentifier": {"type": "redact"},
                    "period": "P365D",
                    "description": "Name of user",
                },
                {
                    "name": "email",
                    "deidentifier": {"type": "replace", "value": "fake@email.com"},
                    "period": "P365D",
                },
                {
                    "name": "ip",
                    "deidentifier": {"type": "mask", "value": "#"},
                    "period": "280 00",
                },
            ],
        },
        "shipment": {
            "datetime_column": "order_date",
            "columns": [
                {
                    "name": "street",
                    "deidentifier": {"type": "redact"},
                    "period": "P185D",
                }
            ],
        },
    }
    sample_adapter_folder = Path(project_config.catalogue_path, "sample_sqlite")
    sample_adapter_folder.mkdir(parents=True)
    with open(
        Path(sample_adapter_folder, "sample_catalogue.yml"),
        "wt",
    ) as f:
        dump(sample_catalogue, f)
