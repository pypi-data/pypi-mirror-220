import asyncio

import aiohttp

from gulf_id_scanner.client import Client

from .execptions import ServiceError


async def main() -> None:
    session = aiohttp.ClientSession()
    client = Client(host="192.168.3.45", web_session=session)
    try:
        await client.connect()
        async for card_data in client.async_detect_card():
            print(card_data)
    except ServiceError as err:
        print(err)
    await session.close()


if __name__ == "__main__":
    asyncio.run(main())
