from abc import ABC, abstractmethod

from model.item import Item


class Repository(ABC):
    @abstractmethod
    def add(self, item: Item) -> Item:
        ...

    @abstractmethod
    def get(self, item_id: int) -> Item | None:
        ...

    @abstractmethod
    def list_all(self) -> list[Item]:
        ...

    @abstractmethod
    def update(self, item: Item) -> None:
        ...

    @abstractmethod
    def delete(self, item_id: int) -> None:
        ...


class InMemoryRepository(Repository):
    def __init__(self) -> None:
        self._items: dict[int, Item] = {}
        self._next_id = 1

    def add(self, item: Item) -> Item:
        item.id = self._next_id
        self._items[item.id] = item
        self._next_id += 1
        return item

    def get(self, item_id: int) -> Item | None:
        return self._items.get(item_id)

    def list_all(self) -> list[Item]:
        return list(self._items.values())

    def update(self, item: Item) -> None:
        if item.id not in self._items:
            raise KeyError(item.id)
        self._items[item.id] = item

    def delete(self, item_id: int) -> None:
        if item_id not in self._items:
            raise KeyError(item_id)
        del self._items[item_id]
