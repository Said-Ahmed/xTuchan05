from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, computed_field


class TuchanBase(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        json_encoders={
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if v else None,
        },
    )

