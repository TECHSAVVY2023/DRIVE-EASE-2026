import { ref, reactive, computed, watch } from 'vue'
import type { Car, FilterOption, CarTypeFilterOption } from '~/utils/types/fleet'

export type OpenState = {
    category: boolean
    price: boolean
    transmission: boolean
    fuel: boolean
    seats: boolean
    features: boolean
}

const loading = ref(false)

const fleet = ref<Car[]>([])

const count = ref(0)

const nextPage = ref<string | null>(null)
const previousPage = ref<string | null>(null)

const currentPage = ref(1)

//Selected filters
const search = ref("")
const selectedCarType = ref<number[]>([])
const selectedTransmission = ref<string[]>([])
const selectedSeat = ref<string[]>([])
const selectedFuel = ref<string[]>([])
const selectedFeature = ref<string[]>([])
const selectedStatus = ref("")

const brand = ref("")
const maxPrice = ref(4700)

//All filters from the backend to be displayed in the sidebar
const carTypeOptions = ref<CarTypeFilterOption[]>([])
const transmissionOptions = ref<FilterOption[]>([])
const seatOptions = ref<FilterOption[]>([])
const fuelTypeOptions = ref<FilterOption[]>([])
const featureOptions = ref<FilterOption[]>([])

const totalCars = ref(0)
const rentedCount = ref(0)
const availableCount = ref(0)
const unavailableCount = ref(0)
const maintenanceCount = ref(0)
const pendingApprovalCount = ref(0)

export function useFleetList(prioritizeAvailable = false) {
    const { fetchFleet, fetchFleetStats } = useFleet()

    const showFilters = ref(false)
    const sortBy = ref('')

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

    const pageSize = 9

    const totalPages = computed(() =>
        Math.ceil(count.value / pageSize)
    )
    
    const fetchCars = async () => {
        loading.value = true
        console.log("selectedStatus:", selectedStatus.value)
        console.log('Car type filter:', selectedCarType.value)
        console.log('Selected car type in parent:', selectedCarType.value)

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
                status: selectedStatus.value,
                prioritize_available: prioritizeAvailable,
            })

            fleet.value = res.results

            count.value = res.count

            carTypeOptions.value = res.filters.categories

            console.log('Car type options:', carTypeOptions.value)
            console.log('Car type ID:', fleet.value[0]?.car_type)

            transmissionOptions.value = res.filters.transmissions
            seatOptions.value = res.filters.seats
            fuelTypeOptions.value = res.filters.fuel

            console.log('feature options:', featureOptions.value)
            console.log('Filters:', res.filters)

            featureOptions.value = res.filters.features

            nextPage.value = res.next ?? null
            previousPage.value = res.previous ?? null

        } finally {
            loading.value = false
        }
    }

    const fetchStats = async () => {
        const stats = await fetchFleetStats()

        rentedCount.value = stats.rented_count
        availableCount.value = stats.available_count
        unavailableCount.value = stats.unavailable_count
        maintenanceCount.value = stats.maintenance_count
        pendingApprovalCount.value = stats.pending_approval_count
        totalCars.value = stats.total_cars
    }

    watch(
        [currentPage, search, selectedCarType, selectedTransmission, selectedSeat, selectedStatus, selectedFuel, selectedFeature, maxPrice,
            sortBy
        ],
        () => {
            fetchCars()
        }
    )

    watch(sortBy, (value) => {
        console.log("sortBy changed:", value)
    })

    watch([selectedCarType, selectedTransmission, selectedFuel, selectedSeat, selectedFeature, selectedStatus, maxPrice, sortBy], () => {
        currentPage.value = 1
    })

    const resetFilters = async () => {
        search.value = ""
        selectedCarType.value = []
        selectedTransmission.value = []
        selectedSeat.value = []
        selectedFeature.value = []
        selectedFuel.value = []
        selectedStatus.value = ""
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
        pageSize,

        selectedCarType,
        selectedTransmission,
        selectedSeat,
        selectedFuel,
        selectedFeature,
        selectedStatus,

        carTypeOptions,
        transmissionOptions,
        seatOptions,
        fuelTypeOptions,
        featureOptions,

        fetchCars,
        totalPages,
        resetFilters,

        fetchStats,
        totalCars,
        availableCount,
        unavailableCount,
        maintenanceCount,
        pendingApprovalCount,
        rentedCount,

        open,
        toggleSection,
    }
}
