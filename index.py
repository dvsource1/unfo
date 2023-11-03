from apps.cars.runner import scrape_riyasewana
from firebase.base import cleanup_firestore

scrape_riyasewana('https://riyasewana.com/search/wagon-r-stingray/price-0-5000000')

cleanup_firestore()
