from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import (NoUserError, TableIsBusyError,
                                UserAlreadyHaveTableError)
from app.api.services.base import BaseService
from app.api.services.printer import printer_service
from app.api.services.table import table_service
from app.crud.user import user_crud
from app.models.user import User
from app.schemas.user import UserInfoSchema


class UserService(BaseService):
    """Сервис для работы с пользователями."""

    async def check_user_exist(
        self,
        user_id: str,
        session: AsyncSession,
    ) -> User:
        user = await self.crud.get(
            user_id,
            session=session
        )
        if not user:
            raise NoUserError()

    async def check_table_user(
        self,
        user_id: int,
        table_id: int,
        session: AsyncSession
    ) -> None:
        table = await table_service.crud.get(table_id, session)
        if table and table.user_id and table.user_id != user_id:
            raise TableIsBusyError()
        table = await table_service.crud.get_table_by_user(user_id, session)
        if table and int(table.id) != table_id:
            raise UserAlreadyHaveTableError(table.id)
        table = await table_service.crud.get(int(table_id), session)

    async def get_user_info(
        self,
        user_id: int,
        session: AsyncSession
    ) -> UserInfoSchema:
        user = await user_crud.get(
            obj_id=user_id,
            session=session
        )
        if not user:
            raise NoUserError
        table = await table_service.crud.get_by_attribute(
            attr_name='user_id',
            attr_value=user_id,
            session=session
        )
        table_id = None if not table else table.id
        printer = await printer_service.crud.get_by_attribute(
            attr_name='user_id',
            attr_value=user_id,
            session=session
        )
        printer_id = None if not printer else printer.id
        return UserInfoSchema(
            username=user.name,
            user_id=user_id,
            table_id=table_id,
            printer_id=printer_id
        )


user_service = UserService(user_crud)
