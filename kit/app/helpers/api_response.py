from typing import *


def send_success_response(
        data: Optional[List[Any] | Any] = None,
        message: str = "Data send successfully!",
        status: int = 200
) -> Dict[str, Any]:
    return {
        "status": status,
        "message": message,
        "data": data
    }


def send_error_response(
        data: Optional[List[Any]] = None,
        message: str = "Something went wrong!",
        status: int = 500
) -> Dict[str, Any]:
    return {
        "status": status,
        "message": message,
        "data": data
    }
