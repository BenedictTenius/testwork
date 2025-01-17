from aio_pika import connect_robust
from aio_pika.patterns import RPC
import asyncio
from main.config import settings
from fastapi import Request, Response, FastAPI, status

app = FastAPI()

def get_status():
    return status


async def register_rpc(loop):
    connection = await connect_robust(settings.BASE_SITE, loop=loop)
    channel = await connection.channel()
    rpc = await RPC.create(channel)


    await rpc.register('remote_method', get_status, auto_delete=True)
    return rpc

async def _rpc(request: Request, call_next):
    response = Response("hello", status_code=500)
    try:
        loop = asyncio.get_event_loop()

        connection = await connect_robust(settings.BASE_SITE, loop=loop)

        channel = await connection.channel()
        request.state.rpc = await RPC.create(channel)
        response = await call_next(request)
    finally:
        await request.state.rpc.close()
    return response


app.middleware('http')(_rpc)



@app.get('/rpc')
async def rpc_check(rpc = register_rpc):
    return await rpc.proxy.get_status()