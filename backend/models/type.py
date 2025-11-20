from typing import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Text, Boolean, DateTime
from datetime import datetime

str_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_unique = Annotated[str, mapped_column(String, unique=True, index=True, nullable=False)]
str_idx = Annotated[str, mapped_column(String, index=True, nullable=False)]
text = Annotated[str, mapped_column(Text)]
bool_default_true = Annotated[bool, mapped_column(Boolean, default=True, server_default="true")]
bool_default_false = Annotated[bool, mapped_column(Boolean, default=False, server_default="false")]
timestamp = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default="now()", onupdate="now()")]