import asyncpg


class BasePostgreSQL:
    def __init__(self):
        self.pool: asyncpg.Pool

    @classmethod
    async def connect(cls, *args, **kwargs):
        instance = cls()
        pool = await asyncpg.create_pool(*args, **kwargs)
        setattr(instance, "pool", pool)
        return instance

    async def close(self):
        await self.pool.close()
