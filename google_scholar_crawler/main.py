from scholarly import scholarly
import jsonpickle
import json
from datetime import datetime
import os
import argparse
import sys


def get_scholar_id():
  """Determine Google Scholar ID from (in order): CLI arg, id-file, env var, local gs_id.txt, or interactive input."""
  parser = argparse.ArgumentParser(description="Fetch Google Scholar author by ID")
  parser.add_argument('-i', '--id', help='Google Scholar author ID (e.g., 5_B6lbwAAAAJ)')
  parser.add_argument('--id-file', help='Path to a file containing only the author ID')
  args = parser.parse_args()

  if args.id:
    return args.id.strip()

  if args.id_file and os.path.exists(args.id_file):
    with open(args.id_file, 'r') as f:
      return f.read().strip()

  env = os.environ.get('GOOGLE_SCHOLAR_ID')
  if env:
    return env.strip()

  local_path = os.path.join(os.path.dirname(__file__), 'gs_id.txt')
  if os.path.exists(local_path):
    with open(local_path, 'r') as f:
      return f.read().strip()

  # Fallback to interactive prompt (useful when running manually)
  if sys.stdin and sys.stdin.isatty():
    try:
      val = input('Enter Google Scholar author ID: ').strip()
      if val:
        return val
    except Exception:
      pass

  return None


scholar_id = get_scholar_id()
if not scholar_id:
  print('Error: no Google Scholar ID provided. Use -i/--id, set GOOGLE_SCHOLAR_ID, or create gs_id.txt', file=sys.stderr)
  sys.exit(1)

try:
  author: dict = scholarly.search_author_id(scholar_id)
  # Allow skipping publications (they can take much longer) via env var SKIP_PUBLICATIONS
  skip_pubs = os.environ.get('SKIP_PUBLICATIONS', '').lower() in ('1', 'true', 'yes')
  if skip_pubs:
    scholarly.fill(author, sections=['basics', 'indices', 'counts'])
  else:
    scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
except Exception as e:
  print(f'Failed to fetch author data for id "{scholar_id}": {e}', file=sys.stderr)
  sys.exit(2)

name = author.get('name')
author['updated'] = str(datetime.now())
# convert publications list to dict keyed by author_pub_id when available
if isinstance(author.get('publications'), list):
  author['publications'] = {v.get('author_pub_id') or str(idx): v for idx, v in enumerate(author['publications'])}

print(json.dumps(author, indent=2, ensure_ascii=False))

os.makedirs('results', exist_ok=True)
with open(f'results/gs_data.json', 'w') as outfile:
  json.dump(author, outfile, ensure_ascii=False)

shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": f"{author.get('citedby', '0')}",
}
with open(f'results/gs_data_shieldsio.json', 'w') as outfile:
  json.dump(shieldio_data, outfile, ensure_ascii=False)

# Also write copies next to this script for backwards compatibility
file_path = os.path.join(os.path.dirname(__file__), "gs_data.json")
with open(file_path, 'w') as outfile:
  json.dump(author, outfile, ensure_ascii=False)

file_path = os.path.join(os.path.dirname(__file__), "gs_data_shieldsio.json")
with open(file_path, 'w') as outfile:
  json.dump(shieldio_data, outfile, ensure_ascii=False)
