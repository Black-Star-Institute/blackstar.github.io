import argparse
import json
import logging
from pathlib import Path

import requests
import requests_cache


DESCRIPTION = """
Get the URLs for pages from the Internet Archive (Wayback machine).
"""

USAGE = """
python -m wayback wayback/urls.txt --timestamp 20060101 > urls.txt
"""

logger = logging.getLogger(__name__)


def get_args():
    "Command line arguments"
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('path', type=Path, help='Path of text file containing a list of URLs to scrape')
    parser.add_argument('--timestamp', help="Wayback Machine target, YYYYMMDD or YYYYMMDDhhmmss e.g. 20060101")
    parser.add_argument('--loglevel', default='INFO')
    return parser.parse_args()


def wayback(session: requests.Session, url: str, timestamp: str=None) -> dict:
    """
    Wayback Machine API
    https://archive.org/help/wayback_api.php

    Get the closest snapshot near the timestamp

    :param timestamp: YYYYMMDDhhmmss
    """

    url = f"http://archive.org/wayback/available?url={url}"

    if timestamp:
        url += f"&timestamp={timestamp}"

    response = session.get(url)
    response.raise_for_status()

    return response.json()

def main():
    args = get_args()
    logging.basicConfig(level=args.loglevel)

    session = requests_cache.CachedSession()

    urls = set()

    # Open URL list
    with args.path.open() as file:
        for url in file:
            url = url.strip()
            logger.info(url)
            urls.add(url)

            # Get Wayback Machine record
            snapshots = wayback(session, url=url, timestamp=args.timestamp)
            logger.info(json.dumps(snapshots))
            snapshot_url = snapshots['archived_snapshots']['closest']['url']
            urls.add(snapshot_url)

    for url in urls:
        print(url)

if __name__ == '__main__':
    main()
