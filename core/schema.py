from ninja import Schema


class ErrorMessage(Schema):
    detail: str
    status: int