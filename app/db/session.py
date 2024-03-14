from sqlalchemy.orm import as_declarative


@as_declarative()
class BaseDBModel:
    __name__: str

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(...)>"
