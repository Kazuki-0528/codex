from fastapi import Header, HTTPException, status

WRITE_ROLES = {"admin", "fm_manager"}
READ_ROLES = WRITE_ROLES | {"engineer", "viewer"}


def require_read_role(x_role: str | None = Header(default=None)) -> str:
    if x_role not in READ_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Read permission denied",
        )
    return x_role


def require_write_role(x_role: str | None = Header(default=None)) -> str:
    if x_role not in WRITE_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Write permission denied",
        )
    return x_role
