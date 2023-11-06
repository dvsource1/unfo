import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from apps.cars.entity import Car, Seller

from src.utils import make_it_number


def get_seller_info(seller_elm):
  if seller_elm is None:
    return None
  text = seller_elm.text.strip()
  pattern = r'Posted by (?P<name>.+) on (?P<datetime>.+), (?P<location>.+)'
  match = re.search(pattern, text)
  
  actual_datetime = datetime.strptime(match.group('datetime'), '%Y-%m-%d %I:%M %p')
  
  return {
    'name': match.group('name'),
    'location': match.group('location'),
    'datetime': actual_datetime
  }

def save_seller(seller_info, phone=None):
  print(f"Saving seller: {seller_info}")
  
  if phone is not None:
    seller_info['phone'] = phone
    Seller.from_dict(seller_info).update()


# -----------------------------------------------


def extract_results_count(results_text: str) -> tuple or None:
  if results_text:
    start, end, total = map(int, re.findall(r'\d+', results_text))
    actual_start = start if start != 1 else 0
    return (total, end - actual_start)
  else:
    return None