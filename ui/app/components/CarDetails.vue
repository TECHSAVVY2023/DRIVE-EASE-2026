<template>
    <!-- Top Section: Images + Info -->
    <div class="flex flex-col justify-center gap-4 items-center bg-[#1B1B1B] w-full px-4 py-4 rounded-xl">
        
        <div class="flex flex-col w-full md:flex-row md:items-center gap-6">
            <!-- Left: Image Gallery -->
            <div class="flex flex-1 flex-col justify-center gap-2 w-full h-full">
                <!-- Main Image -->
                <div class="relative bg-[#1a1a1a] rounded-xl overflow-hidden aspect-[16/10] flex items-center justify-center border border-[#222]">
                    <img
                        :src="galleryImages[activeImage] as string"
                        :alt="car.model"
                        class="absolute inset-0 w-full h-full object-cover"
                    />

                    <!-- Prev -->
                    <button
                        @click="prevImage"
                        class="absolute left-3 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-black/60 hover:bg-black/80 text-white flex items-center justify-center transition-colors duration-200"
                        >
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                        </svg>
                    </button>

                    <!-- Next -->
                    <button
                        @click="nextImage"
                        class="absolute right-3 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-black/60 hover:bg-black/80 text-white flex items-center justify-center transition-colors duration-200"
                        >
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                        </svg>
                    </button>
                </div>
    
                <!-- Thumbnails -->
                <div class="flex gap-2">
                <button
                    v-for="(img, i) in galleryImages"
                    :key="i"
                    @click="activeImage = i"
                    class="w-16 h-12 rounded-lg overflow-hidden border-2 transition-colors duration-200 flex-shrink-0"
                    :class="activeImage === i ? 'border-[#C1121F]' : 'border-[#222] hover:border-[#444]'"
                >
                    <img
                    :src="img as string"
                    :alt="`Thumbnail ${i + 1}`"
                    class="w-full h-full object-cover"
                    />
                </button>
                </div>
            </div>
    
            <!-- Right: Car Info -->
            <div class="flex-1 flex flex-col w-full pt-4">

                <!-- Name + Status -->
                <div class="flex items-start justify-between gap-3">
                    <h1 class="text-white font-extrabold text-2xl leading-tight">{{ car.brand }} {{ car.model }}</h1>
                    <span class="flex items-center gap-1.5 text-xs font-semibold px-3 py-1 rounded-full flex-shrink-0"
                        :class="car.status === 'available' ? 'bg-[#123a1f] text-green-400' : 'bg-[#C1121F]/20 text-[#FF6161]'"
                    >
                        <span class="w-1.5 h-1.5 rounded-full" :class="car.status === 'available' ? 'bg-green-400' : 'bg-[#FF6161]'"></span>
                        {{ car.status === 'available' ? 'AVAILABLE' : 'UNAVAILABLE' }}
                    </span>
                </div>
    
                <!-- Rating -->
                <div class="flex items-center pt-1 gap-1.5">
                    <svg class="w-4 h-4 text-[#c1121f]" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                    </svg>
                    <span class="text-[#c1121f] text-md font-semibold">{{ props.avgRating.toFixed(1) }}</span>
                    <span class="text-[#A3A3A3] text-sm font-light">{{ props.totalReviews }} reviews</span>
                </div>
    
                <!-- Price -->
                <div class="flex items-end py-4 gap-2">
                    <span class="text-white text-3xl font-extrabold">₱{{ car.price_per_day.toLocaleString() }}</span>
                    <span class="text-[#A3A3A3] text-sm mb-1">Per day</span>
                </div>

                <div
                    v-if="currentRental" 
                    class="flex justify-center items-center gap-2 bg-[#2A2516] border border-[#FFAE00] rounded-lg py-3">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 16 16"
                        class="w-5 h-5 text-[#FFAE00]"
                        fill="currentColor"
                    >
                        <path d="M12.25,7H12V4c0-1.653-1.347-3-3-3H7C5.347,1,4,2.347,4,4v3H3.75C3.338,7,3,7.338,3,7.75v6.5C3,14.663,3.338,15,3.75,15h8.5 c0.413,0,0.75-0.337,0.75-0.75v-6.5C13,7.338,12.663,7,12.25,7z M6,4c0-0.55,0.45-1,1-1h2c0.55,0,1,0.45,1,1v3H6V4z"/>
                    </svg>

                    <div class="flex flex-col items-center leading-tight">
                        <span class="text-[#FFAE00] text-sm font-medium">
                            Currently Rented
                        </span>
                        <span class="text-[#FFAE00] text-xs opacity-80">
                            Until {{ rentedUntil }}
                        </span>
                    </div>
                </div>
    
                <!-- Perks -->
                <div class="grid grid-cols-2 py-4 gap-2">
                    <div v-for="perk in perks" :key="perk" class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-green-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                    </svg>
                    <span class="text-gray-300 text-xs">{{ perk }}</span>
                    </div>
                </div>
        
                <!-- CTAs -->
                <div class="flex flex-col gap-3 mt-2">

                    <!-- Available -->
                    <template v-if="!currentRental">
                        <button
                            @click="emit('book')"
                            class="
                                w-full bg-[#C1121F] hover:shadow-md hover:shadow-[#C1121F]/30
                                text-white text-sm font-bold py-3 rounded-lg
                                transition-all duration-300 cursor-pointer
                            "
                        >
                            Book now
                        </button>

                        <button
                            @click="scrollToOwnerNote"
                            class="
                                w-full border border-[#C1121F] hover:bg-[#2A1616]
                                hover:text-[#FF6161] text-[#C1121F] text-sm font-semibold
                                py-3 rounded-lg flex items-center justify-center gap-2
                                transition-all duration-300 cursor-pointer
                            "
                        >
                            Owner's note
                            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                            </svg>
                        </button>
                    </template>

                    <!-- Currently rented -->
                    <template v-else>
                        <button
                            @click="emit('reserve')"
                            class="
                                w-full bg-[#333] text-[#9E9090] hover:shadow-md hover:shadow-[#333]/50
                                text-sm font-semibold py-3 rounded-lg
                                transition-all duration-300 cursor-pointer
                            "
                        >
                            Reserve in Advance
                        </button>

                        <button
                            @click="emit('notify-available')"
                            class="
                                w-full border border-[#9E9090]
                                hover:bg-[#242424]
                                text-[#9E9090] text-sm font-semibold
                                py-3 rounded-lg
                                transition-all duration-300 cursor-pointer
                            "
                        >
                            Notify me when available
                        </button>
                    </template>

                </div>
            </div>

        </div>

        <div class="flex flex-col w-full md:flex-row gap-6">
            <!-- Rental Terms -->
            <div class="w-full overflow-hidden mt-1">
                <div class="px-5 py-4 border-b border-[#3F3F3F]">
                <h3 class="text-white font-bold text-sm">Rental terms</h3>
                </div>
                <div class="divide-y divide-[#3F3F3F]">
                <div
                    v-for="term in rentalTerms"
                    :key="term.label"
                    class="flex items-center justify-between px-5 py-3"
                >
                    <span class="text-gray-400 text-xs">{{ term.label }}</span>
                    <span class="text-white text-xs font-bold">{{ term.value }}</span>
                </div>
                </div>
            </div>

            <!-- Features -->
            <div class="w-full overflow-hidden">
                <div class="px-5 py-4 border-b border-[#3F3F3F]">
                    <h3 class="text-white font-bold text-sm">Features</h3>
                </div>

                <div class="divide-y divide-[#3F3F3F]">
                    <div
                        v-for="feature in car.features"
                        :key="feature"
                        class="flex items-center gap-3 px-5 py-3"
                    >
                        <svg
                            class="w-4 h-4 text-green-400 flex-shrink-0"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2.5"
                                d="M5 13l4 4L19 7"
                            />
                        </svg>

                        <span class="text-white text-xs font-medium">
                            {{ feature }}
                        </span>
                    </div>
                </div>
            </div>

            <!-- Specifications -->
            <div class="w-full overflow-hidden">
                <div class="px-5 py-4 border-b border-[#3F3F3F]">
                    <h3 class="text-white font-bold text-sm">Specifications</h3>
                </div>
                <div class="divide-y divide-[#3F3F3F]">
                <div
                    v-for="spec in specifications"
                    :key="spec.label"
                    class="flex items-start justify-between px-5 py-3 gap-4"
                >
                    <span class="text-gray-400 text-xs w-24">{{ spec.label }}</span>

                    <span
                        class="text-white text-xs font-bold text-right"
                    >
                        {{ spec.value }}
                    </span>
                </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Car } from '~/utils/api/api'

const props = defineProps<{
    car: Car
    avgRating: number
    totalReviews: number
}>()

const emit = defineEmits<{
    (e: 'book'): void
    (e: 'reserve'): void
    (e: 'write-review'): void
    (e: 'notify-available'): void
}>()

interface RentalTerm {
    label: string
    value: string
}
 
const activeImage = ref<number>(0)

const perks: string[] = [
    'Free cancellation',
    'No hidden fees',
    'Ready for pickup',
    'Well maintained',
]
 
const rentalTerms: RentalTerm[] = [
    { label: 'Min. days', value: '1 day' },
    { label: 'Fuel policy', value: 'Full-full' },
    { label: 'Insurance', value: '(Ask)' },
]

const currentRental = computed(() => useCurrentRental(props.car))

console.log('props:',props.car.unavailable_periods)
console.log('Current:', currentRental.value)

const rentedUntil = computed(() => {
    if (!currentRental.value) return ''

    return new Intl.DateTimeFormat('en-PH', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
    }).format(new Date(currentRental.value.return_date))
})

const specifications = computed(() => {
    if (!props.car) return []

    return [
        { label: 'Price per day', value: `₱${Number(props.car.price_per_day).toLocaleString()}` },
        { label: 'Transmission', value: props.car.transmission },
        { label: 'Engine', value: props.car.engine },
        { label: 'Fuel type', value: props.car.fuel_type },
        { label: 'Seats', value: props.car.seats.toString() },
    ]
})

const galleryImages = computed(() => {
    if (!props.car?.meta) return []

    return [
        props.car.meta.primary_image,
        ...props.car.meta.images
    ].filter(Boolean)
})
 
function prevImage(): void {
  const total = galleryImages.value.length

  if (total === 0) return

  activeImage.value =
    (activeImage.value - 1 + total) % total
}

function nextImage(): void {
  const total = galleryImages.value.length

  if (total === 0) return

  activeImage.value =
    (activeImage.value + 1) % total
}

const scrollToOwnerNote = (): void => {
    const section = document.getElementById('owner-note')

    if (section) {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        })
    }
}
</script>
