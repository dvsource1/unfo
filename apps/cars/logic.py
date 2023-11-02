from firebase_admin import firestore

from firebase.logic import add_entry


def process_car_results(results):
    for result in results:
      title = result.find('h2').text.strip()
      url = result.find('div', class_='imgbox').find('a')['href'].strip()
      
      add_entry('cars', {
        'title': title,
        'url': url
      })
      print(f"{title} - {url}")
      
      