from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "position" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS "employee" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "first_name" VARCHAR(120) NOT NULL,
    "middle_name" VARCHAR(120) NOT NULL,
    "last_name" VARCHAR(120) NOT NULL,
    "start_date" DATE NOT NULL,
    "salary" DECIMAL(8,2) NOT NULL,
    "photo_url" VARCHAR(255),
    "boss_id" UUID REFERENCES "employee" ("id") ON DELETE SET NULL,
    "position_id" INT NOT NULL REFERENCES "position" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password_hash" VARCHAR(256)
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
    DROP TABLE IF EXISTS employee;
    DROP TABLE IF EXISTS position;
    DROP TABLE IF EXISTS "user";
    """
