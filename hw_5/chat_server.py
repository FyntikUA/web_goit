import asyncio
import logging
import websockets
import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from main_api import get_currency_rates
from aiofile import async_open
#from aiopath import AsyncPath
import json
import datetime

logging.basicConfig(level=logging.INFO)

class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            async for message in ws:
                await self.distrubute(ws, message)  # Передаємо команду message у distrubute
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def log_exchange_command(self, ws: WebSocketServerProtocol, command: str):
        async with async_open('exchange_log.txt', mode='a') as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await f.write(f"{timestamp}: {ws.name} use {command}\n")

    async def distrubute(self, ws: WebSocketServerProtocol, command: str):
        if command.startswith('exchange'):
            parts = command.split()
            if len(parts) == 2:
                try:
                    days = int(parts[1])
                    if days > 10:
                        await ws.send("Error: Maximum number of days allowed is 10.")
                        return
                    await self.send_to_clients(f"Waiting...")
                    rates = await get_currency_rates(days, ['EUR', 'USD', 'GBP'])  # Користуємося безпосередньо з функції, не через модуль
                    await ws.send(json.dumps(rates, indent=2))

                    # Логування команди exchange
                    await self.log_exchange_command(ws, command)
                except ValueError:
                    await ws.send("Error: Invalid number of days. Max 10")
            else:
                await ws.send("Error: Invalid command format. Must be like 'exchange 3'")
        else:
            await self.send_to_clients(f"{ws.name}: {command}")


async def main_api():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main_api())
