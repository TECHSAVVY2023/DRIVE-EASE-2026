<template>
    <BookCarModal
        v-if="selectedCar"
        v-model="showBookingModal"
        :car="selectedCar"
    />

    <MobileDrawer
        :menu-open="menuOpen"
        @close-menu="closeMenu"
    />

    <Navbar
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
                :price-range="filterState.priceRange.value"
                :filters="filterState.filters"
                :open="filterState.open"
                :transmissions="transmissions"
                :categories="categories"
                :fuel-types="fuelTypes"
                :seat-options="seatOptions"
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
                        {{ filteredCars.length }} cars available
                    </p>
                </div>

                <!-- =========================
                        Sort + Search
                ========================== -->
                <div class="flex flex-col justify-between md:flex-row md:items-center gap-3 w-full">

                    <FleetSort
                        :sort-by="filterState.sortBy.value"
                        :show-filters="filterState.showFilters.value"
                        @update:sortBy="filterState.sortBy.value = $event"
                        @toggleFilters="filterState.showFilters.value = !filterState.showFilters.value"
                    />

                    <FleetSearch
                        :search="filterState.search.value"
                        @update:search="filterState.search.value = $event"
                    />

                </div>

                <!-- Car Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">

                    <NuxtLink
                        v-for="car in paginatedCars"
                        :key="car.car_id"
                        :to="`/car-details/${car.car_id}`"
                        class="
                            bg-[#1a1a1a] rounded-xl border border-[#222] hover:border-[#C1121F]
                            transition-colors duration-200 flex flex-col overflow-hidden"
                    >
                        <!-- Car Image -->
                        <div class="bg-[#141414] h-40 flex items-center justify-center overflow-hidden">
                            <img :src="`${useApiBase()}${getPrimaryImage(car)}`" class="w-full h-full object-cover" />
                        </div>

                        <!-- Info -->
                        <div class="p-4 flex flex-col gap-3 flex-1">

                            <div>
                                <h3 class="text-white font-bold text-sm">{{ car.brand }} {{ car.model }}</h3>
                                <p class="text-[#7E7E7E] text-xs mt-0.5">{{ car.seats }} seats · {{ car.transmission }}</p>
                            </div>

                            <p class="text-white font-bold text-sm">₱{{ car.price_per_day.toLocaleString() }}/day</p>

                            <div class="flex flex-col gap-2 mt-auto">

                                <button 
                                    @click.stop.prevent="openBookingModal(car)"
                                    class="
                                        w-full bg-[#C1121F] hover:bg-[#9B0E18] py-2 
                                        text-white text-xs font-semibold
                                        rounded-lg transition-colors duration-200
                                    "
                                >
                                    Book
                                </button>

                                <button class="
                                    w-full border border-white hover:bg-white rounded-lg
                                    text-white text-xs font-semibold hover:text-[#C1121F] py-2
                                    transition-colors duration-200
                                    "
                                >
                                    View
                                </button>

                            </div>

                        </div>
                    </NuxtLink>

                </div>

                <!-- Empty state -->
                <EmptyState
                    v-if="filteredCars.length === 0"
                    message="No cars match your filters."
                    button-text="Reset filters"
                    @action="filterState.resetFilters"
                />

                <Pagination
                    v-model:currentPage="filterState.currentPage.value"
                    :totalPages="totalPages"
                />

            </div>

        </div>

        <Footer />

    </div>
</template>

<script setup lang="ts">
import { useApiBase, getPrimaryImage } from '~/utils/api/api'


const { setAuth } = useAuth()
const route = useRoute()

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

if (route.query.token) {
    await setAuth(route.query.token as string)
}

/* ✅ SINGLE SOURCE OF TRUTH */
const filterState = useCarFilters()

/* cars */
const { cars } = useCars()

/* filtered logic */
const { totalPages, paginatedCars, filteredCars } =
    useFilteredCars(cars, filterState)

/* options */
const {
    categories,
    transmissions,
    fuelTypes,
    seatOptions,
    featureOptions
} = useCarOptions(cars)


const showBookingModal = ref(false)
const selectedCar = ref(null)

const openBookingModal = (car: any) => {
    selectedCar.value = car
    showBookingModal.value = true
}

</script>