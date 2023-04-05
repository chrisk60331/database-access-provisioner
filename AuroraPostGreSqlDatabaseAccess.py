import json
import logging

import boto3
from botocore.exceptions import ClientError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from Exceptions import UnsupportedEngineError
from PostGreSqlDatabaseAccess import PostGreSqlDatabaseAccess
from Constants import ENGINE_MAPPING, SUPPORTED_ENGINES


class AuroraPostGreSQLDatabaseAccess(PostGreSqlDatabaseAccess):

    creds = dict()

    def __init__(self, database_path: str, action: str):
        super().__init__(database_path, action)
        self.engine = create_engine(
            f"{ENGINE_MAPPING[self.creds['engine']]}://"
            f"{self.creds['username']}:{self.creds['password']}@"
            f"{database_path}"
        )
        self.database_name = str(
            self.engine.engine
        ).split('.')[0].split('@')[1]
        self.db_connection = Session(self.engine)

    def get_db_secret(self) -> dict:
        client = boto3.client("secretsmanager")
        try:
            response = client.get_secret_value(
                SecretId=self.secret_name,
            )
            secret_string = response.get("SecretString", {})
            creds = json.loads(secret_string)
            if creds.get("engine") not in SUPPORTED_ENGINES:
                raise UnsupportedEngineError
            return creds
        except ClientError:
            logging.error(
                msg=f"Unable to locate credentials for {self.secret_name}"
            )
            raise
