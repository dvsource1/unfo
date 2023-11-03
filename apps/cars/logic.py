from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
from firebase_admin import firestore

from firebase.logic import add_entry, set_entry
from util.string_utils import make_it_number


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
    return set_entry('sellers', phone, seller_info)
  
  return None
 

def process_car_page(soup, url):
  seller_elm = soup.find('h2')
  cells = soup.find_all('td', class_='aleft')

  the_dict = {'URL': url}
  
  for i in range(0, len(cells), 2):
    key = cells[i].text.strip()
    value = cells[i+1].text.strip()

    if key == 'Mileage (km)':
      key = 'Mileage'
    elif key == 'Fuel Type':
      key = 'Fuel'

    if key in ['Contact', 'Price', 'YOM', 'Mileage']:
      value = make_it_number(value)

    if key not in ['Get Leasing']:
      the_dict[key.lower()] = value
      
  seller_info = get_seller_info(seller_elm)
  if seller_info:
    sid = save_seller(seller_info, the_dict.get('contact'))
    print(f"Saved seller: {sid}")
    the_dict['seller'] = sid

  # print(the_dict)
  # add_entry('cars', the_dict)

def goto_car_page(url: str, headers):
  print(f"Going to car page: {url}")
  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    process_car_page(soup, url)
  else:
    print(f"Error in car page: {response.status_code}")


def process_car_results(results, headers):
    for result in results:
      title = result.find('h2').text.strip()
      url = result.find('div', class_='imgbox').find('a')['href'].strip()
      goto_car_page(url, headers)
      print(f"{title} - {url}")
