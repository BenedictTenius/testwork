import aio_pika
import aiogram
import asyncio
from config import settings

bot = aiogram.Bot(settings.BOT_TOKEN)
db = [1321321321, 321321, 321321] #db with users tg ID


class GetMessage:
    connection = None
    channel = None
    queue_name = None
    
    
    async def connect(self) -> None:
        if self.connection == None:
            self.connection = await aio_pika.connect_robust("amqp://guest:guest@#.0.0.1/") # your local

        self.queue_name = "message"
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=150)


    async def process_message(message: aio_pika.abc.AbstractIncomingMessage,) -> None:
        async with message.process():
            for id in db:
                await bot.send_message(id, message.body)

    async def send_message(self):
        if self.connection != None:
            queue = await self.channel.declare_queue(self.queue_name, auto_delete=True)
            await queue.consume(self.process_message)
            try:
                await asyncio.Future()
            finally:
                await self.connection.close()


async def main() -> None:
    s = GetMessage()
    s.connect()
    s.send_message()


if __name__ == "__main__":
    asyncio.run(main())