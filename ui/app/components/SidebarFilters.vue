<template>
        <!-- Sidebar Filters -->
    <aside
        class="w-full h-fit flex flex-col bg-[#1B1B1B] rounded-xl pb-20 md:w-48 lg:w-64 flex-shrink-0"
        :class="showFilters ? 'block' : 'hidden md:flex'"
    >
        <!-- Header -->
        <div class="flex items-center justify-between px-5 py-8">
            <span class="text-white font-bold">Filter by</span>
            <button @click="resetFilters" class="text-[#C1121F] text-xs hover:underline">Reset all</button>
        </div>

        <div class="border-t border-[#3F3F3F]"></div>

        <!-- Category -->
        <div class="flex flex-col">

            <button @click="toggleSection('category')" class="flex items-center justify-between w-full px-5 py-4">
                
                <span class="text-white font-semibold">Category</span>
                <svg class="w-4 h-4 text-[#7E7E7E] transition-transform duration-200" :class="open.category ? '' : 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                </svg>

            </button>

            <div v-if="open.category" class="flex flex-col gap-1 px-5 pb-4">

                <label 
                    v-for="cat in categories" 
                    :key="cat.label" 
                    class="flex items-center justify-between cursor-pointer group rounded-md py-1 px-3 transition-all duration-200 ease-in-out"
                    :class="filters.category.includes(cat.label) ? 'bg-[#252525] border-l-4 border-[#C1121F]' : 'border-transparent'"
                    @click="filters.category = filters.category.includes(cat.label) ? filters.category.filter(c => c !== cat.label) : [...filters.category, cat.label]"
                >

                    <div class="flex items-center gap-2">
                        <span
                            class="text-xs transition-colors duration-200 cursor-pointer"
                            :class="filters.category.includes(cat.label) ? 'text-white font-semibold' : 'text-[#7E7E7E] group-hover:text-white'"
                        >{{ cat.label.charAt(0).toUpperCase() + cat.label.slice(1) }}</span>
                    </div>

                    <span
                        class="text-xs font-bold px-1.5 py-0.5 rounded-full"
                        :class="filters.category.includes(cat.label) ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-[#7E7E7E]'"
                    >{{ cat.count }}</span>
                </label>

            </div>

        </div>

        <div class="border-t border-[#3F3F3F]"></div>

        <!-- Price Range -->
        <div class="flex flex-col">

            <button @click="toggleSection('price')" class="flex items-center justify-between w-full px-5 py-4">
                
                <span class="text-white font-semibold">Price range</span>
                <svg class="w-4 h-4 text-[#7E7E7E] transition-transform duration-200" :class="open.price ? '' : 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                </svg>

            </button>

            <div v-if="open.price" class="flex flex-col gap-2 px-5 pb-4">

                <div class="flex justify-between text-xs text-[#7E7E7E]">
                    <span>₱{{ priceRange[0] }}</span>
                    <span>₱{{ priceRange[1] }}</span>
                </div>

                <input type="range" min="100" max="4700" v-model="priceRange[1]" class="w-full accent-[#C1121F] cursor-pointer" />
                <p class="text-[#7E7E7E] text-[12px]">₱{{ priceRange[0] }} – ₱{{ priceRange[1] }}</p>

            </div>

        </div>

        <div class="border-t border-[#3F3F3F]"></div>   

        <!-- Transmission -->
        <div class="flex flex-col">

            <button @click="toggleSection('transmission')" class="flex items-center justify-between w-full px-5 py-4">
                
                <span class="text-white font-semibold">Transmission</span>
                <svg class="w-4 h-4 text-[#7E7E7E] transition-transform duration-200" :class="open.transmission ? '' : 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                </svg>

            </button>

            <div v-if="open.transmission" class="flex flex-col gap-1 px-5 pb-4">
                
                <label 
                    v-for="t in transmissions"
                    :key="t.label" 
                    class="flex items-center justify-between cursor-pointer group py-1 px-3 rounded-md transition-all duration-200 ease-in-out"
                    :class="filters.transmission.includes(t.label) ? 'bg-[#252525] border-l-4 border-[#C1121F]' : 'border-transparent'"
                    @click="filters.transmission = filters.transmission.includes(t.label) ? filters.transmission.filter((item) => item !== t.label) : [...filters.transmission, t.label]"
                >

                    <div class="flex items-center gap-2">
                        <span 
                            class="text-xs transition-colors duration-200 cursor-pointer" 
                            :class="filters.transmission.includes(t.label) ? 'text-white font-semibold' : 'text-[#7E7E7E] group-hover:text-white'" 
                        >{{ t.label.charAt(0).toUpperCase() + t.label.slice(1) }}</span>
                    </div>
                    <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-full" :class="filters.transmission.includes(t.label) ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-[#7E7E7E]'">{{ t.count }}</span>
                
                </label>

            </div>
        </div>

        <div class="border-t border-[#3F3F3F]"></div>

        <!-- Fuel Type -->
        <div class="flex flex-col">
            
            <button @click="toggleSection('fuel')" class="flex items-center justify-between w-full px-5 py-4">
                
                <span class="text-white text-xs font-semibold">Fuel type</span>
                <svg class="w-4 h-4 text-[#7E7E7E] transition-transform duration-200" :class="open.fuel ? '' : 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                </svg>

            </button>

            <div v-if="open.fuel" class="flex flex-col gap-1 px-5 pb-4">

                <label v-for="f in fuelTypes" 
                    :key="f.label" 
                    class="flex items-center justify-between cursor-pointer group py-1 px-3 rounded-md transition-all duration-200 ease-in-out"
                    :class="filters.fuel.includes(f.label) ? 'bg-[#252525] border-l-4 border-[#C1121F]' : 'border-transparent'" 
                    @click="filters.fuel = filters.fuel.includes(f.label) ? filters.fuel.filter((item) => item !== f.label) : [...filters.fuel, f.label]"
                >
                    
                    <div class="flex items-center gap-2">
                        <span 
                            class="text-xs transition-colors duration-200 cursor-pointer" 
                            :class="filters.fuel.includes(f.label) ? 'text-white font-semibold' : 'text-[#7E7E7E] group-hover:text-white'" 
                            >{{ f.label.charAt(0).toUpperCase() + f.label.slice(1) }}</span>
                    </div>
                    <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-full" :class="filters.fuel.includes(f.label) ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-[#7E7E7E]'">{{ f.count }}</span>
                
                </label>

            </div>

        </div>

        <div class="border-t border-[#3F3F3F]"></div>

        <!-- Seats -->
        <div class="flex flex-col">

            <button @click="toggleSection('seats')" class="flex items-center justify-between w-full px-5 py-4">
                
                <span class="text-white text-xs font-semibold">Seats</span>
                <svg class="w-4 h-4 text-[#7E7E7E] transition-transform duration-200" :class="open.seats ? '' : 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                </svg>
            
            </button>

            <div v-if="open.seats" class="flex flex-col gap-1 px-5 pb-4">
                
                <label v-for="s in seatOptions" 
                    :key="s.label" 
                    class="flex items-center justify-between cursor-pointer group py-1 px-3 rounded-md transition-all duration-200 ease-in-out"
                    :class="filters.seats.includes(s.label) ? 'bg-[#252525] border-l-4 border-[#C1121F]' : 'border-transparent'"
                    @click="filters.seats = filters.seats.includes(s.label) ? filters.seats.filter((item) => item !== s.label) : [...filters.seats, s.label]"
                >

                    <div class="flex items-center gap-2">

                        <span class="text-xs transition-colors duration-200 cursor-pointer" 
                            :class="filters.seats.includes(s.label) ? 'text-white font-semibold' : 'text-[#7E7E7E] group-hover:text-white'" 
                        >{{ s.label }}</span>

                    </div>

                    <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-full" :class="filters.seats.includes(s.label) ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-[#7E7E7E]'">{{ s.count }}</span>
                
                </label>

            </div>
        </div>

        <div class="border-t border-[#3F3F3F]"></div>

        <!-- Features -->
        <div class="flex flex-col">

            <button @click="toggleSection('features')" class="flex items-center justify-between w-full px-5 py-4">
                
                <span class="text-white text-xs font-semibold">Features</span>

                <svg class="w-4 h-4 text-[#7E7E7E] transition-transform duration-200" :class="open.features ? '' : 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                </svg>
            
            </button>

            <div v-if="open.features" class="flex flex-col gap-1 px-5 pb-4">

                <label 
                    v-for="f in featureOptions" :key="f.label" 
                    class="flex items-center justify-between cursor-pointer group py-1 px-3 rounded-md transition-all duration-200 ease-in-out"
                    :class="filters.feature.includes(f.label) ? 'bg-[#252525] border-l-4 border-[#C1121F]' : 'border-transparent'"
                    @click="filters.feature = filters.feature.includes(f.label)
                    ? filters.feature.filter(item => item !== f.label)
                    : [...filters.feature, f.label]"
                >
                <div class="flex items-center gap-2">

                    <span class="text-xs transition-colors duration-200 cursor-pointer" 
                        :class="filters.feature.includes(f.label)
                        ? 'text-white font-semibold'
                        : 'text-[#7E7E7E] group-hover:text-white'"
                    >{{ f.label.charAt(0).toUpperCase() + f.label.slice(1) }}</span>

                </div>
                    <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-full" :class="filters.seats.includes(f.label) ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-[#7E7E7E]'">{{ f.count }}</span>
                </label>
            
            </div>

        </div>

    </aside>
</template>

<script setup lang="ts">

    defineProps<{
        showFilters: boolean
        priceRange: [number, number]
        filters: {
            category: string[]
            transmission: string[]
            fuel: string[]
            seats: string[]
            feature: string[]
        }
        open: {
            category: boolean
            price: boolean
            transmission: boolean
            fuel: boolean
            seats: boolean
            features: boolean
        }
        transmissions: { label: string; count: number }[]
        categories: { label: string; count: number }[]
        fuelTypes: { label: string; count: number }[]
        seatOptions: { label: string; count: number }[]
        featureOptions: { label: string; count: number }[]
    }>()

    const emit = defineEmits<{
        toggleSection: [key: 'category' | 'price' | 'transmission' | 'fuel' | 'seats' | 'features']
        resetFilters: []
    }>()

    const toggleSection = (key: 'category' | 'price' | 'transmission' | 'fuel' | 'seats' | 'features') => emit('toggleSection', key)
    const resetFilters = () => emit('resetFilters')
</script>