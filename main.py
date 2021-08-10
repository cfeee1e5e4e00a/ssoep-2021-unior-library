import bleak
import asyncio
import struct
from data_processing import BreathProcessor

floyd = BreathProcessor()

def handle_data(i, bytes: bytearray):
    # print(bytes)
    test = struct.unpack('ff25f', bytes)
    values = list(test[2:])
    for v in values:
        print(floyd.process(v))

async def bootstrap():
    client = bleak.BleakClient('ef:f4:38:77:8f:bc')
    await client.connect()
    data_service = client.services.get_service('e54eeef0-1980-11ea-836a-2e728ce88125')
    data_char = data_service.get_characteristic('e54eeef1-1980-11ea-836a-2e728ce88125')
    rx_char = data_service.get_characteristic('e54e0002-1980-11ea-836a-2e728ce88125')
    start_cmd = bytearray((0x53, 0x54, 0x41, 0x52, 0x54, 0x00))
    await client.write_gatt_char(rx_char, start_cmd)
    await client.start_notify(data_char, handle_data)
    await asyncio.sleep(100)

    await client.disconnect()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bootstrap())
