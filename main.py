from apps.cars.runner import scrape_riyasewana
from apps.requests.entity import Source
from apps.requests.runner import scrape_requests
from firebase.base import cleanup_firestore
from firebase.logic import get_entries


def run_scaper():
  source_dicts = get_entries('sources', with_subcollections=True)
  sources = [Source.from_dict(source_dict) for source_dict in source_dicts]
  
  for source in sources:
    if source.is_active:
      for request in source.requests:
        if request.is_active:
          scrape_requests(source, request)


if __name__ == '__main__':
  run_scaper()
  
  cleanup_firestore()
