import re
import requests
from bs4 import BeautifulSoup
from apps.cars.entity import Car
from apps.cars.logic import extract_results_count, get_next_page_url, get_seller_info, save_seller

from apps.requests.entity import Request
from src.utils import make_it_number


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
    elif key == 'Engine (cc)':
      key = 'Engine'

    if key in ['Contact', 'Price', 'YOM', 'Mileage', 'Engine']:
      value = make_it_number(value)

    if key not in ['Get Leasing']:
      the_dict[key.lower()] = value
      
  seller_info = get_seller_info(seller_elm)
  if seller_info:
    phone = the_dict.get('contact')
    save_seller(seller_info, phone)
    print(f"Saved seller: {seller_info}")
    the_dict['seller'] = phone
    the_dict['timestamp'] = seller_info.get('datetime')

  print(the_dict)
  Car.from_dict(the_dict).save()

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


def process(request: Request, soup, headers):
  results = soup.find_all('li', class_='item round')
  if len(results) > 0:
    process_car_results(results, headers)
  
  if request.is_paginate:
    next_page_elm = soup.find('a', string='Next')
    if next_page_elm:
      goto_next_page(next_page_elm['href'], headers)

    
def goto_next_page(url: str, headers):
  if url is None:
    print("No more pages to go to")
    return
  else:
    actual_url = f"https:{url}"
    print(f"Going to next page: {actual_url}")
    
    response = requests.get(actual_url, headers=headers)
    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
      process(soup, headers)


def scrape_riyasewana(request: Request, headers):
  response = requests.get(request.base, headers=headers)
  
  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results_elm = soup.find('h2', class_='results')
    results_count = extract_results_count(results_elm.text if results_elm else None )
    if results_count:
      total_results, results_per_page = results_count
      process(request, soup, headers)
  else:
    print(f"Error: {response.status_code}")
    print(response.text)
