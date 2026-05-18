<template>
    <div class="min-h-screen bg-[#121212] font-[poppins]">

        <MobileDrawer
            :menu-open="menuOpen"
            @close-menu="closeMenu"
        />
        <Navbar
            :menu-open="menuOpen"
            @toggle-menu="toggleMenu"
        />

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
                :price-range="priceRange"
                :filters="filters"
                :open="open"
                :transmissions="transmissions"
                :categories="categories"
                :fuel-types="fuelTypes"
                :seat-options="seatOptions"
                :feature-options="featureOptions"
                :insurance-options="insuranceOptions"
                @toggle-section="toggleSection"
                @reset-filters="resetFilters"
            />

            <!-- =========================
                    Main Content
            ========================== -->
            <div class="flex-1 flex flex-col gap-5 bg-[#1a1a1a] rounded-xl px-12 py-8">

                <!-- Results Header -->
                <div>
                    <h2 class="text-white font-bold text-lg">
                        Explore Our Fleet
                    </h2>

                    <p class="text-gray-400 text-xs mt-0.5">
                        {{ filteredCars.length }} cars available
                    </p>
                </div>

                <!-- =========================
                        Sort + Search
                ========================== -->
                <div class="flex flex-col justify-between md:flex-row md:items-center gap-3 w-full">

                    <div class="flex flex-col sm:flex-row gap-3 w-full">

                        <!-- Sort -->
                        <div class="relative w-full md:w-54">

                            <select
                                v-model="sortBy"
                                class=" w-full
                                    bg-[#262626] border border-[#2a2a2a] rounded-lg
                                    text-[#929292] text-sm px-4 py-2.5 pr-10
                                    appearance-none focus:outline-none focus:border-[#C1121F]
                                    cursor-pointer transition-colors duration-200
                                "
                            >
                                <option value="">Sort: None</option>
                                <option value="price-asc">Price: Low to High</option>
                                <option value="price-desc">Price: High to Low</option>
                                <option value="name">Name A–Z</option>
                            </select>

                            <svg
                                class="w-4 h-4 text-[#929292] absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M19 9l-7 7-7-7"
                                />
                            </svg>

                        </div>

                        <!-- Mobile Filter Toggle -->
                        <div class="md:hidden w-full">

                            <button
                                @click="showFilters = !showFilters"
                                class="
                                    flex items-center justify-center gap-2
                                    w-full bg-[#1a1a1a] border border-white rounded-lg
                                    text-white text-sm px-4 py-2.5
                                    transition-colors duration-200
                                    hover:bg-[#252525]
                                "
                            >
                                <svg
                                    class="w-4 h-4"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2a1 1 0 01-.293.707L13 13.414V19a1 1 0 01-.553.894l-4 2A1 1 0 017 21v-7.586L3.293 6.707A1 1 0 013 6V4z"
                                    />
                                </svg>

                                {{ showFilters ? 'Hide Filters' : 'Show Filters' }}
                            </button>

                        </div>

                    </div>

                    <!-- Search -->
                    <div class="relative w-full md:max-w-sm">

                        <input
                            v-model="search"
                            type="text"
                            placeholder="Search"
                            class="
                                w-full bg-[#262626] border border-[#2a2a2a] px-4 py-2.5 pr-10 rounded-lg
                                text-white text-sm
                                focus:outline-none focus:border-[#C1121F] placeholder-[#929292]
                                transition-colors duration-200
                            "
                        />

                        <svg
                            class="w-4 h-4 text-[#929292] absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                            />
                        </svg>

                    </div>

                </div>

                <!-- Car Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">

                    <div
                        v-for="(car, i) in paginatedCars"
                        :key="i"
                        class="bg-[#1a1a1a] rounded-xl overflow-hidden border border-[#222] hover:border-[#C1121F] transition-colors duration-200 flex flex-col"
                    >
                        <!-- Car Image -->
                        <div class="bg-[#141414] h-40 flex items-center justify-center overflow-hidden">
                            <img :src="car.image" :alt="car.name" class="w-full h-full object-cover" />
                        </div>

                        <!-- Info -->
                        <div class="p-4 flex flex-col gap-3 flex-1">

                            <div>
                                <h3 class="text-white font-bold text-sm">{{ car.name }}</h3>
                                <p class="text-gray-400 text-xs mt-0.5">{{ car.seats }} seats · {{ car.transmission }}</p>
                            </div>

                            <p class="text-white font-bold text-sm">₱{{ car.price.toLocaleString() }}/day</p>

                            <div class="flex flex-col gap-2 mt-auto">
                                <button class="w-full bg-[#C1121F] hover:bg-[#6B0A10] text-white text-xs font-semibold py-2 rounded-lg transition-colors duration-200">
                                    Book
                                </button>
                                <button class="w-full border border-white hover:bg-white text-white text-xs font-semibold hover:text-[#C1121F] py-2 rounded-lg transition-colors duration-200">
                                    View
                                </button>
                            </div>

                        </div>
                    </div>

                </div>

                <!-- Empty state -->
                <div v-if="filteredCars.length === 0" class="flex flex-col items-center justify-center py-20 gap-3">

                    <svg class="w-10 h-10 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <p class="text-gray-500 text-sm">No cars match your filters.</p>
                    <button @click="resetFilters" class="text-[#C1121F] text-xs hover:underline">Reset filters</button>
                
                </div>

                <!-- Pagination -->
                <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 mt-4">
                    <button
                        @click="currentPage--"
                        :disabled="currentPage === 1"
                        class="
                            flex items-center gap-1
                            rounded-lg border border-[#2a2a2a]
                            px-3 py-1.5 text-xs text-gray-400 
                            hover:border-white hover:text-white 
                            disabled:opacity-30 disabled:cursor-not-allowed 
                            transition-colors duration-200"
                    >
                        <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
                        Previous
                    </button>

                    <template v-for="p in totalPages" :key="p">
                        <button
                        @click="currentPage = p"
                        class="w-8 h-8 rounded-lg text-xs font-semibold transition-colors duration-200"
                        :class="currentPage === p ? 'bg-[#C1121F] text-white' : 'border border-[#2a2a2a] text-gray-400 hover:border-white hover:text-white'"
                        >
                        {{ p }}
                        </button>
                    </template>

                    <button
                        @click="currentPage++"
                        :disabled="currentPage === totalPages"
                        class="
                            flex items-center gap-1
                            rounded-lg border border-[#2a2a2a]
                            px-3 py-1.5 text-xs text-gray-400 
                            hover:border-white hover:text-white 
                            disabled:opacity-30 disabled:cursor-not-allowed 
                            transition-colors duration-200"
                    >
                        Next
                        <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                    </button>

                </div>

            </div>

        </div>

        <Footer />

    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const menuOpen = ref(false)

const toggleMenu = () => {
    menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
    menuOpen.value = false
}

const {
    showFilters,
    search,
    sortBy,
    currentPage,
    priceRange,
    filters,
    open,
    categories,
    transmissions,
    fuelTypes,
    seatOptions,
    featureOptions,
    insuranceOptions,
    filteredCars,
    totalPages,
    paginatedCars,
    toggleSection,
    resetFilters,
} = useCarFilters()

</script>