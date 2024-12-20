"""


created at 2024/12/20
"""

from typing import Annotated

from pydantic import Field, TypeAdapter

PositiveInt = Annotated[int, Field(gt=0)]

ta_obj = TypeAdapter(PositiveInt)

print(ta_obj.validate_python(-1))
