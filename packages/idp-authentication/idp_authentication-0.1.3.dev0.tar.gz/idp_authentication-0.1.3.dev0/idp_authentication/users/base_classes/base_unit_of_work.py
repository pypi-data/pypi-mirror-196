from idp_authentication import SessionPort
from idp_authentication.users.domain.ports.unit_of_work import UnitOfWorkPort


class BaseUnitOfWork(UnitOfWorkPort):
    def __init__(self, session: SessionPort):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # If anything is left in the session, rollback
        self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
