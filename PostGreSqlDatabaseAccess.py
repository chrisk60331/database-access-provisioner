import re

from sqlalchemy.engine import Result

from Exceptions import UnsupportedAction
from Constants import READONLY_ROLE_NAME, DEFAULT_SCHEMA, READWRITE_ROLE_NAME, GRANT, REVOKE
from DatabaseAccess import DatabaseAccess

SUPPORTED_ACTIONS = [GRANT, REVOKE]


class PostGreSqlDatabaseAccess(DatabaseAccess):

    database_name = None

    def __init__(self, database_path: str, action: str):
        if action not in SUPPORTED_ACTIONS:
            raise UnsupportedAction()
        self.database_path = database_path
        self.action = action
        self.secret_name = re.sub(r"/\w*$", "", database_path)

    def grant(self, user_name: str) -> Result:
        """Grant database access."""
        command = f"GRANT {READONLY_ROLE_NAME} TO {user_name};"
        result = self.execute_sql(command)
        return result

    def revoke(self, user_name: str) -> Result:
        """Revoke database access."""
        command = f"REVOKE {READONLY_ROLE_NAME} FROM {user_name}"
        result = self.execute_sql(command)
        return result

    def create_user(self, user_name: str):
        command = f"CREATE USER {user_name};"
        result = self.execute_sql(command)
        return result

    def create_readonly_role(self) -> Result:
        command = (
            f"CREATE ROLE {READONLY_ROLE_NAME};"
            f"GRANT CONNECT ON DATABASE {self.database_name} "
            f"TO {READONLY_ROLE_NAME};"
            f"GRANT USAGE ON SCHEMA {DEFAULT_SCHEMA} TO {READONLY_ROLE_NAME};"
            f"GRANT SELECT ON ALL TABLES IN SCHEMA {DEFAULT_SCHEMA} "
            f"TO {READONLY_ROLE_NAME};"
        )
        result = self.execute_sql(command)
        return result

    def create_readwrite_role(self) -> Result:
        command = (
            f"CREATE ROLE {READWRITE_ROLE_NAME};"
            f"GRANT CONNECT ON DATABASE {self.database_name} "
            f"TO {READWRITE_ROLE_NAME};"
            f"GRANT USAGE ON SCHEMA {DEFAULT_SCHEMA} TO {READWRITE_ROLE_NAME};"
            "GRANT SELECT,INSERT,DELETE,UPDATE ON ALL TABLES IN SCHEMA "
            f"{DEFAULT_SCHEMA} TO {READWRITE_ROLE_NAME};"
        )
        result = self.execute_sql(command)
        return result
