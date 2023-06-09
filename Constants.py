POSTGRES_DUPLICATE_OBJECT_ERROR_CODE = 'f405'
READONLY_ROLE_NAME = "readonly_role"
READWRITE_ROLE_NAME = "readwrite_role"
READWRITE_ACCESS_LEVEL = "READWRITE"
READONLY_ACCESS_LEVEL = "READONLY"
POSTGRES = "postgres"
DEFAULT_SCHEMA = "public"
SUPPORTED_ENGINES = [
    POSTGRES,
]
ENGINE_MAPPING = {POSTGRES: "postgresql+psycopg2"}
GRANT = "GRANT"
REVOKE = "REVOKE"
