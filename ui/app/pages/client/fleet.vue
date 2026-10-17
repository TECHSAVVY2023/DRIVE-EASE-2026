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
        :auth-ready="authReady"
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
                :show-filters="showFilters"
                :open="open"

                :carTypeOptions="carTypeOptions"
                :selectedCarTypes="selectedCarType"
                @update:selectedCarTypes="selectedCarType = $event"

                :selectedTransmission="selectedTransmission"
                :transmissionOptions="transmissionOptions"
                @update:selectedTransmission="selectedTransmission = $event"

                :selectedFuel="selectedFuel"
                :fuelTypesOptions="fuelTypeOptions"
                @update:selectedFuel="selectedFuel = $event"

                :selectedSeat="selectedSeat"
                :seatOptions="seatOptions"
                @update:selectedSeat="selectedSeat = $event"

                :selectedFeature="selectedFeature"
                :featureOptions="featureOptions"
                @update:selectedFeature="selectedFeature = $event"

                :max-price="maxPrice"
                @update:max-price="maxPrice = $event"

                @toggle-section="toggleSection"
                @reset-filters="resetFilters"
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
                        @toggle-filters="toggleFilters"
                    />

                    <FleetSearch
                        :search="search"
                        @update:search="search = $event"
                    />

                </div>

                <!-- Car Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">

                    <ClientFleetCarCards
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
import { ref } from 'vue'
import type { Car } from '~/utils/api/api'

const { isLoggedIn, authReady } = useAuth()
const { apiFetch } = useApiFetch()

const router = useRouter()
const { $swal } = useNuxtApp()

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

const {
    fleet, count, currentPage, search, selectedTransmission, selectedFeature, selectedSeat,
    selectedCarType, selectedFuel, transmissionOptions, carTypeOptions, fuelTypeOptions,
    seatOptions, featureOptions, sortBy, maxPrice, fetchCars, totalPages, showFilters, resetFilters,
    open, toggleSection
} = useFleetList(true)

const showBookingModal = ref(false)
const selectedCar = ref<Car | null>(null)

const openBookingModal = async (car: Car) => {
    if (!user.value) {
        const result = await $swal.fire({
            icon: 'warning',
            title: 'Login Required',
            text: 'You need to log in before booking a vehicle.',
            showCancelButton: true,
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
            confirmButtonText: 'Login',
            cancelButtonText: 'Cancel',
        })

        if (result.isConfirmed) {
            await router.push('/client/login')
        }

        return
    }

    selectedCar.value = car
    showBookingModal.value = true
}

const toggleFilters = () => {
    showFilters.value = !showFilters.value
}


onMounted(async () => {
    await fetchCars()
})

</script>