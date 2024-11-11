from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "position" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS "employee" (
    "uuid" UUID NOT NULL  PRIMARY KEY,
    "first_name" VARCHAR(120) NOT NULL,
    "middle_name" VARCHAR(120) NOT NULL,
    "last_name" VARCHAR(120) NOT NULL,
    "start_date" DATE NOT NULL,
    "salary" DECIMAL(8,2) NOT NULL,
    "boss_id" UUID REFERENCES "employee" ("uuid") ON DELETE SET NULL,
    "position_id" INT NOT NULL REFERENCES "position" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
