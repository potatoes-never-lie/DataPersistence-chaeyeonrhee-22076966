import pytest

from model.item import Item
from model.repository import CsvRepository, InMemoryRepository, JsonRepository, SqliteRepository


def make_in_memory(tmp_path):
    return InMemoryRepository()


def make_csv(tmp_path):
    return CsvRepository(str(tmp_path / "items.csv"))


def make_json(tmp_path):
    return JsonRepository(str(tmp_path / "items.json"))


def make_sqlite(tmp_path):
    return SqliteRepository(str(tmp_path / "items.db"))


FACTORIES = [make_in_memory, make_csv, make_json, make_sqlite]
FILE_FACTORIES = [make_csv, make_json, make_sqlite]


@pytest.mark.parametrize("make_repo", FACTORIES)
def test_crud_roundtrip(tmp_path, make_repo):
    repo = make_repo(tmp_path)

    added = repo.add(Item(id=None, name="apple", description="fruit"))
    assert added.id is not None
    assert repo.get(added.id) == Item(id=added.id, name="apple", description="fruit")
    assert repo.list_all() == [Item(id=added.id, name="apple", description="fruit")]

    repo.update(Item(id=added.id, name="apple", description="red fruit"))
    assert repo.get(added.id).description == "red fruit"

    repo.delete(added.id)
    assert repo.get(added.id) is None
    assert repo.list_all() == []


@pytest.mark.parametrize("make_repo", FACTORIES)
def test_update_unknown_id_raises(tmp_path, make_repo):
    repo = make_repo(tmp_path)
    with pytest.raises(KeyError):
        repo.update(Item(id=999, name="x", description="y"))


@pytest.mark.parametrize("make_repo", FACTORIES)
def test_delete_unknown_id_raises(tmp_path, make_repo):
    repo = make_repo(tmp_path)
    with pytest.raises(KeyError):
        repo.delete(999)


@pytest.mark.parametrize("make_repo", FILE_FACTORIES)
def test_persists_across_instances(tmp_path, make_repo):
    repo = make_repo(tmp_path)
    added = repo.add(Item(id=None, name="banana", description="fruit"))

    reloaded = make_repo(tmp_path)
    assert reloaded.get(added.id) == Item(id=added.id, name="banana", description="fruit")
