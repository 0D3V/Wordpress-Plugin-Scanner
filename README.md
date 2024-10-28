python main.py -h
usage: main.py [-h] [-u <page number>] <sites file> <plugins file>

python main.py list.txt plugins.txt

Scan WordPress-powered websites and identify installed plugins

positional arguments:
  <sites file>          File with list of websites to scan
  <plugins file>        File to read/write the list of plugins

options:
  -h, --help            show this help message and exit
  -u <page number>, --update <page number>
                        Update the list of plugins from wordpress.org up to <page number>
