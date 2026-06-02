import { ref } from 'vue'
import car1 from '~/assets/images/car1.png'
import car2 from '~/assets/images/car2.png'
import car3 from '~/assets/images/car3.png'

export const useLandingPage = () => {

  const stats = [
    { value: '10k', label: 'Happy customers' },
    { value: '10k', label: 'Happy customers' },
    { value: '10k', label: 'Happy customers' },
    { value: '10k', label: 'Happy customers' },
  ]

  const reviews = [
    {
      name: 'Juber Sahiol',
      stars: 5,
      text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In sit amet luctus velit. Pellentesque egestas sagittis placerat. Nulla commodo vehicula.',
      car: 'Rented Toyota Wigo Asenso',
    },
    {
      name: 'Juber Sahiol',
      stars: 5,
      text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In sit amet luctus velit. Pellentesque egestas sagittis placerat. Nulla commodo vehicula.',
      car: 'Rented Toyota Wigo Asenso',
    },
    {
      name: 'Juber Sahiol',
      stars: 5,
      text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In sit amet luctus velit. Pellentesque egestas sagittis placerat. Nulla commodo vehicula.',
      car: 'Rented Toyota Wigo Asenso',
    },
  ]

  const cars = [
    {
        name: 'Toyota Wigo',
        price: '₱1,200',
        image: car1,
    },
    {
        name: 'Mitsubishi Xforce',
        price: '₱1,800',
        image: car2,
    },
    {
        name: 'Ford Raptor',
        price: '₱2,500',
        image: car3,
    },
  ]

  const faqs = [
    {
        question: 'What documents are required to rent a car?',
        answer: 'You need a valid driver’s license and a government-issued ID.'
    },
    {
        question: 'Can I book a car online?',
        answer: 'Yes, you can reserve your preferred vehicle directly from our website.'
    },
    {
        question: 'Do you offer airport pickup?',
        answer: 'Yes, airport pickup and drop-off are available upon request.'
    },
    {
        question: 'Do you offer airport pickup?',
        answer: 'Yes, airport pickup and drop-off are available upon request.'
    },
    {
        question: 'Do you offer airport pickup?',
        answer: 'Yes, airport pickup and drop-off are available upon request.'
    }
  ]

  return {
    stats,
    reviews,
    cars,
    faqs,
  }
}