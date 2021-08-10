import time
from connection import Connection

# e2e test kekw
if __name__ == '__main__':
  connection = Connection('4EB09980-0C37-45C9-BE84-25EEFE6B64F2')

  time.sleep(5)
  del connection
  exit(0)
  