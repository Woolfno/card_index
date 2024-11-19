from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "employee" RENAME COLUMN "photo_filename" TO "photo_url";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "employee" RENAME COLUMN "photo_url" TO "photo_filename";"""
