<template>
    <div class="flex min-h-screen bg-[#0D0D0D] font-[poppins]">

        <AdminSidebar 
            :sidebarOpen="sidebarOpen" 
            @close-sidebar="sidebarOpen = false" 
        />

        <!-- Main -->
        <div class="flex-1 flex flex-col min-w-0">

        <AdminTopbar
            :user="user"
            :isLoggedIn="isLoggedIn"
            title="Admin / Fleet"
            :subtitle="currentDate"
        />

        <div class="mx-4 sm:mx-6 lg:mx-10 my-6 lg:my-10">

            <!-- Stat Cards -->
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-6 sm:mb-8">
            <div
                v-for="stat in stats"
                :key="stat.label"
                class="bg-[#1a1a1a] rounded-xl p-4 sm:p-5 flex flex-col gap-1.5 sm:gap-2 border-t-4 sm:border-t-6 border-[#C1121F]"
            >
                <p class="text-gray-400 text-[11px] sm:text-xs">{{ stat.label }}</p>
                <p class="text-white text-2xl sm:text-3xl font-extrabold">{{ stat.value }}</p>
            </div>
            </div>

            <!-- Table Card -->
            <div class="bg-[#1a1a1a] rounded-xl border border-[#222] flex flex-col gap-4 overflow-hidden">

            <!-- Filters + Search -->
            <div class="flex flex-col xl:flex-row justify-between gap-3 px-4 sm:px-5 pt-4 sm:pt-5">

                <div class="flex gap-2">
                    <button
                        v-for="tab in tabs"
                        :key="tab"
                        @click="activeTab = tab"
                        class="max-h-15 text-xs px-3 py-1.5 rounded-full border transition-colors duration-200 font-medium"
                        :class="activeTab === tab
                        ? 'bg-[#C1121F] border-[#C1121F] text-white'
                        : 'border-[#2a2a2a] text-gray-400 hover:border-white hover:text-white'"
                    >
                        {{ tab }}
                    </button>
                </div>

                <div class="flex flex-col xl:flex-row gap-2 sm:gap-3">
                    <div class="relative">
                        <input
                            v-model="search"
                            type="text"
                            placeholder="Search"
                            class="bg-[#111111] border border-[#2a2a2a] text-white text-sm px-4 py-2 pr-9 rounded-lg w-full placeholder-[#444] focus:outline-none focus:border-[#C1121F] transition-colors duration-200"
                        />
                        <svg class="w-4 h-4 text-gray-400 fill-none absolute right-3 top-1/2 -translate-y-1/2" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                        </svg>
                    </div>

                    <button class="flex items-center justify-center gap-2 bg-[#C1121F] hover:bg-red-700 text-white text-sm font-semibold px-5 py-2 rounded-lg transition-colors duration-200">
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                        </svg>
                        Add car
                    </button>
                </div>

            </div>

            <div class="hidden lg:block overflow-x-auto">
                <table class="w-full text-sm">
                <thead>
                    <tr class="border-b border-[#222]">
                    <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">Vehicle</th>
                    <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">Category</th>
                    <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">Status</th>
                    <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">Rate/day</th>
                    <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="paginatedCars.length === 0">
                    <td colspan="5" class="text-center text-gray-500 text-sm py-16">No vehicles found.</td>
                    </tr>

                    <tr
                    v-for="(car, i) in paginatedCars"
                    :key="i"
                    class="border-b border-[#1f1f1f] hover:bg-[#222] transition-colors duration-150"
                    >
                    <!-- Vehicle -->
                    <td class="px-5 py-4">
                        <div class="flex items-center gap-3">
                        <div class="w-12 h-9 bg-[#111] rounded-lg overflow-hidden flex-shrink-0 flex items-center justify-center">
                            <img :src="car.image" :alt="car.name" class="w-full h-full object-cover" @error="(e) => (e.target as HTMLImageElement).style.display = 'none'" />
                        </div>
                        <span class="text-white text-sm font-medium">{{ car.name }}</span>
                        </div>
                    </td>

                    <!-- Category -->
                    <td class="px-5 py-4 text-gray-300 text-sm">{{ car.category }}</td>

                    <!-- Status -->
                    <td class="px-5 py-4">
                        <span class="text-xs font-semibold px-2.5 py-1 rounded-full" :class="statusClass(car.status)">
                        {{ car.status }}
                        </span>
                    </td>

                    <!-- Rate -->
                    <td class="px-5 py-4 text-white text-sm font-medium">₱{{ car.rate.toLocaleString() }}</td>

                    <!-- Actions -->
                    <td class="px-5 py-4">
                        <div class="flex items-center gap-2">
                        <button class="w-7 h-7 rounded-md bg-[#C1121F] hover:bg-red-700 flex items-center justify-center transition-colors duration-200">
                            <svg class="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                            </svg>
                        </button>
                        <button class="w-7 h-7 rounded-md bg-[#C1121F] hover:bg-red-700 flex items-center justify-center transition-colors duration-200">
                            <svg class="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                            </svg>
                        </button>
                        <button class="w-7 h-7 rounded-md bg-[#C1121F] hover:bg-red-700 flex items-center justify-center transition-colors duration-200">
                            <svg class="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                            </svg>
                        </button>
                        </div>
                    </td>
                    </tr>
                </tbody>
                </table>
            </div>

            <!-- Cards — mobile (< md) -->
            <div class="lg:hidden flex flex-col divide-y divide-[#1f1f1f]">
                <div v-if="paginatedCars.length === 0" class="text-center text-gray-500 text-sm py-16">
                No vehicles found.
                </div>

                <div
                v-for="(car, i) in paginatedCars"
                :key="i"
                class="flex items-center gap-3 px-4 py-3.5 hover:bg-[#222] transition-colors duration-150"
                >
                <!-- Thumbnail -->
                <div class="w-12 h-9 bg-[#111] rounded-lg overflow-hidden flex-shrink-0 flex items-center justify-center">
                    <img :src="car.image" :alt="car.name" class="w-full h-full object-cover" @error="(e) => (e.target as HTMLImageElement).style.display = 'none'" />
                </div>

                <!-- Info -->
                <div class="flex-1 min-w-0">
                    <p class="text-white text-sm font-medium truncate">{{ car.name }}</p>
                    <div class="flex items-center gap-2 mt-1">
                    <span class="text-xs font-semibold px-2 py-0.5 rounded-full" :class="statusClass(car.status)">{{ car.status }}</span>
                    <span class="text-gray-500 text-xs">{{ car.category }}</span>
                    </div>
                </div>

                <!-- Rate -->
                <p class="text-white text-sm font-semibold flex-shrink-0">₱{{ car.rate.toLocaleString() }}</p>

                <!-- Actions -->
                <div class="flex items-center gap-1.5 flex-shrink-0">
                    <button class="w-7 h-7 rounded-md bg-[#C1121F] hover:bg-red-700 flex items-center justify-center transition-colors duration-200">
                    <svg class="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                    </svg>
                    </button>
                    <button class="w-7 h-7 rounded-md bg-[#C1121F] hover:bg-red-700 flex items-center justify-center transition-colors duration-200">
                    <svg class="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    </button>
                    <button class="w-7 h-7 rounded-md bg-[#C1121F] hover:bg-red-700 flex items-center justify-center transition-colors duration-200">
                    <svg class="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                    </button>
                </div>
                </div>
            </div>

            <!-- Pagination -->
            <div class="flex items-center justify-center gap-2 px-4 sm:px-5 pb-4 sm:pb-5">
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
    </div>
