#!/usr/bin/env python

import argparse
import re
import urllib.request
import lxml.html
import os
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

def _main():
    argParser = argparse.ArgumentParser(description='Scan WordPress-powered websites and identify installed plugins')
    argParser.add_argument('sites_file', metavar='<sites file>', help='File with list of websites to scan')
    argParser.add_argument('plugins_file', metavar='<plugins file>', help='File to read/write the list of plugins')
    argParser.add_argument('-u', '--update', type=int, metavar='<page number>', dest='pageN', help='Update the list of plugins from wordpress.org up to <page number>')
    args = argParser.parse_args()

    if args.pageN:
        update(args.pageN, args.plugins_file)
    else:
        scan_sites(args.sites_file, args.plugins_file)

def _isUrl(url):
    pattern = re.compile(r'^https?://[\w\d\-.]+/(([\w\d\-]+/)+)?$')
    return pattern.match(url) is not None

def _isWebsiteAlive(url):
    try:
        return urllib.request.urlopen(url).getcode() == 200
    except:
        return False

def _parseHrefs(html):
    doc = lxml.html.document_fromstring(html)
    pattern = re.compile(r'/plugins/([\w\d\-]+)/')
    pluginsList = []
    links = doc.cssselect('div.plugin-block h3 a')
    for link in links:
        plugin = pattern.search(link.get('href')).group(1)
        pluginsList.append(plugin)
        print(plugin + '[+]')
    return pluginsList

def _writePlugins(pluginsList, plugins_file):
    with open(plugins_file, 'w') as file:
        file.write('\n'.join(pluginsList))

def _readPlugins(plugins_file):
    if not os.path.isfile(plugins_file):
        print(f"Plugins file '{plugins_file}' not found. Run with --update to create it.")
        return []
    with open(plugins_file, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def scan_site(url, pluginsList):
    if not _isUrl(url):
        print(f'The URL "{url}" does not match the expected pattern.')
        return
    if not _isWebsiteAlive(url):
        print(f'Website "{url}" is not accessible.')
        return

    print(f'Scanning {url}...')
    # Get the domain name for the filename
    domain = urlparse(url).netloc.replace("www.", "")
    output_file = f"./output/{domain}.txt"
    
    for plugin in pluginsList:
        try:
            code = urllib.request.urlopen(f'{url}/wp-content/plugins/{plugin}/').getcode()
            if code != 404:
                print(f"{plugin} [+]")
                # Write the found plugin to the file immediately
                with open(output_file, 'a') as file:
                    file.write(plugin + '\n')
        except:
            continue

    print(f"Plugins for {url} saved in '{output_file}'.")

def scan_sites(sites_file, plugins_file):
    try:
        with open(sites_file, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Sites file '{sites_file}' not found.")
        return

    pluginsList = _readPlugins(plugins_file)
    if not pluginsList:
        return

    # Use ThreadPoolExecutor with 10 workers
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit each site scan as a separate task
        for url in urls:
            executor.submit(scan_site, url, pluginsList)

def update(pageN, plugins_file):
    pluginsList = []
    for page in range(1, pageN + 1):
        html = urllib.request.urlopen(f'http://wordpress.org/extend/plugins/browse/popular/page/{page}/').read()
        pluginsList.extend(_parseHrefs(html))
    _writePlugins(pluginsList, plugins_file)
    print(f"Plugins list updated in '{plugins_file}'.")

if __name__ == "__main__":
    _main()
