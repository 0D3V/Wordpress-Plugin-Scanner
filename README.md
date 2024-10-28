# WordPress Plugin Discovery

A Python tool for scanning WordPress websites to identify installed plugins and update the plugin list from WordPress.org.

## Features

- Validates URLs and checks accessibility
- Detects installed plugins
- Multi-threaded scanning
- Updates plugin list from WordPress.org

## Requirements

- Python 3.x
- `lxml` library

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/0D3V/wp-plugin-scanner.git
   cd wp-plugin-Discovery
## Usage

### Scan Websites

Run the script with:

  ```bash
  python main.py <sites_file> <plugins_file>
