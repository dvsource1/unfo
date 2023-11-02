import { Cheerio, CheerioAPI, Element } from 'cheerio'
import Car from './car'

export const processCarElements = (
  db: any,
  $: CheerioAPI,
  carElements: Cheerio<Element>
) => {
  console.log('Car elements:', carElements.length)

  const cars: Car[] = []

  carElements.each((index, car: Element) => {
    // Do something with each car element
    const title = $(car).text()

    cars.push({
      title,
    })

    console.log(`Car ${index + 1}: ${title}`)
  })

  const carsCollection = db.collection('cars')
  console.log('Cars collection:', carsCollection)
  if (carsCollection && cars.length) {
    cars.forEach(async (car) => {
      try {
        const res = await carsCollection.add(car)
        car.id = res.id
      } catch (error) {
        console.error(error)
      }
    })
  }
}
