// import puppeteer from 'puppeteer'
import axios from 'axios'
import cheerio, { CheerioAPI } from 'cheerio'
import { processCarElements } from './app/cars'
import { initializeApp, cert } from 'firebase-admin/app'
import { getFirestore } from 'firebase-admin/firestore'

const firebase = initializeApp({
  credential: cert(require('./.firebase/firebase-service.json')),
  databaseURL: 'https://riyasewana-3e8c5-default-rtdb.firebaseio.com',
})

const db = getFirestore()

const getResultCount = ($: CheerioAPI): [number, number] | null => {
  const totalResultsText = $('.results').text()
  const regex = /(\d+) - (\d+) of (\d+) Search Results/
  const match = totalResultsText.match(regex)

  if (match) {
    const [, start, end, totalResults] = match
    const actualStart = start === '1' ? 0 : parseInt(start, 10)
    const actualEnd = parseInt(end, 10)
    return [parseInt(totalResults, 10), actualEnd - actualStart]
  }
  return null
}

const getNextPageUrl = ($: CheerioAPI) => {
  const nextPageLink = $('.pagination a:contains("Next")')
  const nextPageUrl = nextPageLink.attr('href')
  console.log('Next page url:', nextPageUrl)
  return nextPageUrl
}

const processResults = ($: CheerioAPI) => {
  const carsContainer = $('#content > ul')
  const cars = carsContainer.children()
  processCarElements(db, $, cars)
  console.log('Cars count:', cars.length)
}

const goToNextPage = async (pageUrl: string | undefined) => {
  if (!pageUrl) {
    return
  }

  const actualURL = `https:${pageUrl}`

  const response = await axios.get(actualURL)
  const $ = cheerio.load(response.data)

  const resultsCount = getResultCount($)
  if (!resultsCount) {
    console.log('No results found')
    return
  }

  processResults($)
  goToNextPage(getNextPageUrl($))
}

;(async () => {
  const response = await axios.get(
    'https://riyasewana.com/search/wagon-r-stingray/price-0-5000000'
  )
  const $ = cheerio.load(response.data)

  const resultsCount = getResultCount($)
  if (!resultsCount) {
    console.log('No results found')
    return
  }
  const [totalResultsCount, resultsCountOnPage] = resultsCount

  console.log('Total result count:', totalResultsCount)
  console.log('Results count on page:', resultsCountOnPage)

  processResults($)
  // goToNextPage(getNextPageUrl($))
})()
