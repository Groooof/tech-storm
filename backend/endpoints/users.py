from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from logic.messages import get_user_messages
from logic.users import get_user_info_by_id
from schemas.auth import AccessTokenPayload
from schemas.messages import MessageData
from schemas.users import UserInfoSchema
from shared.dependencies import get_session, get_unexpired_token

router = APIRouter(tags=['users'])


@router.get('/me', summary='Данные текущего пользователя')
async def get_current_user_data(
    session: AsyncSession = Depends(get_session), token: AccessTokenPayload = Depends(get_unexpired_token)
) -> UserInfoSchema | None:
    return await get_user_info_by_id(session, token.user_id)


@router.get('/me/messages', summary='Сообщения текущего пользователя')
async def get_current_user_messages(
    session: AsyncSession = Depends(get_session), token: AccessTokenPayload = Depends(get_unexpired_token)
) -> list[MessageData]:
    return await get_user_messages(session, token.user_id)
