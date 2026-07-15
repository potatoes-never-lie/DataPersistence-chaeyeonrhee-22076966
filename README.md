# DataPersistence

MVC 구조의 Item CRUD 앱에 데이터 영속성 모듈을 추가한 프로젝트입니다.
같은 `Repository` 인터페이스를 CSV / JSON / SQLite / 인메모리 네 가지 방식으로
구현해서, 저장 방식을 바꿔도 controller/view 코드는 전혀 건드릴 필요가 없습니다.

## 구조

```
model/
  item.py        # Item 데이터클래스 (id, name, description)
  repository.py  # Repository 추상클래스 + 4가지 구현체 (CRUD)
controller/
  item_controller.py  # 콘솔 메뉴 흐름 제어
view/
  console_view.py     # input()/print() 기반 콘솔 입출력
main.py           # 실행 진입점 (사용할 저장소를 여기서 선택)
tests/
  test_repositories.py  # 4가지 구현체 공통 CRUD 계약 테스트 (pytest)
```

## 저장 방식 선택

`model/repository.py`에 `Repository` 추상클래스를 구현한 4개 클래스가 있습니다.
전부 `add / get / list_all / update / delete`를 동일하게 제공하므로 서로 바꿔
끼울 수 있습니다.

| 클래스 | 저장 위치 (기본값) | 방식 |
|---|---|---|
| `InMemoryRepository` | 없음 (프로세스 종료 시 소멸) | dict에만 저장, 영속성 없음 |
| `CsvRepository` | `data/items.csv` | csv 모듈, 매 변경 시 파일 전체를 다시 씀 |
| `JsonRepository` | `data/items.json` | json 모듈, 매 변경 시 파일 전체를 다시 씀 |
| `SqliteRepository` | `data/items.db` | sqlite3 모듈, 쿼리로 직접 CRUD (autoincrement id) |

`data/` 폴더는 각 클래스 생성 시 없으면 자동으로 만들어집니다.

### 사용할 저장소 바꾸기

`main.py`에서 import와 생성자만 바꾸면 됩니다.

```python
from model.repository import CsvRepository  # 이 줄만 바꾸면 저장 방식이 바뀜
# from model.repository import JsonRepository
# from model.repository import SqliteRepository
# from model.repository import InMemoryRepository

ItemController(CsvRepository(), console_view).run()
```

저장 파일 경로를 바꾸고 싶으면 생성자에 경로를 넘기면 됩니다.

```python
CsvRepository("data/backup.csv")
JsonRepository("data/backup.json")
SqliteRepository("data/backup.db")
```

## 실행

```bash
python main.py
```

콘솔 메뉴에서 항목 조회/추가/수정/삭제를 선택하면 됩니다. 종료 후 다시 실행해도
`data/` 아래 파일(또는 DB)에 저장된 데이터가 그대로 남아 있습니다
(`InMemoryRepository`만 예외).

## Repository를 코드에서 직접 쓰기

```python
from model.item import Item
from model.repository import SqliteRepository

repo = SqliteRepository()  # data/items.db 사용

item = repo.add(Item(id=None, name="apple", description="fruit"))
repo.get(item.id)
repo.list_all()
repo.update(Item(id=item.id, name="apple", description="red fruit"))
repo.delete(item.id)
```

`update`/`delete`에 존재하지 않는 id를 넘기면 `KeyError`가 발생합니다.

## 테스트

```bash
pytest
```

4가지 구현체가 동일한 CRUD 계약(추가→조회→목록→수정→삭제, 존재하지 않는 id
처리, 파일 기반 구현체의 재시작 후 데이터 유지)을 만족하는지 검증합니다.
