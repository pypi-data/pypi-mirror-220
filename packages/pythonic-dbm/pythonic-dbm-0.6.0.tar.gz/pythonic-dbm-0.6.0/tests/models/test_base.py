import datetime as datetime

import pytest

from pydbm import DbmModel
from pydbm.exceptions import EmptyModelError


class Model(DbmModel):
    bool: bool
    bytes: bytes
    date: datetime.date
    datetime: datetime.datetime
    float: float
    int: int
    none: None
    str: str


def test_base_slots():
    assert DbmModel.__slots__ == ("fields",)


def test_base_init():
    model = Model(
        bool=True,
        bytes=b"123",
        date=datetime.date(2020, 1, 1),
        datetime=datetime.datetime(2020, 1, 1, 2, 10, 40),
        float=1.0,
        int=1,
        none=None,
        str="str",
    )

    assert model.bool is True
    assert model.bytes == b"123"
    assert model.date == datetime.date(2020, 1, 1)
    assert model.datetime == datetime.datetime(2020, 1, 1, 2, 10, 40)
    assert model.float == 1.0
    assert model.int == 1
    assert model.none is None
    assert model.str == "str"

    assert model.id == "552eb2e66df095304137be35af85aaed"
    assert model.fields == {
        "bool": True,
        "bytes": b"123",
        "date": datetime.date(2020, 1, 1),
        "datetime": datetime.datetime(2020, 1, 1, 2, 10, 40),
        "float": 1.0,
        "int": 1,
        "none": None,
        "str": "str",
    }


def test_base_repr():
    model = Model(
        bool=True,
        bytes=b"123",
        date=datetime.date(2020, 1, 1),
        datetime=datetime.datetime(2020, 1, 1, 2, 10, 40),
        float=1.0,
        int=1,
        none=None,
        str="str",
    )

    assert repr(model) == "Model(bool=True, bytes=b'123', date=datetime.date(2020, 1, 1), datetime=datetime.datetime(2020, 1, 1, 2, 10, 40), float=1.0, int=1, none=None, str='str')"  # noqa: E501


def test_base_eq():
    model_1 = Model(
        bool=True,
        bytes=b"123",
        date=datetime.date(2020, 1, 1),
        datetime=datetime.datetime(2020, 1, 1, 2, 10, 40),
        float=1.0,
        int=1,
        none=None,
        str="str",
    )
    model_2 = Model(
        bool=True,
        bytes=b"123",
        date=datetime.date(2020, 1, 1),
        datetime=datetime.datetime(2020, 1, 1, 2, 10, 40),
        float=1.0,
        int=1,
        none=None,
        str="str",
    )

    assert model_1 == model_2

    model_3 = Model(
        bool=False,
        bytes=b"123",
        date=datetime.date(2020, 1, 1),
        datetime=datetime.datetime(2020, 1, 1, 2, 10, 40),
        float=1.0,
        int=1,
        none=None,
        str="str",
    )
    assert model_1 != model_3
    assert model_2 != model_3


def test_base_hash():
    class Account(DbmModel):
        ids: int
        name: str

    account_1 = Account(ids=1, name="John")
    account_2 = Account(ids=1, name="John")
    account_3 = Account(ids=2, name="Jane")

    assert account_1 == account_2

    assert account_1.id == "db6dede12578a5795f59d25ea68a8289"
    assert account_2.id == "db6dede12578a5795f59d25ea68a8289"
    assert account_3.id == "44fab4c4efaeb5f5a751496de67e0285"
    assert {account_1, account_2, account_3} == {account_1, account_3}


@pytest.mark.parametrize(
    "field_type, field_value",
    [
        (bool, True),
        (bytes, b"123"),
        (datetime.date, datetime.date(2020, 1, 1)),
        (datetime.datetime, datetime.datetime(2020, 1, 1, 2, 10, 40)),
        (float, 1.0),
        (int, 1),
        (None, None),
        (str, "str"),
    ],
)
def test_base_save(teardown_db, field_type, field_value):
    example_model: DbmModel = type("Example", (DbmModel,), {"__annotations__": {"field": field_type}})  # type: ignore

    model = example_model(field=field_value)
    assert model.save() is None

    model = example_model.objects.get(id=model.id)
    assert model.field == field_value


def test_base_create(teardown_db):
    class Example(DbmModel):
        str: str

    assert Example.objects.create(str="str") == Example(str="str")


def test_base_get(teardown_db):
    class Example(DbmModel):
        str: str

    model = Example.objects.create(str="str")

    assert Example.objects.get(id=model.id) == model


def test_base_get_with_unique_together(teardown_db):
    class Example(DbmModel):
        str: str
        int: int

    model = Example.objects.create(str="str", int=1)
    assert Example.objects.get(str="str", int=1) == model

    class Example(DbmModel):
        str: str
        int: int

        class Config:
            unique_together = ("str", "int")

    model = Example.objects.create(str="str", int=1)
    assert Example.objects.get(str="str", int=1) == model


