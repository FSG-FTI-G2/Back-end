from typing import Any, Union


class MemoryStateProvider:
    def __init__(self) -> None:
        self.state: dict = {}

    def get(self, key: str) -> Union[Any, None]:
        return self.state.get(key, None)

    def set(self, key: str, value: Any) -> None:
        self.state[key] = value

    def delete(self, key: str) -> None:
        if key in self.state:
            del self.state[key]

    def gets(self, keys: list[str]) -> list[Union[Any, None]]:
        return [self.get(key) for key in keys]

    def sets(self, data: dict[str, Any]) -> None:
        self.state.update(data)

    def deletes(self, keys: list[str]) -> None:
        for key in keys:
            self.delete(key)

    def clear(self) -> None:
        self.state.clear()
