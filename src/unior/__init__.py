# e2e test kekw
if __name__ == '__main__':
    import signal
    import time
    from connection import Connection

    is_running = True

    def signal_handler(_, __):
        global is_running
        is_running = False

    signal.signal(signal.SIGINT, signal_handler)
    connection = Connection('ef:f4:38:77:8f:bc')

    while is_running:
        print(connection.value)
        time.sleep(0.01)

    print("Stooping")
    connection.disconnect()
    print("Stopped")
