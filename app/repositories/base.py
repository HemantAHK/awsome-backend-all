from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, TypeVar, Union

from asyncpg.connection import Connection

from app.db.session import BaseDBModel


class BaseRepository:
    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    @property
    def connection(self) -> Connection:
        return self._conn


T = TypeVar("T", bound=BaseDBModel)


class IRepository(Generic[T], ABC):
    """
    IRepository is an abstract base class that defines the contract for a repository.
    """

    @abstractmethod
    async def get_all(
        self, filters: Dict[str, Union[Any, List[Any]]] = None
    ) -> Dict[str, Union[List[T], int]]:
        """
        Get all objects from the repository that match the provided filters.

        :param session: SQLAlchemy Session object
        :param filters: Dictionary of filters to apply. If the value is a list, 'or' is
            used; otherwise 'and' is used.
        :return: Dictionary containing data and total count
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> T:
        """
        Get an object from the repository by its id.

        :param session: SQLAlchemy Session object
        :param id: ID of the object
        :return: The object with the given id
        """
        raise NotImplementedError

    @abstractmethod
    async def add(self, obj: T) -> T:
        """
        Add an object to the repository.

        :param session: SQLAlchemy Session object
        :param obj: Object to add
        :return: The added object
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, obj: T) -> T:
        """
        Update an object in the repository.

        :param session: SQLAlchemy Session object
        :param id: ID of the object to update
        :param obj: Updated object
        :return: The updated object
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> None:
        """
        Delete an object from the repository by its id.

        :param session: SQLAlchemy Session object
        :param id: ID of the object
        """
        raise NotImplementedError

    @abstractmethod
    async def remove(self, id: int) -> None:
        """
        Delete an object from the repository by its id.

        :param session: SQLAlchemy Session object
        :param id: ID of the object
        """
        raise NotImplementedError
