from typing import Any, Dict, List, Union, Optional
from fastapi import HTTPException, status

from asyncpg import Connection, Record
from pypika import Query, Table, functions
from pypika.terms import Criterion

from app.db.queries.queries import queries
from app.models.sample import DBSample
from app.repositories.base import IRepository, BaseRepository
from app.schemas.sample import SampleInCreate, SampleInResponse, SampleInUpdate, Sample, SampleInDB

from pydantic import UUID4


class SamplesRepository(BaseRepository, IRepository[DBSample]):
    """
    SamplesRepository is a concrete implementation of the IRepository contract.
    """

    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)
        self.model_class = DBSample

    async def get_all(
        self,
        filters: Dict[str, Union[Any, List[Any]]] = None,
        offset: int = 1,
        limit: int = 10,
    ) -> Dict[str, Union[List[DBSample], int]]:

        db_table = Table(self.model_class.__tablename__)

        # Initialize the query
        query = Query.from_(db_table).select("*")

        # Add filter for non-deleted records
        query = query.where(db_table.is_active == True)

        # Apply additional filters based on input
        if filters:
            query = self._apply_filters_to_query(query, filters)
            count_query = self._apply_filters_to_query(count_query, filters)

        # Add offset and limit
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        # Count the number of records matching the filters
        count_query = Query.from_(db_table).select(
            functions.Count('*')).where(db_table.is_active == True)

        # Execute the query within a transaction
        async with self.connection.transaction():
            # Execute the query to fetch data
            samples_rows = await self.connection.fetch(str(query))

            # Execute the count query to get total count
            total_count = await self.connection.fetchval(str(count_query))

        result = []

        for sample_row in samples_rows:
            respons = await self._get_sample_from_db_record(
                sample_row=sample_row,
            )
            result.append(SampleInResponse(
                **respons.model_dump(exclude_none=True)))

        return {"data": result, "total_count": total_count}

    async def get(self, uuid: str) -> DBSample:

        async with self.connection.transaction():
            sample_row = await queries.get_sample_by_uuid(self.connection, uuid)

        if sample_row is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="sample not found",
            )

        return await self._get_sample_from_db_record(
            sample_row=sample_row,

        )

    async def get_in_db(self, uuid: str) -> DBSample:

        async with self.connection.transaction():
            sample_row = await queries.get_sample_by_uuid_in_db(self.connection, uuid)

        if sample_row is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="sample not found",
            )

        return await self._get_sample_from_db_record_in_db(
            sample_row=sample_row,

        )

    async def add(self, payload: SampleInCreate) -> DBSample:

        async with self.connection.transaction():
            sample_row = await queries.create_sample(
                self.connection, **payload.model_dump(exclude_none=True)
            )

        return await self._get_sample_from_db_record(
            sample_row=sample_row,

        )

    async def update(self, obj: Sample, name: Optional[str], task: Optional[str]) -> DBSample:

        obj.name = name or obj.name
        obj.task = task or obj.task

        async with self.connection.transaction():

            sample_row = await queries.update_sample(
                conn=self.connection,
                uuid=str(obj.uuid),
                new_name=obj.name,
                new_task=obj.task,
            )

        return await self._get_sample_from_db_record(
            sample_row=sample_row
        )

    async def delete(self, uuid: UUID4) -> None:
        """
        Delete an object from the repository by its id.

        :param session: SQLAlchemy Session object
        :param id: ID of the object
        """
        # obj = session.query(self.model_class).get(id)

        # if obj is not None:
        #     session.delete(obj)
        #     session.commit()

        async with self.connection.transaction():

            await queries.delete_sample(self.connection, uuid)

    async def remove(self, uuid: UUID4) -> None:
        """
        Soft delete an object from the repository by its id.

        :param session: SQLAlchemy Session object
        :param id: ID of the object
        """
        # obj = session.query(self.model_class).get(id)

        # if obj is not None:
        #     obj.is_actived = True
        #     session.commit()

        async with self.connection.transaction():

            await queries.remove_sample(self.connection, uuid)

    async def _get_sample_from_db_record(
        self,
        *,
        sample_row: Record,
    ) -> SampleInResponse:
        return SampleInResponse(
            uuid=sample_row["uuid"],
            name=sample_row["name"],
            task=sample_row["task"],
        )

    async def _get_sample_from_db_record_in_db(
        self,
        *,
        sample_row: Record,
    ) -> SampleInDB:
        return SampleInDB(
            uuid=sample_row["uuid"],
            name=sample_row["name"],
            task=sample_row["task"],
            is_active=sample_row["is_active"],
        )

    def _apply_filters_to_query(self, query: Query, filters: Dict[str, Union[Any, List[Any]]]) -> Query:
        """
        Apply additional filters to the query based on input filters.

        :param query: The query to which filters will be applied.
        :param filters: Dictionary of filters to apply.
        :return: The query with applied filters.
        """
        if filters:
            conditions = []
            for key, value in filters.items():
                if isinstance(value, list):
                    conditions.append(
                        Criterion.in_(
                            getattr(self.model_class, key), value
                        )
                    )
                else:
                    conditions.append(
                        getattr(self.model_class, key) == value
                    )

            query = query.where(*conditions)

        return query
