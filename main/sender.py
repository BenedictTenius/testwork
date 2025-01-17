import aio_pika

#interface with send message
class SendMessage:
    connection = None
    channel = None
    routing_key = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust("amqp://guest:guest@#.0.0.1/")
        
        async with self.connection:
            self.routing_key = "message"

            self.channel = await self.connection.channel()

    async def send_message(ex: str,message: str ,self):
        if self.connection != None and self.channel != None:
            try:
                await self.channel.default_exchange.publish(
                    aio_pika.Message(body=message.encode()),
                    routing_key=self.routing_key
                )
                print(f'{message} sent')
            except:
                print(f'{message} message was not send')
    
    async def disconnect(self):
        if self.connection != None:
            await self.connection.close
    

