from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "employee" ADD "photo_filename" VARCHAR(255);
        CREATE UNIQUE INDEX "uid_user_usernam_9987ab" ON "user" ("username");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_user_usernam_9987ab";
        ALTER TABLE "employee" DROP COLUMN "photo_filename";"""
