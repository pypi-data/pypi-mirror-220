from sqlalchemy.orm import Mapped, mapped_column
from MOCKED_PACKAGE import NoneType
from MOCKED_PACKAGE import SimpleEnum
from MOCKED_PACKAGE import datetime
from MOCKED_PACKAGE import str
from lassen.db.base_class import Base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.sqltypes import Enum
from sqlalchemy.sql.sqltypes import String

from datetime import datetime
from enum import Enum
from lassen.stubs.base import BaseStub
from lassen.stubs.field import Field
from lassen.stubs.generators import SchemaGenerator, StoreGenerator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import timezone


class UserStub(Base):

    first_name: Mapped[str]

    last_name: Mapped[str | None]

    password: Mapped[str]

    enum_value: Mapped[SimpleEnum] = mapped_column(Enum(SimpleEnum))

    creation_date: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)

    forward_reference_value: Mapped['timezone'] = mapped_column('timezone')
