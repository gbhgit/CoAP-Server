import logging
import asyncio
from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    context = await Context.create_client_context()
    await asyncio.sleep(2)
    payload = b"{\"token\": \"hgipxndbexkuknxokfiw\", \"inputData\": \"imagemX1\", \"dataStatus\": \"create\"}"
    # payload = b"{\"token\": \"hgipxndbexkuknxokfiw\", \"inputData\": \"X2\", \"dataStatus\": \"update\", \"dataId\": \"1\"}"
    # payload = b"{\"token\": \"hgipxndbexkuknxokfiw\", \"inputData\": \"imagemX64\", \"dataStatus\": \"end\", \"dataId\": \"1\"}"
    request = Message(code=PUT, payload=payload, uri="coap://localhost/procdata")
    response = await context.request(request).response
    print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())