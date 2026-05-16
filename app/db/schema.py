from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def ensure_runtime_schema(engine: Engine) -> None:
    inspector = inspect(engine)
    if "members" not in inspector.get_table_names():
        return

    member_columns = {
        column["name"]
        for column in inspector.get_columns("members")
    }

    statements = []
    dialect = engine.dialect.name

    if "email" not in member_columns:
        statements.append("ALTER TABLE members ADD COLUMN email VARCHAR(100) NULL")

    if "created_at" not in member_columns:
        if dialect == "mysql":
            statements.append(
                "ALTER TABLE members ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"
            )
        else:
            statements.append("ALTER TABLE members ADD COLUMN created_at DATETIME")

    if not statements:
        return

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
