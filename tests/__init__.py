if __name__ == '__main__':
    import sys
    sys.path.append('../src')

    from unior.connection import Connection
    import signal
    import time

    is_running = True


    def signal_handler(_, __):
        global is_running
        is_running = False


    signal.signal(signal.SIGINT, signal_handler)
    connection = Connection('ef:f4:38:77:8f:bc')
    prev_val = 0
    while is_running:
        v = connection.get_value()
        delta = v - prev_val
        prev_val = v
        print(delta, v)
        # time.sleep(0.01)

    print("Stooping")
    connection.disconnect()
    print("Stopped")


