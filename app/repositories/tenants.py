from typing import Any, Dict, Generic, List, TypeVar, Union

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.repository.base import IRepository

T = Generic[TypeVar("T")]


class TenantRepository(IRepository[T]):
    def __init__(self, model_class):
        self.model_class = model_class

    def get_all(
        self,
        session: Session,
        filters: Dict[str, Union[Any, List[Any]]] = None,
    ) -> List[T]:
        """
        Get all objects from the repository that match the provided filters.

        :param session: SQLAlchemy Session object
        :param filters: Dictionary of filters to apply. If the value is a list, 'or' is
            used; otherwise 'and' is used.
        :return: List of objects that match the filters
        """

        query = session.query(self.model_class)

        if filters:
            conditions = []
            for key, value in filters.items():
                if isinstance(value, list):
                    conditions.append(
                        or_(
                            *[
                                getattr(self.model_class, key) == v
                                for v in value
                            ]
                        )
                    )

                else:
                    conditions.append(
                        getattr(self.model_class, key) == value
                    )

            query = query.filter(and_(*conditions))

        return query.all()


# Create an instance of your repository
tenant_repo = TenantRepository(TenantRepository)
