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
                    v-for="cat in props.carTypeOptions" 
                    :key="cat.label" 
                    class="flex items-center justify-between cursor-pointer group rounded-md py-1 px-3 transition-all duration-200 ease-in-out"
                    :class="props.selectedCarTypes.includes(cat.label) ? 'bg-[#252525] border-l-4 border-[#C1121F]' : 'border-transparent'"
                    @click="
                        emit(
                            'update:selectedCarTypes',
                            props.selectedCarTypes.includes(cat.label)
                                ? props.selectedCarTypes.filter(c => c !== cat.label)
                                : [...props.selectedCarTypes, cat.label]
                        )
                    "
                >

                    <div class="flex items-center gap-2">
                        <span
                            class="text-xs transition-colors duration-200 cursor-pointer"
                            :class="props.selectedCarTypes.includes(cat.label) ? 'text-white font-semibold' : 'text-[#7E7E7E] group-hover:text-white'"
                        >{{ cat.label.charAt(0).toUpperCase() + cat.label.slice(1) }}</span>
                    </div>

                    <span
                        class="text-xs font-bold px-1.5 py-0.5 rounded-full"
                        :class="props.selectedCarTypes.includes(cat.label) ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-[#7E7E7E]'"
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
                    <span>₱100</span>
                    <span>₱{{ maxPrice }}</span>
                </div>

                <input
                    type="range"
                    min="100"
                    max="4700"
                    step="100"
                    v-model.number="maxPrice"
                    class="w-full accent-[#C1121F] cursor-pointer"
                />

                <p class="text-[#7E7E7E] text-[12px]">
                    Up to ₱{{ maxPrice }}
                </p>

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
                    v-for="t in transmissionOptions"
                    :key="t.label" 
                    class="flex items-center justify-between cursor-pointer group py-1 px-3 rounded-md transition-all duration-200 ease-in-out"
                    :class="props.selectedTransmission.includes(t.label) ? 'bg-[#252525] border-l-4 border-[#C1121F]' : 'border-transparent'"
                    @click="
                        emit(
                            'update:selectedTransmission',
                            props.selectedTransmission.includes(t.label)
                                ? props.selectedTransmission.filter(c => c !== t.label)
                                : [...props.selectedTransmission, t.label]
                        )
                    "
                >

                    <div class="flex items-center gap-2">
                        <span 
                            class="text-xs transition-colors duration-200 cursor-pointer" 
                            :class="props.selectedTransmission.includes(t.label) ? 'text-white font-semibold' : 'text-[#7E7E7E] group-hover:text-white'" 
                        >{{ t.label.charAt(0).toUpperCase() + t.label.slice(1) }}</span>
                    </div>
                    <span 
                        class="text-[10px] font-bold px-1.5 py-0.5 rounded-full" 
                        :class="props.selectedTransmission.includes(t.label) ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-[#7E7E7E]'"
                    >{{ t.count }}</span>
                
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

                <label v-for="f in fuelTypesOptions" 
                    :key="f.label" 
                    class="flex items-center justify-between cursor-pointer group py-1 px-3 rounded-md transition-all duration-200 ease-in-out"
                    :class="props.selectedFuel.includes(f.label) ? 'bg-[#252525] border-l-4 border-[#C1121F]' : 'border-transparent'" 
                    @click="
                        emit(
                            'update:selectedFuel',
                            props.selectedFuel.includes(f.label)
                                ? props.selectedFuel.filter(c => c !== f.label)
                                : [...props.selectedFuel, f.label]
                        )
                    "
                >
                    
                    <div class="flex items-center gap-2">
                        <span 
                            class="text-xs transition-colors duration-200 cursor-pointer" 
                            :class="props.selectedFuel.includes(f.label) ? 'text-white font-semibold' : 'text-[#7E7E7E] group-hover:text-white'" 
                            >{{ f.label.charAt(0).toUpperCase() + f.label.slice(1) }}</span>
                    </div>
                    <span 
                        class="text-[10px] font-bold px-1.5 py-0.5 rounded-full" 
                        :class="props.selectedFuel.includes(f.label) ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-[#7E7E7E]'">{{ f.count }}</span>
                
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
                    :class="props.selectedSeat.includes(s.label) ? 'bg-[#252525] border-l-4 border-[#C1121F]' : 'border-transparent'"
                    @click="
                        emit(
                            'update:selectedSeat',
                            props.selectedSeat.includes(s.label)
                                ? props.selectedSeat.filter(c => c !== s.label)
                                : [...props.selectedSeat, s.label]
                        )
                    "
                >

                    <div class="flex items-center gap-2">

                        <span class="text-xs transition-colors duration-200 cursor-pointer" 
                            :class="props.selectedSeat.includes(s.label) ?'text-white font-semibold' : 'text-[#7E7E7E] group-hover:text-white'" 
                        >{{ s.label }} Seats </span>

                    </div>

                    <span 
                        class="text-[10px] font-bold px-1.5 py-0.5 rounded-full" 
                        :class="props.selectedSeat.includes(s.label) ? 'bg-[#C1121F] text-white' : 'bg-[#2a2a2a] text-[#7E7E7E]'">{{ s.count }}</span>
                
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
                    :class="props.selectedFeature.includes(f.label) ? 'bg-[#252525] border-l-4 border-[#C1121F]' : 'border-transparent'"
                    @click="
                        emit(
                            'update:selectedFeature',
                            props.selectedFeature.includes(f.label)
                                ? props.selectedFeature.filter(c => c !== f.label)
                                : [...props.selectedFeature, f.label]
                        )
                    "
                >
                <div class="flex items-center gap-2">

                    <span class="text-xs transition-colors duration-200 cursor-pointer" 
                        :class="props.selectedFeature.includes(f.label)
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

    const props = defineProps<{
        showFilters: boolean
        maxPrice: number
        selectedCarTypes: string[]
        selectedTransmission: string[]
        selectedSeat: string[]
        selectedFuel: string[]
        selectedFeature: string[]
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
        transmissionOptions: { label: string; count: number }[]
        carTypeOptions: { label: string; count: number }[]
        fuelTypesOptions: { label: string; count: number }[]
        seatOptions: { label: string; count: number }[]
        featureOptions: { label: string; count: number }[]
    }>()

    const emit = defineEmits<{
        toggleSection: [key: 'category' | 'price' | 'transmission' | 'fuel' | 'seats' | 'features']
        resetFilters: []
        'update:selectedCarTypes': [value: string[]]
        'update:selectedTransmission': [value: string[]]
        'update:selectedSeat': [value: string[]]
        'update:selectedFuel': [value: string[]]
        'update:selectedFeature': [value: string[]]
        'update:maxPrice': [value: number]
    }>()

    const toggleSection = (key: 'category' | 'price' | 'transmission' | 'fuel' | 'seats' | 'features') => emit('toggleSection', key)
    
    const resetFilters = () => emit('resetFilters')

    const maxPrice = computed({
        get: () => props.maxPrice,
        set: (value: number) => emit('update:maxPrice', value),
    })
</script>