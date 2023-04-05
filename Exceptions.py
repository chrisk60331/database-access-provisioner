class UnsupportedAction(Exception):
    """Action must be grant or revoke."""


class UnsupportedEngineError(Exception):
    """Credentials from get_db_secret are for non-postgres db engines."""
