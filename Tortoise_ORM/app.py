from tortoise import Tortoise, run_async

async def init():
    await Tortoise.init(
        db_url='postgres://user:password@localhost:5432/university_db',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()

