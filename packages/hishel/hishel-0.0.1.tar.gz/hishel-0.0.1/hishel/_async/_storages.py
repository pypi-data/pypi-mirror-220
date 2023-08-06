import logging
import typing as tp
from pathlib import Path

from httpcore import Response

from hishel._serializers import BaseSerializer

from .._files import AsyncFileManager
from .._serializers import DictSerializer

logger = logging.getLogger('hishel.storages')

__all__ = (
    'AsyncFileStorage',
)

class AsyncBaseStorage:

    def __init__(self,
                 serializer: tp.Optional[BaseSerializer] = None) -> None:
        if serializer:  # pragma: no cover
            self._serializer = serializer
        else:
            self._serializer = DictSerializer()

    async def store(self, key: str, response: Response) -> None:
        raise NotImplementedError()

    async def retreive(self, key: str) -> tp.Optional[Response]:
        raise NotImplementedError()


class AsyncFileStorage(AsyncBaseStorage):

    def __init__(self,
                 serializer: tp.Optional[BaseSerializer] = None,
                 base_path: tp.Optional[Path] = None) -> None:
        super().__init__(serializer)
        if base_path:  # pragma: no cover
            self._base_path = base_path
        else:
            self._base_path = Path('./.cache/hishel')

        if not self._base_path.is_dir():
            self._base_path.mkdir(parents=True)

        self._file_manager = AsyncFileManager(is_binary=self._serializer.is_binary)

    async def store(self, key: str, response: Response) -> None:

        response_path = self._base_path / key
        await self._file_manager.write_to(
            str(response_path),
            self._serializer.dumps(response)
        )

    async def retreive(self, key: str) -> tp.Optional[Response]:

        response_path = self._base_path / key

        if response_path.exists():
            return self._serializer.loads(
                await self._file_manager.read_from(str(response_path))
            )
        return None

    async def delete(self, key: str) -> bool:
        response_path = self._base_path / key

        if response_path.exists():
            response_path.unlink()
            return True
        return False
