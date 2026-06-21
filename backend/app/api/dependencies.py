from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.hr_user import HRUser
from app.repositories.user_repo import UserRepository
from app.utils.security import verify_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> HRUser:
    email = verify_token(token)
    if email is None:
        raise HTTPException(status_code=401, detail="INVALID_TOKEN")

    user = await UserRepository(db).get_by_email(email)
    if user is None:
        raise HTTPException(status_code=401, detail="USER_NOT_FOUND")
    return user
