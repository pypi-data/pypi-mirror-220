# Read Gulf ID card data

Python package that interfaces with the Gulf ID and EID card reader service. It uses websocket to connect to the service installed on the host machine where a USB smart card reader is connected.

## Usage

- Install the card reader service on a windows machine
- Ensure the services are running
- Get the IP of the machine

```python
import aiohttp
from gulf_id_scanner import Client, ServiceError

session = aiohttp.ClientSession()
client = Client(host="192.168.3.45", web_session=session)
# validate connection
try:
    await client.connect()
except ServiceError as err:
    return False

# read card data
try:
  card_data = client.async_read_card():
    # code to process returned card data
except ServiceError as err:
    return
# detect when card is inserted and read card data
try:
  async for card_data in client.async_detect_card():
    # code to process returned card data
except ServiceError as err:
    return
await session.close()
```

## Card Data

The [`CardData`](https://github.com/Gallagher-ME/gulf_id_scanner/blob/8a0d692c85b86c3486e73cb5dd0fcbf9da6315a9/gulf_id_scanner/models.py#L653) class provides the main card data fields that are commonly required when reading the ID. For more specific fields you can find all the data fields retrived from `CardData.card_data`.
