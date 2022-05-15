from pathlib import Path
from typing import NamedTuple

OUTDIR = Path('out')

class Page(NamedTuple):
  thread_id: int
  page_num: int

  @property
  def path(self) -> Path:
    return OUTDIR / str(self.thread_id) / f'{self.page_num}'

THREAD_PAGE_COUNTS = {
  4582: 5,
}

ALL_PAGES = {
  Page(thread_id, page_num)
  for thread_id, page_count in THREAD_PAGE_COUNTS.items()
  for page_num in range(page_count)
}
