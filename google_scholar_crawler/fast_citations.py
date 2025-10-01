#!/usr/bin/env python3
"""Lightweight fetcher that retrieves the 'cited by' number from a Google Scholar profile page.

This is a best-effort, minimal-dependency fallback for CI to avoid long runs.
"""
import requests
import re
import sys
import json
import os
from datetime import datetime


def fetch_citedby(scholar_id, hl='en'):
    url = f'https://scholar.google.com/citations?user={scholar_id}&hl={hl}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; GitHubAction/1.0; +https://github.com)'
    }
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    text = r.text
    # best-effort regex: look for 'Cited by' followed by numbers
    m = re.search(r'(?i)Cited by[^0-9]*([0-9,]+)', text)
    if not m:
        # fallback: look for 'citedby' pattern used by scholarly JSON
        m2 = re.search(r'"citedby"\s*:\s*(\d+)', text)
        if m2:
            return int(m2.group(1))
        return None
    val = m.group(1).replace(',', '')
    try:
        return int(val)
    except ValueError:
        return None


def main():
    if len(sys.argv) > 1:
        scholar_id = sys.argv[1]
    else:
        scholar_id = os.environ.get('GOOGLE_SCHOLAR_ID')
        if not scholar_id:
            # fallback to file
            pid = os.path.join(os.path.dirname(__file__), 'gs_id.txt')
            if os.path.exists(pid):
                scholar_id = open(pid).read().strip()
    if not scholar_id:
        print('No scholar id provided', file=sys.stderr)
        sys.exit(1)

    cited = fetch_citedby(scholar_id)
    out = {
        'schemaVersion': 1,
        'label': 'citations',
        'message': str(cited if cited is not None else '0'),
    }
    # write results
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'results'), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), '..', 'results', 'gs_data_shieldsio.json'), 'w') as f:
        json.dump(out, f, ensure_ascii=False)
    # also write local copy
    with open(os.path.join(os.path.dirname(__file__), 'gs_data_shieldsio.json'), 'w') as f:
        json.dump(out, f, ensure_ascii=False)

    # print minimal JSON for logs
    print(json.dumps({'scholar_id': scholar_id, 'citedby': cited, 'updated': str(datetime.now())}, ensure_ascii=False))


if __name__ == '__main__':
    main()
