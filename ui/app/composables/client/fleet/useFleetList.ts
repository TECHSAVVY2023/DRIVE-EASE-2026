import type { Car } from '~/utils/api/api'
import type { FilterOption } from '~/utils/api/api'

const loading = ref(false)

const fleet = ref<Car[]>([])

const count = ref(0)

const nextPage = ref<string | null>(null)
const previousPage = ref<string | null>(null)

const currentPage = ref(1)

//Selected filters
const search = ref("")
const selectedCarType = ref<string[]>([])
const selectedTransmission = ref<string[]>([])
const selectedSeat = ref<string[]>([])
const selectedFuel = ref<string[]>([])
const selectedFeature = ref<string[]>([])

const brand = ref("")
const maxPrice = ref(4700)

//All filters from the backend to be displayed in the sidebar
const carTypeOptions = ref<FilterOption[]>([])
const transmissionOptions = ref<FilterOption[]>([])
const seatOptions = ref<FilterOption[]>([])
const fuelTypeOptions = ref<FilterOption[]>([])
const featureOptions = ref<FilterOption[]>([])

export function useFleetList() {
    const { fetchFleet } = useFleet()

    const showFilters = ref(false)
    const sortBy = ref('')

    const pageSize = 9

    const totalPages = computed(() =>
        Math.ceil(count.value / pageSize)
    )
    
    const fetchCars = async () => {
        loading.value = true

        try {
            const res = await fetchFleet({
                page: currentPage.value,
                search: search.value,
                brand: brand.value,
                transmission: selectedTransmission.value.join(","),
                seats: selectedSeat.value.join(","),
                car_type: selectedCarType.value.join(","),
                fuel_type: selectedFuel.value.join(","),
                features: selectedFeature.value,
                sort: sortBy.value,
                max_price: maxPrice.value,
            })

            console.log("Sort:", sortBy.value)
            console.log(res.results.map(car => car.price_per_day))

            fleet.value = res.results

            count.value = res.count

            carTypeOptions.value = res.filters.categories
            transmissionOptions.value = res.filters.transmissions
            seatOptions.value = res.filters.seats
            fuelTypeOptions.value = res.filters.fuel
            featureOptions.value = res.filters.features

            nextPage.value = res.next ?? null
            previousPage.value = res.previous ?? null

        } finally {
            loading.value = false
        }
    }

    watch(
        [currentPage, search, selectedCarType, selectedTransmission, selectedSeat, selectedFuel, selectedFeature, maxPrice,
            sortBy
        ],
        () => {
            fetchCars()
        }
    )

    watch(sortBy, (value) => {
        console.log("sortBy changed:", value)
    })

    watch([selectedCarType, selectedTransmission, selectedFuel, selectedSeat, selectedFeature, maxPrice, sortBy], () => {
        currentPage.value = 1
    })

    const resetFilters = async () => {
        search.value = ""
        selectedCarType.value = []
        selectedTransmission.value = []
        selectedSeat.value = []
        selectedFeature.value = []
        selectedFuel.value = []
        maxPrice.value = 4700
    }

    return {
        loading,
        fleet,
        count,
        nextPage,
        previousPage,
        currentPage,
        search,
        brand,
        showFilters,
        sortBy,
        maxPrice,

        selectedCarType,
        selectedTransmission,
        selectedSeat,
        selectedFuel,
        selectedFeature,

        carTypeOptions,
        transmissionOptions,
        seatOptions,
        fuelTypeOptions,
        featureOptions,

        fetchCars,
        totalPages,
        resetFilters,
    }
}