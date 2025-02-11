import asyncio

from app.application import application_startup
from app.config.config import config
from app.infrastructure.utils.func_util import auto_register_injectables

injectables = auto_register_injectables(config.injection)

print(injectables)


async def test_application_startup():

    await application_startup()


asyncio.run(test_application_startup())
