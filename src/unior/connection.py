import bleak
import asyncio
import struct
from .data_processing import BreathProcessor
import threading


class Connection:
    def __init__(self, mac: str):
        self._connected = True
        self._value = 0
        self.breathe_processor = BreathProcessor()
        self.mac = mac
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._bootstrap())
        self.thread = threading.Thread(name=f'Device {self.mac} thread', target=lambda :self.loop.run_forever())
        self.thread.start()
        # now loop runs in another thread

    def _handle_data(self, i: int, bytes: bytearray):
        # print(1)
        data = struct.unpack('ff25f', bytes)
        values = list(data[2:])
        for v in values:
            self._value = self.breathe_processor.process(v)

    @property
    def value(self):
        # this is probably thread-safe.... I hope
        return self._value

    async def _bootstrap(self):
        proc = await asyncio.subprocess.create_subprocess_shell('sudo bluetoothctl power on')
        await proc.communicate()

        self.client = bleak.BleakClient(self.mac)
        await self.client.connect()

        data_service = self.client.services.get_service('e54eeef0-1980-11ea-836a-2e728ce88125')
        data_char = data_service.get_characteristic('e54eeef1-1980-11ea-836a-2e728ce88125')
        rx_char = data_service.get_characteristic('e54e0002-1980-11ea-836a-2e728ce88125')

        start_cmd = bytearray((0x53, 0x54, 0x41, 0x52, 0x54, 0x00))

        await self.client.write_gatt_char(rx_char, start_cmd)
        await self.client.start_notify(data_char, self._handle_data)


    def disconnect(self):
        if not self._connected:
            return
        self.loop.call_soon_threadsafe(lambda: self.loop.stop())
        self.thread.join()
        # now loop runs in caller thread
        self.loop.run_until_complete(self.client.disconnect())


    def __del__(self):
        self.disconnect()

