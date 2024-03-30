from typing import Any, Dict, List, Optional, Union

from asyncpg import Connection, Record
from fastapi import HTTPException, status
from pydantic import UUID4
from pypika import Query, Table, functions
from pypika.terms import Criterion

from app.db.queries.queries import queries
from app.models.user import DBUser
from app.repositories.base import BaseRepository, IRepository


class UsersRepository(BaseRepository, IRepository[DBUser]):
    """
    UsersRepository is a concrete implementation of the IRepository contract.
    """

    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)
        self.model_class = DBUser

    async def get_all(
        self,
        filters: Dict[str, Union[Any, List[Any]]] = None,
        offset: int = 1,
        limit: int = 10,
    ) -> Dict[str, Union[List[DBUser], int]]:

        db_table = Table(self.model_class.__tablename__)

        # Initialize the query
        query = Query.from_(db_table).select("*")

        # Add filter for non-deleted records
        query = query.where(db_table.is_active == True)

        # Apply additional filters based on input
        if filters:
            query = self._apply_filters_to_query(query, filters)
            count_query = self._apply_filters_to_query(
                count_query, filters
            )

        # Add offset and limit
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        # Count the number of records matching the filters
        count_query = (
            Query.from_(db_table)
            .select(functions.Count("*"))
            .where(db_table.is_active == True)
        )

        # Execute the query within a transaction
        async with self.connection.transaction():
            # Execute the query to fetch data
            user_rows = await self.connection.fetch(str(query))

            # Execute the count query to get total count
            total_count = await self.connection.fetchval(
                str(count_query)
            )

        result = []

        for sample_row in user_rows:
            respons = await self._get_sample_from_db_record(
                sample_row=sample_row,
            )
            result.append(
                UserInResponse(**respons.model_dump(exclude_none=True))
            )

        return {"data": result, "total_count": total_count}

    async def get(self, uuid: str) -> DBUser:

        async with self.connection.transaction():
            user_row = await queries.get_user_by_uuid(
                self.connection, uuid
            )

        if user_row is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user not found",
            )

        return await self._get_user_from_db_record(
            user_row=user_row,
        )

    async def get_in_db(self, uuid: str) -> DBUser:

        async with self.connection.transaction():
            user_row = await queries.get_user_by_uuid_in_db(
                self.connection, uuid
            )

        if user_row is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user not found",
            )

        return await self._get_user_from_db_record_in_db(
            user_row=user_row,
        )

    async def add(self, payload: UserInCreate) -> DBUser:

        async with self.connection.transaction():
            user_row = await queries.create_user(
                self.connection, **payload.model_dump(exclude_none=True)
            )

        return await self._get_user_from_db_record(
            user_row=user_row,
        )

    async def update(
        self, obj: User, email: Optional[str], password: Optional[str]
    ) -> DBUser:

        obj.email = email or obj.email
        obj.password = password or obj.password

        async with self.connection.transaction():

            user_row = await queries.update_user(
                conn=self.connection,
                uuid=str(obj.uuid),
                new_email=obj.email,
                new_password=obj.password,
            )

        return await self._get_user_from_db_record(user_row=user_row)

    async def delete(self, uuid: UUID4) -> None:
        """
        Soft delete an object from the repository by its id.

        :param session: SQLAlchemy Session object
        :param id: ID of the object
        """
        # obj = session.query(self.model_class).get(id)

        # if obj is not None:
        #     session.delete(obj)
        #     session.commit()

        async with self.connection.transaction():

            await queries.delete_user(self.connection, uuid)

    async def remove(self, uuid: UUID4) -> None:
        """
        Delete an object from the repository by its id.

        :param session: SQLAlchemy Session object
        :param id: ID of the object
        """
        # obj = session.query(self.model_class).get(id)

        # if obj is not None:
        #     obj.is_actived = True
        #     session.commit()

        async with self.connection.transaction():

            await queries.remove_user(self.connection, uuid)

    async def _get_user_from_db_record(
        self,
        *,
        user_row: Record,
    ) -> UserInResponse:
        return UserInResponse(
            uuid=user_row["uuid"],
        )

    async def _get_sample_from_db_record_in_db(
        self,
        *,
        user_row: Record,
    ) -> UserInDB:
        return UserInDB(
            uuid=user_row["uuid"],
            is_active=user_row["is_active"],
        )
