from enum import Enum
from typing import Any, Dict, List

import pytest
import sqlalchemy

from lassen.stubs.base import BaseStub
from lassen.stubs.definition import UniqueDefinition
from lassen.stubs.field import Field
from lassen.stubs.generators.common import ExtractedStubImports
from lassen.stubs.generators.store import StoreGenerator


class SimpleEnum(Enum):
    TEST = "TEST"


@pytest.mark.parametrize(
    "typehint, expected_str, expected_class",
    [
        (int, "Integer()", sqlalchemy.Integer()),
        (float, "Float()", sqlalchemy.Float()),
        (SimpleEnum, "Enum(SimpleEnum)", sqlalchemy.Enum(SimpleEnum)),
        (list[str], "ARRAY(String())", sqlalchemy.ARRAY(sqlalchemy.String())),
        (List[str], "ARRAY(String())", sqlalchemy.ARRAY(sqlalchemy.String())),
        (str | None, "String()", sqlalchemy.String()),
        (Any, "JSON()", sqlalchemy.JSON()),
        (dict[str, str], "JSON()", sqlalchemy.JSON()),
        (Dict[str, str], "JSON()", sqlalchemy.JSON()),
    ],
)
def test_format_column_for_sqlalchemy(typehint, expected_str, expected_class):
    store_generator = StoreGenerator("test")
    (
        formatted_column,
        class_value,
        dependencies,
    ) = store_generator.format_column_for_sqlalchemy(typehint)

    assert formatted_column == expected_str
    # Since the classes are fully instantiated separately and therefore fail exact equality, compare the string values
    assert str(class_value) == str(expected_class)
    assert len(dependencies) > 0


def test_generate_relationship() -> None:
    class MyParentModel(BaseStub):
        pass

    class MyChildModel(BaseStub):
        user_parent_id: int = Field(foreign_key="my_parent_model.id")
        user_parent: "MyParentModel" = Field(
            foreign_key=user_parent_id, is_relationship=True
        )

    store_generator = StoreGenerator("test")
    definition = store_generator(MyChildModel, ExtractedStubImports([], []))

    assert (
        "user_parent_id: Mapped[int] = mapped_column(foreign_key='my_parent_model.id')"
        in definition
    )
    assert (
        "user_parent: Mapped['MyParentModel'] = relationship('MyParentModel', foreign_keys=['user_parent_id'])"
        in definition
    )


def test_get_model_table_args() -> None:
    class MyModel(BaseStub):
        unique_text: str = Field()

        my_unique_constraint = UniqueDefinition(
            name="my_unique_constraint", fields=[unique_text]
        )

    store_generator = StoreGenerator("test")
    definitions, _ = store_generator.get_model_table_args(MyModel)
    assert definitions == ["UniqueConstraint(unique_text, name='my_unique_constraint')"]
