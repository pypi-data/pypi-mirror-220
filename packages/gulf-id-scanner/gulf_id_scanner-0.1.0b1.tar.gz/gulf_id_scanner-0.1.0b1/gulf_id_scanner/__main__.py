import asyncio

import aiohttp

from gulf_id_scanner import Client, ServiceError


async def main() -> None:
    session = aiohttp.ClientSession()
    client = Client(host="192.168.3.45", web_session=session)
    try:
        await client.connect()
        card_data = await client.async_read_card()
        print(card_data)
    except ServiceError as err:
        print(str(err))
    await session.close()


if __name__ == "__main__":
    asyncio.run(main())