</template>

<script setup lang="ts">
import { ref,computed } from 'vue'

const { isLoggedIn } = useAuth()
const { apiFetch } = useApiFetch()

const user = ref<any>(null)

watch(isLoggedIn, async (val) => {
    if (val) {
        user.value = await apiFetch('/auth/me/')
        console.log('profile_picture:', user.value.profile_picture)
    } else {
        user.value = null
    }
}, { immediate: true })

const sidebarOpen = ref<boolean>(false)

const handleCloseSidebar = (): void => {
    sidebarOpen.value = false
}

const handleOpenSidebar = (): void => {
    sidebarOpen.value = true
}

const currentDate = computed(() =>
    new Date().toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    })
)

const activeItem = ref('fleet')
 
type TabType = 'Available' | 'Unavailable' | 'Good' | 'In-maintenance'
type StatusType = 'Available' | 'Unavailable' | 'Rented'
type ConditionType = 'Good' | 'Fair' | 'In-maintenance'
 
interface Car {
    name: string
    category: string
    status: StatusType
    condition: ConditionType
    rate: number
    image: string
}
 
interface Stat {
    label: string
    value: number
}
 
const today = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
})
 
const activeTab = ref<TabType>('Available')
const search = ref<string>('')
const currentPage = ref<number>(1)
const perPage = 8
 
