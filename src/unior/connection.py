import bleak
import asyncio
import struct
from .data_processing import BreathProcessor
import threading
import queue


class Connection:
    def __init__(self, mac: str):
        self._starting_thread = threading.current_thread()
        self._disconnect_lock = threading.Lock()
        self._queue = queue.LifoQueue(maxsize=100_000)
        self.breathe_processor = BreathProcessor()
        self.mac = mac
        self._value = 0
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._bootstrap())
        self.thread = threading.Thread(name=f'Device {self.mac} thread', target=lambda :self.loop.run_forever())
        self.thread.start()
        self._connected = True
        # now loop runs in another thread

    def _handle_data(self, i: int, bytes: bytearray):
        # print(1)
        data = struct.unpack('ff25f', bytes)
        values = list(data[2:])
        can_keep_up = True
        for v in values:
            v = self.breathe_processor.process(v)
            self._value = v
            try:
                self._queue.put_nowait(v)
            except queue.Full:
                can_keep_up = False
        if not can_keep_up:
            print("WARNING: sensor data was ignored! Your code can't keep up with incoming data! New data will be lost!")

    @property
    def prev_value(self):
        # this is probably thread-safe.... I hope
        return self._value

    @property
    def has_new_values(self):
        return not self._queue.empty()

    def get_value(self, timeout=None):
        if not self._connected:
            raise Exception("Device disconnected")
        v = self._queue.get(timeout=timeout)
        if v is None:
            raise Exception("Device disconnected")
        return v

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
        self.client.set_disconnected_callback(lambda _: self._disconnect_callback())
        self.loop.create_task(self._thread_checker())


    def disconnect(self):
        with self._disconnect_lock:
            if not self._connected:
                return
            self._connected = False
        self.loop.call_soon_threadsafe(lambda: self.loop.stop())
        self.thread.join()
        # now loop runs in caller thread
        self.loop.run_until_complete(self.client.disconnect())

    def _disconnect_callback(self):
        with self._disconnect_lock:
            if not self._connected:
                return
            self._connected = False
        self.loop.stop()
        self._queue.put(None)
        print("Device was disconnected")

    async def _thread_checker(self):
        while True:
            if not self._starting_thread.is_alive() and self._connected:
                print("WARNING: you didn't call disconnect! Shame on you!")
                await self.client.disconnect()
                self.loop.stop()
                break
            await asyncio.sleep(0.5)

    def __del__(self):
        self.disconnect()

