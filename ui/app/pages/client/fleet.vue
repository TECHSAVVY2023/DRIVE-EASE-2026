<template>
    <ClientBookingModal
        v-model="showBookingModal"
        :car="selectedCar"
        :user="user"
    />

    <MobileDrawer
        :menu-open="menuOpen"
        @close-menu="closeMenu"
    />

    <Navbar
        :user="user"
        :is-logged-in="isLoggedIn"
        :menu-open="menuOpen"
        @toggle-menu="toggleMenu"
        @open-sidebar="handleOpenSidebar" 
        @close-sidebar="handleCloseSidebar"
    />

    <div class="min-h-screen bg-[#121212] font-[poppins]">

        <Banner 
            subtitle="Find Your Perfect Ride"
            title="Our Fleet"
            :breadcrumbs="[
                { label: 'Home', to: '/' },
                { label: 'Fleet' }
            ]"
        />

        <div class="max-w-7xl px-4 py-8 flex flex-col mx-auto md:flex-row gap-6">

            <SidebarFilters
                :show-filters="filterState.showFilters.value"
                :filters="filterState.filters"
                :open="filterState.open"
                
                :carTypeOptions="carTypeOptions"
                :selectedCarTypes="selectedCarType"
                @update:selectedCarTypes="selectedCarType = $event"

                :selectedTransmission="selectedTransmission"
                :transmissionOptions="transmissionOptions"
                @update:selectedTransmission="selectedTransmission = $event"

                :selectedSeat="selectedSeat"
                :seatOptions="seatOptions"
                @update:selectedSeat="selectedSeat = $event"

                :max-price="maxPrice"
                @update:max-price="maxPrice = $event"

                :fuel-types="fuelTypes"
                :feature-options="featureOptions"
                @toggle-section="filterState.toggleSection"
                @reset-filters="filterState.resetFilters"
            />

            <!-- =========================
                    Main Content
            ========================== -->
            <div class="flex-1 flex flex-col gap-5 bg-[#1a1a1a] rounded-xl px-12 py-8">

                <!-- Results Header -->
                <div>
                    <h2 class="text-white font-bold text-xl">
                        Explore Our Fleet
                    </h2>

                    <p class="text-[#7E7E7E] text-xs mt-0.5">
                        {{ count }} cars available
                    </p>
                </div>

                <!-- =========================
                        Sort + Search
                ========================== -->
                <div class="flex flex-col justify-between md:flex-row md:items-center gap-3 w-full">

                    <FleetSort
                        :sort-by="sortBy"
                        :show-filters="showFilters"
                        @update:sortBy="sortBy = $event"
                        @toggleFilters="showFilters = !showFilters"
                    />

                    <FleetSearch
                        :search="search"
                        @update:search="search = $event"
                    />

                </div>

                <!-- Car Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">

                    <CarCards
                        :paginated-cars="fleet"
                        @book="openBookingModal"
                    />

                </div>

                <ClientCommonEmptyState
                    v-if="fleet.length === 0"
                    message="No cars match your filters."
                    button-text="Reset filters"
                    @action="resetFilters"
                />

                <Pagination
                    v-model:currentPage="currentPage"
                    :totalPages="totalPages"
                />

            </div>

        </div>

        <Footer />

    </div>
</template>

<script setup lang="ts">
import type { Car } from '~/utils/api/api'
import { type FleetResponse } from '~/utils/api/api'

const { isLoggedIn } = useAuth()
const { apiFetch } = useApiFetch()

const user = ref<any>(null)

watch(isLoggedIn, async (val) => {
    if (val) {
        user.value = await apiFetch('/auth/me/')
    } else {
        user.value = null
    }
}, { immediate: true })

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

/* ✅ SINGLE SOURCE OF TRUTH */
const filterState = useCarFilters()

/* cars */
const { cars } = useCars()

/* filtered logic */
const { paginatedCars, filteredCars } =
    useFilteredCars(cars, filterState)

/* options */
const {
    fuelTypes,
    featureOptions
} = useCarOptions(cars)

const { 
    fleet, count, currentPage, search, selectedTransmission, selectedSeat, selectedCarType, 
    transmissionOptions, carTypeOptions, seatOptions, sortBy, maxPrice, fetchCars, totalPages, showFilters
} = useFleetList()

const { resetFilters } = useFiltersCar()

const showBookingModal = ref(false)
const selectedCar = ref<Car | null>(null)

const openBookingModal = (car: Car) => {
    selectedCar.value = car
    showBookingModal.value = true
}

onMounted(async () => {
    await fetchCars()
})

</script>