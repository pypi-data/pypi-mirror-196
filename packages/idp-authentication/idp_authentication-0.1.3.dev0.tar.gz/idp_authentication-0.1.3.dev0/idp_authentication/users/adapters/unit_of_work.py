from idp_authentication import SessionPort
from idp_authentication.users.adapters.repositories.user_repository import (
    UserRepository,
)
from idp_authentication.users.adapters.repositories.user_role_repository import (
    UserRoleRepository,
)
from idp_authentication.users.base_classes.base_unit_of_work import BaseUnitOfWork
from idp_authentication.users.domain.ports.unit_of_work import UsersUnitOfWorkPort


class UsersUnitOfWork(BaseUnitOfWork, UsersUnitOfWorkPort):
    def __init__(self, session: SessionPort):
        super().__init__(session)
        self.user_repository = UserRepository(session)
        self.user_role_repository = UserRoleRepository(session)
