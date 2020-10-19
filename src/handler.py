import json
import os
from aiohttp import request

import asyncio

loop = asyncio.get_event_loop()

async def get(url, headers):
    async with request('GET', url, headers=headers) as response:
        
        if response.status > 300:
            raise Exception(await response.text())
        
        return  await response.json()

async def main_async(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event,
        "request-response": await get(os.environ['API_URL'], {}) 
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def main(event, context):   
    return loop.run_until_complete(main_async(event, context))

