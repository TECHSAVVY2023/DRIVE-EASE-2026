import { ref, reactive, computed } from 'vue'
import type { Ref } from 'vue'
import { fetchCars, type Car as ApiCar } from '~/utils/api/api'
import { fetchCar, type Car as ApiCarDetail } from '~/utils/api/api'

export type FilterState = {
    category: string[]
    transmission: string[]
    fuel: string[]
    seats: string[]
    feature: string[]
}

export type OpenState = {
    category: boolean
    price: boolean
    transmission: boolean
    fuel: boolean
    seats: boolean
    features: boolean
}

export type OptionItem = {
    label: string
    count: number
}

export type Car = {
    id: number
    name: string
    available: boolean
    seats: number
    transmission: string
    price: number
    category: string
    fuel: string
    image: string
    reviews: number
    rating: number
    ownerNote: string
    images: string[]
    specifications: { label: string; value: string }[]
}

export function useCars() {
    const cars = ref<ApiCar[]>([])
    const loading = ref(false)

    const loadCars = async () => {
        loading.value = true
        try {
            cars.value = await fetchCars()
        } finally {
            loading.value = false
        }
    }

    onMounted(loadCars)

    return {
        cars,
        loading,
        loadCars,
    }
}

export function useCarOptions(cars: Ref<ApiCar[]>) {
    
    const categories = computed<OptionItem[]>(() => {
        const counts: Record<string, number> = {}

        cars.value.forEach(car => {
            counts[car.car_type] = (counts[car.car_type] || 0) + 1
        })

        return Object.entries(counts).map(([label, count]) => ({
            label,
            count
        }))
    })

    const transmissions = computed<OptionItem[]>(() => {
        const counts: Record<string, number> = {}

        cars.value.forEach(car => {
            counts[car.transmission] = (counts[car.transmission] || 0) + 1
        })

        return Object.entries(counts).map(([label, count]) => ({
            label,
            count
        }))
    })

    const fuelTypes = computed<OptionItem[]>(() => {
        const counts: Record<string, number> = {}

        cars.value.forEach(car => {
            counts[car.fuel_type] = (counts[car.fuel_type] || 0) + 1
        })

        return Object.entries(counts).map(([label, count]) => ({
            label,
            count
        }))
    })

    const seatOptions = computed<OptionItem[]>(() => {
        const ranges = {
            '4-5 seats': 0,
            '6-7 seats': 0,
            '8+ seats': 0,
        }

        cars.value.forEach(car => {
            if (car.seats >= 4 && car.seats <= 5) {
                ranges['4-5 seats']++
            } else if (car.seats <= 7) {
                ranges['6-7 seats']++
            } else {
                ranges['8+ seats']++
            }
        })

        return Object.entries(ranges).map(([label, count]) => ({
            label,
            count
        }))
    })

    const featureOptions = computed<OptionItem[]>(() => {
        const counts: Record<string, number> = {}

        cars.value.forEach(car => {
            car.features?.forEach(feature => {
            counts[feature] = (counts[feature] || 0) + 1
            })
        })

        return Object.entries(counts).map(([label, count]) => ({
            label,
            count
        }))
    })

    return {
        categories,
        transmissions,
        fuelTypes,
        seatOptions,
        featureOptions,
    }
}

// export function useCarOptions(){

//     const categories: OptionItem[] = [
//         { label: 'Economy', count: 67 },
//         { label: 'Family', count: 7 },
//         { label: 'Luxury', count: 7 },
//         { label: 'SUV', count: 7 },
//     ]

//     const transmissions: OptionItem[] = [
//         { label: 'Automatic', count: 67 },
//         { label: 'Manual', count: 7 },
//     ]

//     const fuelTypes: OptionItem[] = [
//         { label: 'Diesel', count: 67 },
//         { label: 'Gasoline', count: 7 },
//         { label: 'Hybrid', count: 7 },
//     ]

//     const seatOptions: OptionItem[] = [
//         { label: '4+ seats', count: 67 },
//         { label: '6+ seats', count: 7 },
//     ]

//     const featureOptions: OptionItem[] = [
//         { label: 'Air conditioned', count: 67 },
//         { label: 'Bluetooth', count: 7 },
//     ]

//     const insuranceOptions: OptionItem[] = [
//         { label: 'Insurance 1', count: 67 },
//         { label: 'Insurance 2', count: 7 },
//     ]