def test_base_exception_get_with_unique_together(teardown_db):
    class Example(DbmModel):
        field1: str
        field2: int

    model = Example.objects.create(field1="str", field2=1)

    with pytest.raises(model.RiskofReturningMultipleObjects) as cm:
        assert Example.objects.get(field1="str") == model
    assert str(cm.value) == "To get single data from database you must pass all unique_together fields: ('field1', 'field2')"  # noqa: E501

    class Example(DbmModel):
        field1: str
        field2: int

        class Config:
            unique_together = ("field1", "field2")

    model = Example.objects.create(field1="str", field2=1)

    with pytest.raises(model.RiskofReturningMultipleObjects) as cm:
        assert Example.objects.get(field2=1) == model
    assert str(cm.value) == "To get single data from database you must pass all unique_together fields: ('field1', 'field2')"  # noqa: E501


def test_base_delete(teardown_db):
    class Example(DbmModel):
        str: str

    model = Example.objects.create(str="str")

    model.delete()
    with pytest.raises(model.DoesNotExists) as cm:
        Example.objects.get(id=model.id)
    assert str(cm.value) == "Example with id 341be97d9aff90c9978347f66f945b77 does not exists"


def test_base_update(teardown_db):
    class Example(DbmModel):
        str: str

    model = Example.objects.create(str="str")
    model.update(str="new_str")

    assert model.str == "new_str"
    assert Example.objects.get(id=model.id).str == "new_str"


def test_base_all_and_filter(teardown_db):
    class Example(DbmModel):
        field1: str
        field2: int

    model_1 = Example.objects.create(field1="str", field2=1)
    model_2 = Example.objects.create(field1="another str", field2=2)

    assert model_1.id == "0ece50da8a7fc1d3b2ca9d147db7af6a"
    assert model_2.id == "bafc344cc206678e99efd8bc660a28dc"
    assert model_1 == Example(field1="str", field2=1)
    assert model_2 == Example(field1="another str", field2=2)
    assert len(list(Example.objects.all())) == Example.objects.count()
    assert list(Example.objects.all()) == [Example(field1="another str", field2=2), Example(field1="str", field2=1)]
    assert list(Example.objects.filter()) == [Example(field1="another str", field2=2), Example(field1="str", field2=1)]
    assert list(Example.objects.filter(field2=1)) == [Example(field1="str", field2=1)]

    assert list(Example.objects.filter())[0].id == "bafc344cc206678e99efd8bc660a28dc"
    assert list(Example.objects.filter())[1].id == "0ece50da8a7fc1d3b2ca9d147db7af6a"

    assert list(Example.objects.all())[0].id == "bafc344cc206678e99efd8bc660a28dc"
    assert list(Example.objects.all())[1].id == "0ece50da8a7fc1d3b2ca9d147db7af6a"


def test_base_filter(teardown_db):
    class Example(DbmModel):
        str: str

    Example.objects.create(str="str")
    Example.objects.create(str="another str")

    assert list(Example.objects.filter(str="str")) == [Example(str="str")]


def test_base_empty_model():
    with pytest.raises(EmptyModelError) as cm:
        class EmptyModel(DbmModel):
            pass

    assert str(cm.value) == "Empty model is not allowed."


def test_base_only_id_field_model():
    with pytest.raises(EmptyModelError) as cm:
        class EmptyModel(DbmModel):
            id: str

    assert str(cm.value) == "Empty model is not allowed."


def test_base_update_obj_on_db_when_updating_the_field_on_the_instance(teardown_db):
    class TestModel(DbmModel):
        username: str

    model = TestModel(username="username")
    model.save()

    assert model.id == "14c4b06b824ec593239362517f538b29"

    model.username = "new_username"
    model.save()

    assert model.id == "14c4b06b824ec593239362517f538b29"

    assert TestModel.objects.get(id="14c4b06b824ec593239362517f538b29") == TestModel(username="new_username")


def test_base_count(teardown_db):
    class Model(DbmModel):
        username: str

    assert Model.objects.count() == 0

    Model(username="hakan").save()
    assert Model.objects.count() == 1

    Model(username="celik").save()
    assert Model.objects.count() == 2


def test_base_exists_true(teardown_db):
    class Model(DbmModel):
        username: str

        class Config:
            unique_together = ("username",)

    Model(username="hakan").save()
    assert Model.objects.exists(username="hakan") is True


def test_base_exists_false():
    class Model(DbmModel):
        username: str

    assert Model.objects.exists(username="hakan") is False


def test_base_exists_true_more_fields(teardown_db):
    class Model(DbmModel):
        username: str
        name: str
        surname: str

        class Config:
            unique_together = ("username",)

    Model(username="hakan", name="hakan", surname="celik").save()
    assert Model.objects.exists(name="hakan", surname="celik") is True


def test_base_exists_false_more_fields():
    class Model(DbmModel):
        username: str
        name: str
        surname: str

        class Config:
            unique_together = ("username",)

    assert Model.objects.exists(name="hakan", surname="celik") is False
