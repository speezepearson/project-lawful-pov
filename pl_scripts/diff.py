from pathlib import Path
import subprocess

from . import ALL_PAGES, OUTDIR, Page

EDITED_PAGES = {
  p for p in ALL_PAGES
  if (p.path / 'before-edit.html').exists() and (p.path / 'after-edit.html').exists()
}

def patchpath(page: Page) -> Path:
  return Path('patches') / str(page.thread_id) / f'{page.page_num}.patch'

def main():
  for page in EDITED_PAGES:
    before = page.path / 'before-edit.html'
    after = page.path / 'after-edit.html'

    dest = patchpath(page)
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.call(['diff', '-u', before, after], stdout=dest.open('w'))

_DOIT_TASKSPEC = {
  'file_dep': [
    __file__,
    *(page.path / f'{t}-edit.html'
      for page in EDITED_PAGES
      for t in ['before', 'after']
      ),
    ],
  'targets': [patchpath(page) for page in EDITED_PAGES],
  'actions': [main],
}
