import sys
import bs4
import requests

from . import ALL_PAGES

def main():
  for page in ALL_PAGES:
    dest = page.path / 'original.html'
    if dest.exists():
      print(f'skipping {dest} because it already exists', file=sys.stderr)
      continue
    html = requests.get(f'https://www.glowfic.com/posts/{page.thread_id}?page={page.page_num}&per_page=100').text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(soup.prettify())

_DOIT_TASKSPEC = {
  'file_dep': [__file__],
  'targets': [page.path / 'original.html' for page in ALL_PAGES],
  'actions': [main],
}
