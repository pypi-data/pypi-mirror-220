from typing import Annotated, Any

import screeninfo
from pydantic import WrapValidator, ValidationError
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import ValidatorFunctionWrapHandler, ValidationInfo


def validate_monitor_id(
        value: Any, handler: ValidatorFunctionWrapHandler, _info: ValidationInfo
) -> Any:
    monitor_names = {monitor.name for monitor in screeninfo.get_monitors()}
    try:
        value = handler(value)

        if value not in monitor_names:
            raise ValueError(f"Invalid monitor ID", monitor_names)

    except ValidationError:
        raise PydanticCustomError(
            'invalid_monitor_id',
            f'Input is not a Monitor ID - {monitor_names}',
        )


MonitorId = Annotated[
    str,
    WrapValidator(validate_monitor_id)
]
