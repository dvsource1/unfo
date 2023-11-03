import re
import requests
from bs4 import BeautifulSoup

from apps.cars.logic import process_car_results
from apps.requests.model import Request


def extract_results_count(soup) -> tuple or None:
  results_elm = soup.find('h2', class_='results')
  
  if results_elm:
    start, end, total = map(int, re.findall(r'\d+', results_elm.text))
    actual_start = start if start != 1 else 0
    return (total, end - actual_start)
  else:
    return None


def get_next_page_url(soup) -> str or None:
  next_page_elm = soup.find('a', string='Next')
  
  if next_page_elm:
    return next_page_elm['href']
  else:
    return None


def find_results(soup):
  return soup.find_all('li', class_='item round')
  
    
def process(request: Request, soup, headers):
  results = find_results(soup)
  if len(results) > 0:
    process_car_results(results, headers)
  
  if request.is_paginate:
    goto_next_page(get_next_page_url(soup), headers)

    
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
    
    results_count = extract_results_count(soup)
    if results_count:
      total_results, results_per_page = results_count
      process(request, soup, headers)
  else:
    print(f"Error: {response.status_code}")
    print(response.text)
