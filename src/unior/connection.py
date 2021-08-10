import bleak
import asyncio
import struct
from data_processing import BreathProcessor

floyd = BreathProcessor()

def handle_data(i: int, bytes: bytearray):
    print(1)
    data = struct.unpack('ff25f', bytes)
    values = list(data[2:])
    for v in values:
        print(floyd.process(v))

class Connection:
    def __init__(self, mac: str):
        self.mac = mac
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._bootstrap())

    async def _bootstrap(self):
        self.client = bleak.BleakClient(self.mac)
        await self.client.connect()

        data_service = self.client.services.get_service('e54eeef0-1980-11ea-836a-2e728ce88125')
        data_char = data_service.get_characteristic('e54eeef1-1980-11ea-836a-2e728ce88125')
        rx_char = data_service.get_characteristic('e54e0002-1980-11ea-836a-2e728ce88125')

        start_cmd = bytearray((0x53, 0x54, 0x41, 0x52, 0x54, 0x00))

        await self.client.write_gatt_char(rx_char, start_cmd)
        await self.client.start_notify(data_char, handle_data)
        print(2)

    async def __del__(self):
        await self.client.disconnect()
