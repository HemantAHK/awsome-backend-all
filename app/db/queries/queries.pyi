"""Typings for queries generated by aiosql"""

from asyncpg import Connection, Record
from typing import Dict, Optional, Sequence


class SamplesQueriesMixin:
    async def get_sample_by_uuid(
        self, conn: Connection, *, uuid: str
    ) -> Record: ...

    async def get_sample_by_uuid_in_db(
        self, conn: Connection, *, uuid: str
    ) -> Record: ...

    async def create_sample(
        self, conn: Connection, name: str, task: str
    ) -> Record: ...

    async def update_sample(
        self,
        conn: Connection,
        uuid: str,
        new_name: str,
        new_task: str,
    ) -> Record: ...

    async def delete_sample(
        self,
        conn: Connection,
        uuid: str,
    ) -> None: ...

    async def remove_sample(
        self,
        conn: Connection,
        uuid: str,
    ) -> None: ...


class Queries(
    SamplesQueriesMixin
):
    ...


queries: Queries