from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from llm_replicate.vendored_replicate.client import Client
    from llm_replicate.vendored_replicate.collection import Collection

try:
    from pydantic import v1 as pydantic
except ImportError:
    import pydantic


class BaseModel(pydantic.BaseModel):
    """
    A base class for representing a single object on the server.
    """

    id: str

    _client: "Client" = pydantic.PrivateAttr()
    _collection: "Collection" = pydantic.PrivateAttr()

    def reload(self) -> None:
        """
        Load this object from the server again.
        """
        new_model = self._collection.get(self.id)
        for k, v in new_model.dict().items():
            setattr(self, k, v)