//     return{
//         categories,
//         transmissions,
//         fuelTypes,
//         seatOptions,
//         featureOptions,
//         insuranceOptions,
//     }

// }

export function useCarFilters() {
    const showFilters = ref(false)

    const search = ref('')
    const sortBy = ref('')
    const currentPage = ref(1)
    const perPage = 6

    const priceRange = ref<[number, number]>([100, 4700])

    const filters = reactive<FilterState>({
        category: [],
        transmission: [],
        fuel: [],
        seats: [],
        feature: [],
    })

    const resetFilters = () => {
        filters.category = []
        filters.transmission = []
        filters.fuel = []
        filters.seats = []
        filters.feature = []

        search.value = ''
        sortBy.value = ''
        currentPage.value = 1
        priceRange.value = [100, 4700]
    }

    const open = reactive<OpenState>({
        category: true,
        price: true,
        transmission: true,
        fuel: true,
        seats: true,
        features: true,
    })

    function toggleSection(key: keyof OpenState): void {
        open[key] = !open[key]
    }

    return {
        search,
        sortBy,
        currentPage,
        open,
        toggleSection,
        perPage,
        priceRange,
        filters,
        resetFilters,
        showFilters,
    }
}

export function useFilteredCars(
    cars: Ref<ApiCar[]>,
    filtersState: ReturnType<typeof useCarFilters>
) {
    const filteredCars = computed(() => {
        let result = [...cars.value]

        if (filtersState.search.value) {
            const s = filtersState.search.value.toLowerCase()

            result = result.filter(car =>
                `${car.brand} ${car.model}`
                    .toLowerCase()
                    .includes(s)
            )
        }

        if (filtersState.filters.category.length) {
            result = result.filter(car =>
                filtersState.filters.category.includes(car.car_type)
            )
        }

        if (filtersState.filters.transmission.length) {
            result = result.filter(car =>
                filtersState.filters.transmission.includes(car.transmission)
            )
        }

        if (filtersState.filters.fuel.length) {
            result = result.filter(car =>
                filtersState.filters.fuel.includes(car.fuel_type)
            )
        }

        const seatRules: Record<string, (seats: number) => boolean> = {
            '4+ seats': (s) => s >= 4,
            '6+ seats': (s) => s >= 6,
        }

        if (filtersState.filters.seats.length) {
            result = result.filter(car =>
                filtersState.filters.seats.some(label => {
                    const seats = car.seats

                    if (label === '4-5 seats') return seats >= 4 && seats <= 5
                    if (label === '6-7 seats') return seats >= 6 && seats <= 7
                    if (label === '8+ seats') return seats >= 8

                    return false
                })
            )
        }

        if (filtersState.filters.feature.length) {
            result = result.filter(car =>
                car.features?.some(feature =>
                    filtersState.filters.feature.includes(feature)
                )
            )
        }

        result = result.filter(car =>
            Number(car.price_per_day) >= filtersState.priceRange.value[0] &&
            Number(car.price_per_day) <= filtersState.priceRange.value[1]
        )

        switch (filtersState.sortBy.value) {
            case 'price-asc':
                result.sort((a, b) =>
                    Number(a.price_per_day) - Number(b.price_per_day)
                )
                break

            case 'price-desc':
                result.sort((a, b) =>
                    Number(b.price_per_day) - Number(a.price_per_day)
                )
                break
            case 'name':
            result.sort((a, b) =>
                `${a.brand} ${a.model}`
                .toLowerCase()
                .localeCompare(`${b.brand} ${b.model}`.toLowerCase())
            )
            break
        }

        return result
    })

    const totalPages = computed(() =>
        Math.ceil(
            filteredCars.value.length /
            filtersState.perPage
        )
    )

    const paginatedCars = computed(() => {
        const start =
            (filtersState.currentPage.value - 1) *
            filtersState.perPage

        return filteredCars.value.slice(
            start,
            start + filtersState.perPage
        )
    })

    return {
        filteredCars,
        paginatedCars,
        totalPages,
    }
}

export function useCarDetail() {
    const car = ref<ApiCarDetail | null>(null)
    const loading = ref(false)
    const error = ref<unknown>(null)

    const getCar = async (carId: string, options?: { force?: boolean }) => {
        loading.value = true
        error.value = null

        try {
            car.value = await fetchCar(carId, {
                force: options?.force,
            })
        } catch (err) {
            error.value = err
            car.value = null
        } finally {
            loading.value = false
        }
    }

    return {
        car,
        loading,
        error,
        getCar,
    }
}