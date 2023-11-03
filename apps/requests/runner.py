from apps.cars.runner import scrape_riyasewana
from apps.requests.model import Request, Source


headers = {
  'User-Agent': 'PostmanRuntime/7.34.0'
}


def scrape_requests(source: Source, request: Request):
  if source.key == 'RIYASEWANA':
    scrape_riyasewana(request, headers)
  