const tabs: TabType[] = ['Available', 'Unavailable', 'Good', 'In-maintenance']
 
const cars: Car[] = [
    { name: 'Toyota Wigo', category: 'Economy', status: 'Available', condition: 'Good', rate: 1200, image: '/images/car1.png' },
    { name: 'Toyota Wigo', category: 'Economy', status: 'Available', condition: 'Good', rate: 1200, image: '/images/car1.png' },
    { name: 'Toyota Wigo', category: 'Economy', status: 'Available', condition: 'Good', rate: 1200, image: '/images/car1.png' },
    { name: 'Toyota Wigo', category: 'Economy', status: 'Available', condition: 'Good', rate: 1200, image: '/images/car1.png' },
    { name: 'Toyota Vios', category: 'Economy', status: 'Rented', condition: 'Good', rate: 1800, image: '/images/car1.png' },
    { name: 'Toyota Innova', category: 'Family', status: 'Rented', condition: 'Fair', rate: 2500, image: '/images/car1.png' },
    { name: 'Toyota Fortuner', category: 'SUV', status: 'Unavailable', condition: 'In-maintenance', rate: 3500, image: '/images/car1.png' },
    { name: 'Toyota Hiace', category: 'Family', status: 'Available', condition: 'Good', rate: 4700, image: '/images/car1.png' },
    { name: 'Toyota Camry', category: 'Luxury', status: 'Available', condition: 'Good', rate: 4000, image: '/images/car1.png' },
    { name: 'Toyota Rush', category: 'SUV', status: 'Rented', condition: 'Good', rate: 2200, image: '/images/car1.png' },
]
 
const stats: Stat[] = [
    { label: 'Total vehicles', value: cars.length },
    { label: 'Available', value: cars.filter(c => c.status === 'Available').length },
    { label: 'Currently rented', value: cars.filter(c => c.status === 'Rented').length },
    { label: 'In-maintenance', value: cars.filter(c => c.condition === 'In-maintenance').length },
]
 
function statusClass(status: StatusType): string {
    const map: Record<StatusType, string> = {
        Available: 'bg-green-500/10 text-green-400',
        Unavailable: 'bg-red-500/10 text-red-400',
        Rented: 'bg-yellow-500/10 text-yellow-400',
    }
    return map[status] ?? ''
}
 
const filteredCars = computed<Car[]>(() => {
    let result = [...cars]
    
    if (activeTab.value === 'Available') result = result.filter(c => c.status === 'Available')
    if (activeTab.value === 'Unavailable') result = result.filter(c => c.status === 'Unavailable')
    if (activeTab.value === 'Good') result = result.filter(c => c.condition === 'Good')
    if (activeTab.value === 'In-maintenance') result = result.filter(c => c.condition === 'In-maintenance')
    
    if (search.value) {
        result = result.filter(c =>
        c.name.toLowerCase().includes(search.value.toLowerCase()) ||
        c.category.toLowerCase().includes(search.value.toLowerCase())
        )
    }
    
    return result
})
 
const totalPages = computed<number>(() => Math.max(1, Math.ceil(filteredCars.value.length / perPage)))
 
const paginatedCars = computed<Car[]>(() => {
    const start = (currentPage.value - 1) * perPage
    return filteredCars.value.slice(start, start + perPage)
})

</script>
