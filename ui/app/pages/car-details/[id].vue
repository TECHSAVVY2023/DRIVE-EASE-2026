<template>
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

    <Banner 
        subtitle="More info about the car"
        title="Car Details"
        :breadcrumbs="[
            { label: 'Home', to: '/' },
            { label: 'Fleet', to: '/fleet' },
            { label: 'Car Details' }
        ]"
    />

    <div class="min-h-screen bg-[#121212] font-[poppins] px-4 py-8">
        <div v-if="car" class="max-w-4xl h-fit mx-auto flex flex-col gap-6">

            <!-- Top Section: Images + Info -->
            <div class="flex flex-col justify-center gap-4 items-center bg-[#1B1B1B] px-4 py-4 rounded-xl">
                
                <div class="flex flex-col w-full md:flex-row md:items-center gap-6">
                    <!-- Left: Image Gallery -->
                    <div class="flex flex-1 flex-col justify-center gap-2 w-full h-full">
                        <!-- Main Image -->
                        <div class="relative bg-[#1a1a1a] rounded-xl overflow-hidden h-52 md:h-fit flex items-center justify-center border border-[#222]">
                            <img
                            :src="car.images[activeImage]"
                            :alt="car.name"
                            class="w-full h-full object-cover"
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
                            v-for="(img, i) in car.images"
                            :key="i"
                            @click="activeImage = i"
                            class="w-16 h-12 rounded-lg overflow-hidden border-2 transition-colors duration-200 flex-shrink-0"
                            :class="activeImage === i ? 'border-[#C1121F]' : 'border-[#222] hover:border-[#444]'"
                            >
                            <img :src="img" :alt="`Thumbnail ${i + 1}`" class="w-full h-full object-cover" />
                            </button>
                        </div>
                    </div>
            
                    <!-- Right: Car Info -->
                    <div class="flex-1 flex flex-col gap-4 w-full pt-4">
                    <!-- Name + Status -->
                    <div class="flex items-start justify-between gap-3">
                        <h1 class="text-white font-extrabold text-2xl leading-tight">{{ car.name }}</h1>
                        <span class="flex items-center gap-1.5 text-xs font-semibold px-3 py-1 rounded-full flex-shrink-0"
                        :class="car.available ? 'bg-green-500/10 text-green-400 border border-green-500/30' : 'bg-red-500/10 text-red-400 border border-red-500/30'"
                        >
                        <span class="w-1.5 h-1.5 rounded-full" :class="car.available ? 'bg-green-400' : 'bg-red-400'"></span>
                        {{ car.available ? 'AVAILABLE' : 'UNAVAILABLE' }}
                        </span>
                    </div>
            
                    <!-- Rating -->
                    <div class="flex items-center gap-1.5">
                        <svg class="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                        </svg>
                        <span class="text-yellow-400 text-sm font-semibold">{{ car.rating }}</span>
                        <span class="text-gray-400 text-xs">({{ car.reviews }} reviews)</span>
                    </div>
            
                    <!-- Price -->
                    <div class="flex items-end gap-2">
                        <span class="text-white text-3xl font-extrabold">₱{{ car.price.toLocaleString() }}</span>
                        <span class="text-gray-400 text-sm mb-1">Per day</span>
                    </div>
            
                    <!-- Perks -->
                    <div class="grid grid-cols-2 gap-2">
                        <div v-for="perk in perks" :key="perk" class="flex items-center gap-2">
                        <svg class="w-4 h-4 text-green-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                        </svg>
                        <span class="text-gray-300 text-xs">{{ perk }}</span>
                        </div>
                    </div>
            
                    <!-- CTAs -->
                    <div class="flex flex-col gap-3 mt-2">
                        <button class="w-full bg-[#C1121F] hover:bg-red-700 text-white text-sm font-bold py-3 rounded-lg transition-colors duration-200">
                        Book now
                        </button>
                        <button class="w-full border border-white hover:bg-white hover:text-[#C1121F] text-white text-sm font-semibold py-3 rounded-lg flex items-center justify-center gap-2 transition-colors duration-200">
                        Owner's note
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                        </button>
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

                    <!-- Specifications -->
                    <div class="w-full overflow-hidden">
                        <div class="px-5 py-4 border-b border-[#3F3F3F]">
                        <h3 class="text-white font-bold text-sm">Specifications</h3>
                        </div>
                        <div class="divide-y divide-[#3F3F3F]">
                        <div
                            v-for="spec in car.specifications"
                            :key="spec.label"
                            class="flex items-center justify-between px-5 py-3"
                        >
                            <span class="text-gray-400 text-xs">{{ spec.label }}</span>
                            <span class="text-white text-xs font-bold">{{ spec.value }}</span>
                        </div>
                        </div>
                    </div>
                </div>

            </div>
    
            <!-- Owner's Note Section -->
            <div class="bg-[#1a1a1a] border border-[#C1121F]/30 rounded-xl overflow-hidden">
                <div class="flex items-center gap-2 px-5 py-4 border-b border-[#C1121F]/20">
                <svg class="w-4 h-4 text-[#C1121F]" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
                </svg>
                <span class="text-[#C1121F] text-xs font-semibold">Owner's note</span>
                </div>
                <div class="px-6 py-5">
                <svg class="w-5 h-5 text-[#C1121F]/40 mb-3" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M6 17h3l2-4V7H5v6h3zm8 0h3l2-4V7h-6v6h3z"/>
                </svg>
                <p class="text-gray-300 text-sm leading-relaxed">{{ car.ownerNote }}</p>
                <svg class="w-5 h-5 text-[#C1121F]/40 mt-3 ml-auto block" fill="currentColor" viewBox="0 0 24 24" style="transform: rotate(180deg)">
                    <path d="M6 17h3l2-4V7H5v6h3zm8 0h3l2-4V7h-6v6h3z"/>
                </svg>
                </div>
            </div>
    
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import car3 from '~/assets/images/sample.png'

const { setAuth } = useAuth()
const route = useRoute()

const sidebarOpen = ref<boolean>(false)

const menuOpen = ref(false)

const toggleMenu = () => {
    menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
    menuOpen.value = false
}

const handleCloseSidebar = (): void => {
    sidebarOpen.value = false
}

const handleOpenSidebar = (): void => {
    sidebarOpen.value = true
}

if (route.query.token) {
    await setAuth(route.query.token as string)
}

interface Spec {
  label: string
  value: string
}
 
interface RentalTerm {
  label: string
  value: string
}
 
interface Car {
    name: string
    available: boolean
    rating: number
    reviews: number
    pricePerDay: number
    images: string[]
    specifications: Spec[]
    ownerNote: string
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
 
function prevImage(): void {
  activeImage.value = (activeImage.value - 1 + cars[0].images.length) % cars[0].images.length
}
 
function nextImage(): void {
  activeImage.value = (activeImage.value + 1) % cars[0].images.length
}

const { cars } = useCarFilters()

const car = computed(() => {
    const id = Number(route.params.id)
    return cars.find(c => c.id === id)
})

</script>