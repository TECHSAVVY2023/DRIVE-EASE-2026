import { ref, reactive, computed } from 'vue'
import car3 from '~/assets/images/sample.png'

export type FilterState = {
    category: string[]
    transmission: string
    fuel: string
    seats: string
    feature: string
    insurance: string
}

export type OpenState = {
    category: boolean
    price: boolean
    transmission: boolean
    fuel: boolean
    seats: boolean
    features: boolean
    insurance: boolean
}

export type OptionItem = {
    label: string
    count: number
}

export type Car = {
    name: string
    seats: number
    transmission: string
    price: number
    category: string
    fuel: string
    image: string
}

export function useCarFilters() {

    const showFilters = ref(false)
    const search = ref('')
    const sortBy = ref('')
    const currentPage = ref(1)
    const perPage = 6

    const priceRange = ref<[number, number]>([100, 4700])

    const filters = reactive<FilterState>({
        category: [],
        transmission: '',
        fuel: '',
        seats: '',
        feature: '',
        insurance: '',
    })

    const open = reactive<OpenState>({
        category: true,
        price: true,
        transmission: true,
        fuel: true,
        seats: true,
        features: true,
        insurance: true,
    })

    function toggleSection(key: keyof OpenState): void {
        open[key] = !open[key]
    }

    function resetFilters(): void {
        filters.category = []
        filters.transmission = ''
        filters.fuel = ''
        filters.seats = ''
        filters.feature = ''
        filters.insurance = ''

        priceRange.value = [100, 4700]
        search.value = ''
        sortBy.value = ''
        currentPage.value = 1
    }

    const categories: OptionItem[] = [
        { label: 'Economy', count: 67 },
        { label: 'Family', count: 7 },
        { label: 'Luxury', count: 7 },
        { label: 'SUV', count: 7 },
    ]

    const cars: Car[] = [
        {
            name: 'Toyota Wigo',
            seats: 5,
            transmission: 'Automatic',
            price: 1200,
            category: 'Economy',
            fuel: 'Gasoline',
            image: car3,
        },
        {
            name: 'Toyota Vios',
            seats: 5,
            transmission: 'Automatic',
            price: 1800,
            category: 'Economy',
            fuel: 'Gasoline',
            image: car3,
        },
        {
            name: 'Toyota Innova',
            seats: 7,
            transmission: 'Automatic',
            price: 2500,
            category: 'Family',
            fuel: 'Diesel',
            image: car3,
        },
        {
            name: 'Toyota Fortuner',
            seats: 7,
            transmission: 'Automatic',
            price: 3500,
            category: 'SUV',
            fuel: 'Diesel',
            image: car3,
        },
        {
            name: 'Toyota Camry',
            seats: 5,
            transmission: 'Automatic',
            price: 4000,
            category: 'Luxury',
            fuel: 'Hybrid',
            image: car3,
        },
        {
            name: 'Toyota Corolla',
            seats: 5,
            transmission: 'Automatic',
            price: 2200,
            category: 'Economy',
            fuel: 'Gasoline',
            image: car3,
        },
        {
            name: 'Toyota Hiace',
            seats: 12,
            transmission: 'Manual',
            price: 4700,
            category: 'Family',
            fuel: 'Diesel',
            image: car3,
        },
    ]

    const transmissions: OptionItem[] = [
        { label: 'Automatic', count: 67 },
        { label: 'Manual', count: 7 },
    ]

    const fuelTypes: OptionItem[] = [
        { label: 'Diesel', count: 67 },
        { label: 'Gasoline', count: 7 },
        { label: 'Hybrid', count: 7 },
    ]

    const seatOptions: OptionItem[] = [
        { label: '4+ seats', count: 67 },
        { label: '6+ seats', count: 7 },
    ]

    const featureOptions: OptionItem[] = [
        { label: 'Air conditioned', count: 67 },
        { label: 'Bluetooth', count: 7 },
    ]

    const insuranceOptions: OptionItem[] = [
        { label: 'Insurance 1', count: 67 },
        { label: 'Insurance 2', count: 7 },
    ]

    const filteredCars = computed<Car[]>(() => {
        let result = [...cars]

        if (search.value) {
            result = result.filter((c) =>
                c.name.toLowerCase().includes(search.value.toLowerCase())
            )
        }

        if (filters.category.length) {
            result = result.filter((c) =>
                filters.category.includes(c.category)
            )
        }

        result = result.filter((c) =>
            c.price >= priceRange.value[0] &&
            c.price <= priceRange.value[1]
        )

        if (sortBy.value === 'price-asc') {
            result.sort((a, b) => a.price - b.price)
        }

        if (sortBy.value === 'price-desc') {
            result.sort((a, b) => b.price - a.price)
        }

        if (sortBy.value === 'name-asc') {
            result.sort((a, b) => a.name.localeCompare(b.name))
        }

        if (sortBy.value === 'name-desc') {
            result.sort((a, b) => b.name.localeCompare(a.name))
        }

        return result
    })

    const totalPages = computed(() =>
        Math.ceil(filteredCars.value.length / perPage)
    )

    const paginatedCars = computed<Car[]>(() => {
        const start = (currentPage.value - 1) * perPage
        return filteredCars.value.slice(start, start + perPage)
    })

    return {
        showFilters,
        search,
        sortBy,
        currentPage,
        perPage,
        priceRange,
        filters,
        open,
        categories,
        transmissions,
        fuelTypes,
        seatOptions,
        featureOptions,
        insuranceOptions,
        cars,
        filteredCars,
        totalPages,
        paginatedCars,
        toggleSection,
        resetFilters,
    }
}