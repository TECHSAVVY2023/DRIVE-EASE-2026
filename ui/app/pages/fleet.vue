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

        <Banner1 />

        <div class="max-w-7xl px-4 py-8 flex flex-col mx-auto md:flex-row gap-6">

            <!-- Mobile Filter Toggle -->
            <div class="md:hidden">
                <button
                @click="showFilters = !showFilters"
                class="flex items-center gap-2 bg-[#1a1a1a] border border-[#2a2a2a] text-white text-sm px-4 py-2.5 rounded-lg w-full justify-center"
                >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2a1 1 0 01-.293.707L13 13.414V19a1 1 0 01-.553.894l-4 2A1 1 0 017 21v-7.586L3.293 6.707A1 1 0 013 6V4z"/>
                </svg>
                {{ showFilters ? 'Hide Filters' : 'Show Filters' }}
                </button>
            </div>

            <!-- Sidebar Filters -->
            <aside
                class="w-full h-fit flex flex-col bg-[#1B1B1B] rounded-xl pb-20 md:w-48 lg:w-64 flex-shrink-0"
                :class="showFilters ? 'block' : 'hidden md:flex'"
            >
                <!-- Header -->
                <div class="flex items-center justify-between px-5 py-8">
                    <span class="text-white font-bold text-sm">Filter by</span>
                    <button @click="resetFilters" class="text-[#C1121F] text-xs hover:underline">Reset all</button>
                </div>

                <div class="border-t border-[#3F3F3F]"></div>

                <!-- Category -->
                <div class="flex flex-col">

                    <button @click="toggleSection('category')" class="flex items-center justify-between w-full px-5 py-4">
                        
                        <span class="text-white text-xs font-semibold">Category</span>
                        <svg class="w-4 h-4 text-gray-400 transition-transform duration-200" :class="open.category ? '' : 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                        </svg>

                    </button>

                    <div v-if="open.category" class="flex flex-col gap-1 px-5 pb-4">

                        <label 
                            v-for="cat in categories" 
                            :key="cat.label" 
                            class="flex items-center justify-between cursor-pointer group rounded-md py-1 px-3 transition-all duration-200 ease-in-out"
                            :class="filters.category.includes(cat.label) ? 'bg-[#252525] border-l-4 border-[#C1121F]' : ''"
                            @click="filters.category = filters.category.includes(cat.label) ? filters.category.filter(c => c !== cat.label) : [...filters.category, cat.label]"
                        >

                            <div class="flex items-center gap-2">
                                <span
                                    class="text-xs transition-colors duration-200 cursor-pointer"
                                    :class="filters.category.includes(cat.label) ? 'text-white font-semibold' : 'text-gray-400 group-hover:text-white'"
                                >{{ cat.label }}</span>
                            </div>

                            <span
                                class="text-[10px] font-bold px-1.5 py-0.5 rounded-full"
                                :class="filters.category.includes(cat.label) ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-gray-400'"
                            >{{ cat.count }}</span>
                        </label>

                    </div>

                </div>

                <div class="border-t border-[#3F3F3F]"></div>

                <!-- Price Range -->
                <div class="flex flex-col">

                    <button @click="toggleSection('price')" class="flex items-center justify-between w-full px-5 py-4">
                        
                        <span class="text-white text-xs font-semibold">Price range</span>
                        <svg class="w-4 h-4 text-gray-400 transition-transform duration-200" :class="open.price ? '' : 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                        </svg>

                    </button>

                    <div v-if="open.price" class="flex flex-col gap-2 px-5 pb-4">
                        <div class="flex justify-between text-[10px] text-gray-400">
                        <span>₱{{ priceRange[0] }}</span>
                        <span>₱{{ priceRange[1] }}</span>
                        </div>
                        <input type="range" min="100" max="4700" v-model="priceRange[1]" class="w-full accent-[#C1121F] cursor-pointer" />
                        <p class="text-gray-500 text-[10px]">₱{{ priceRange[0] }} – ₱{{ priceRange[1] }}</p>
                    </div>

                </div>

                <div class="border-t border-[#3F3F3F]"></div>   

                <!-- Transmission -->
                <div class="flex flex-col">

                    <button @click="toggleSection('transmission')" class="flex items-center justify-between w-full px-5 py-4">
                        
                        <span class="text-white text-xs font-semibold">Transmission</span>
                        <svg class="w-4 h-4 text-gray-400 transition-transform duration-200" :class="open.transmission ? '' : 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                        </svg>

                    </button>

                    <div v-if="open.transmission" class="flex flex-col px-5 pb-4">
                        
                        <label 
                            v-for="t in transmissions"
                            :key="t.label" 
                            class="flex items-center justify-between cursor-pointer group py-1 px-3 rounded-md transition-all duration-200 ease-in-out"
                            :class="filters.transmission === t.label ? 'bg-[#252525] border-l-4 border-[#C1121F]' : ''"
                            @click="filters.transmission = filters.transmission === t.label ? '' : t.label"
                        >

                            <div class="flex items-center gap-2">
                                <span 
                                    class="text-xs transition-colors duration-200 cursor-pointer" 
                                    :class="filters.transmission === t.label ? 'text-white font-semibold' : 'text-gray-400 group-hover:text-white'" 
                                >{{ t.label }}</span>
                            </div>
                            <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-full" :class="filters.transmission === t.label ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-gray-400'">{{ t.count }}</span>
                        
                        </label>

                    </div>
                </div>

                <div class="border-t border-[#3F3F3F]"></div>

                <!-- Fuel Type -->
                <div class="flex flex-col">
                    
                    <button @click="toggleSection('fuel')" class="flex items-center justify-between w-full px-5 py-4">
                        
                        <span class="text-white text-xs font-semibold">Fuel type</span>
                        <svg class="w-4 h-4 text-gray-400 transition-transform duration-200" :class="open.fuel ? '' : 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                        </svg>

                    </button>

                    <div v-if="open.fuel" class="flex flex-col px-5 pb-4">

                        <label v-for="f in fuelTypes" 
                            :key="f.label" 
                            class="flex items-center justify-between cursor-pointer group py-1 px-3 rounded-md transition-all duration-200 ease-in-out"
                            :class="filters.fuel === f.label ? 'bg-[#252525] border-l-4 border-[#C1121F]' : ''" 
                            @click="filters.fuel = filters.fuel === f.label ? '' : f.label"
                        >
                            
                            <div class="flex items-center gap-2">
                                <span 
                                    class="text-xs transition-colors duration-200 cursor-pointer" 
                                    :class="filters.fuel === f.label ? 'text-white font-semibold' : 'text-gray-400 group-hover:text-white'" 
                                    >{{ f.label }}</span>
                            </div>
                            <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-full" :class="filters.fuel === f.label ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-gray-400'">{{ f.count }}</span>
                        
                        </label>

                    </div>

                </div>

                <div class="border-t border-[#3F3F3F]"></div>

                <!-- Seats -->
                <div class="flex flex-col">

                    <button @click="toggleSection('seats')" class="flex items-center justify-between w-full px-5 py-4">
                        
                        <span class="text-white text-xs font-semibold">Seats</span>
                        <svg class="w-4 h-4 text-gray-400 transition-transform duration-200" :class="open.seats ? '' : 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                        </svg>
                    
                    </button>

                    <div v-if="open.seats" class="flex flex-col px-5 pb-4">
                        
                        <label v-for="s in seatOptions" 
                            :key="s.label" 
                            class="flex items-center justify-between cursor-pointer group py-1 px-3 rounded-md transition-all duration-200 ease-in-out"
                            :class="filters.seats === s.label ? 'bg-[#252525] border-l-4 border-[#C1121F]' : ''"
                            @click="filters.seats = filters.seats === s.label ? '' : s.label" 
                        >

                            <div class="flex items-center gap-2">

                                <span class="text-xs transition-colors duration-200 cursor-pointer" 
                                    :class="filters.seats === s.label ? 'text-white font-semibold' : 'text-gray-400 group-hover:text-white'" 
                                >{{ s.label }}</span>

                            </div>

                            <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-full" :class="filters.seats === s.label ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-gray-400'">{{ s.count }}</span>
                        
                        </label>

                    </div>
                </div>

                <div class="border-t border-[#3F3F3F]"></div>

                <!-- Features -->
                <div class="flex flex-col">

                    <button @click="toggleSection('features')" class="flex items-center justify-between w-full px-5 py-4">
                        
                        <span class="text-white text-xs font-semibold">Features</span>

                        <svg class="w-4 h-4 text-gray-400 transition-transform duration-200" :class="open.features ? '' : 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                        </svg>
                    
                    </button>

                    <div v-if="open.features" class="flex flex-col px-5 pb-4">

                        <label 
                            v-for="f in featureOptions" :key="f.label" 
                            class="flex items-center justify-between cursor-pointer group py-1 px-3 rounded-md transition-all duration-200 ease-in-out"
                            :class="filters.feature === f.label ? 'bg-[#252525] border-l-4 border-[#C1121F]' : ''"
                            @click="filters.feature = filters.feature === f.label ? '' : f.label"
                        >
                        <div class="flex items-center gap-2">

                            <span class="text-xs transition-colors duration-200 cursor-pointer" 
                                :class="filters.feature === f.label ? 'text-white font-semibold' : 'text-gray-400 group-hover:text-white'" 
                            >{{ f.label }}</span>

                        </div>
                            <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-full" :class="filters.feature === f.label ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-gray-400'">{{ f.count }}</span>
                        </label>
                    
                    </div>

                </div>

                <div class="border-t border-[#3F3F3F]"></div>

                <!-- Insurance -->
                <div class="flex flex-col">
                    
                    <button @click="toggleSection('insurance')" class="flex items-center justify-between w-full px-5 py-4">
                        
                        <span class="text-white text-xs font-semibold">Insurance?</span>
                        <svg class="w-4 h-4 text-gray-400 transition-transform duration-200" :class="open.insurance ? '' : 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                        </svg>

                    </button>

                    <div v-if="open.insurance" class="flex flex-col px-5 pb-4">

                        <label 
                            v-for="ins in insuranceOptions" 
                            :key="ins.label" 
                            class="flex items-center justify-between cursor-pointer group py-1 px-3 rounded-md transition-all duration-200 ease-in-out"
                            :class="filters.insurance === ins.label ? 'bg-[#252525] border-l-4 border-[#C1121F]' : ''"
                            @click="filters.insurance = filters.insurance === ins.label ? '' : ins.label"
                        >
                        <div class="flex items-center gap-2">
                            <span 
                                class="text-xs transition-colors duration-200 cursor-pointer" 
                                :class="filters.insurance === ins.label ? 'text-white font-semibold' : 'text-gray-400 group-hover:text-white'" 
                            >{{ ins.label }}</span>
                        </div>
                            <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-full" :class="filters.insurance === ins.label ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-gray-400'">{{ ins.count }}</span>
                        </label>
                        
                    </div>
                </div>

            </aside>

            <!-- Main Content -->
            <div class="flex-1 flex flex-col gap-5 bg-[#1a1a1a] rounded-xl px-12 py-8">

                <!-- Results Header -->
                <div>
                    <h2 class="text-white font-bold text-lg">
                        Result:
                        {{
                            search
                                ? `"${search}"`
                                : filters.category.length
                                    ? filters.category.join(', ')
                                    : 'All Cars'
                        }}
                    </h2>

                    <p class="text-gray-400 text-xs mt-0.5">
                        {{ filteredCars.length }} cars available
                    </p>
                </div>

                <!-- Sort + Search -->
                <div class="flex flex-col sm:flex-row gap-3">
                    <div class="relative">

                        <select
                            v-model="sortBy"
                            class="w-full sm:w-auto bg-[#1a1a1a] border border-[#2a2a2a] text-white text-sm px-4 py-2.5 pr-10 rounded-lg appearance-none focus:outline-none focus:border-[#C1121F] cursor-pointer transition-colors duration-200"
                        >
                            <option value="">Sort: None</option>
                            <option value="price-asc">Price: Low to High</option>
                            <option value="price-desc">Price: High to Low</option>
                            <option value="name">Name A–Z</option>
                        </select>

                        <svg
                            class="w-4 h-4 text-gray-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                        </svg>

                    </div>

                    <div class="relative flex-1">

                        <input
                        v-model="search"
                        type="text"
                        placeholder="Search"
                        class="w-full bg-[#1a1a1a] border border-[#2a2a2a] text-white text-sm px-4 py-2.5 pr-10 rounded-lg focus:outline-none focus:border-[#C1121F] placeholder-[#444] transition-colors duration-200"
                        />
                        <svg class="w-4 h-4 text-gray-400 absolute right-3 top-1/2 -translate-y-1/2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
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
                        <button class="w-full bg-[#C1121F] hover:bg-red-700 text-white text-xs font-semibold py-2 rounded-lg transition-colors duration-200">
                        Book
                        </button>
                        <button class="w-full border border-[#2a2a2a] hover:border-white text-white text-xs font-semibold py-2 rounded-lg transition-colors duration-200">
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
                    class="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs border border-[#2a2a2a] text-gray-400 hover:border-white hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors duration-200"
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
                    class="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs border border-[#2a2a2a] text-gray-400 hover:border-white hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors duration-200"
                >
                    Next
                    <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                </button>
                </div>

            </div>

        </div>

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
    perPage,
    priceRange,
    filters,
    open,
    transmissions,
    categories,
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
} = useCarFilters()

</script>