from uuid import UUID


def is_valid_uuid(val: str) -> bool:
    try:
        UUID(val)
        return True
    except Exception:
        return False
