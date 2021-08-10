import dbus as _dbus

_bus = _dbus.SystemBus()
_obj = _bus.get_object('ru.leadpogrommer.Breather', '/')
_breather = _dbus.Interface(_obj, "ru.leadpogrommer.Breather")


def connect(mac: str) -> bool:
    """
    Connects to bluetooth sensor

    :param mac: Mac address of the sensor
    :return: True if device was connected, False if some error occurred
    """
    return _breather.connect(mac)


def disconnect():
    """
    Disconnects from the sensor. Always call this function at the end of your program

    :return: nothing
    """
    _breather.disconnect()


def read() -> float:
    """
    Reads data from sensor

    :return: Current value from sensor
    """
    return _breather.getData()
