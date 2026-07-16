<template>
    <div class="flex h-screen bg-[#0D0D0D] font-[poppins] overflow-hidden">

        <AdminSidebar :sidebarOpen="sidebarOpen" @close-sidebar="sidebarOpen = false" />

        <!-- Main -->
        <div class="flex-1 flex flex-col overflow-hidden">

            <AdminTopbar 
                :user="user" 
                :isLoggedIn="isLoggedIn"
                @open-sidebar="handleOpenSidebar"
                @close-sidebar="handleCloseSidebar"
                title="Admin / Dashboard"
                :subtitle="currentDate"
            />

            <!-- Content -->
            <main class="flex-1 overflow-y-auto px-8 py-8">

                <!-- Page header -->
                <div class="flex justify-between items-center mb-8">
                    <div>
                        <h1 class="text-white text-lg font-extrabold">Summary</h1>
                        <p class="text-gray-400 text-xs">Overview for this month</p>
                    </div>

                    <button class="flex items-center gap-2 text-white text-sm px-4 py-2 rounded-lg">
                        This month
                        <svg class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
                    </button>
                </div>

                <!-- Stat Cards -->
                <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">

                    <div class="bg-[#1a1a1a] rounded-xl p-5 flex flex-col gap-3 border border-[#222]">
                        <div class="w-9 h-9 bg-[#C1121F] rounded-lg flex items-center justify-center">
                            <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
                        </div>
                        <p class="text-gray-400 text-xs">Bookings</p>
                        <p class="text-white text-3xl font-extrabold">20</p>
                    </div>

                    <div class="bg-[#1a1a1a] rounded-xl p-5 flex flex-col gap-3 border border-[#222]">
                        <div class="w-9 h-9 bg-[#C1121F] rounded-lg flex items-center justify-center">
                            <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        </div>
                        <p class="text-gray-400 text-xs">Revenue</p>
                        <p class="text-white text-3xl font-extrabold">₱184K</p>
                    </div>

                    <div class="bg-[#1a1a1a] rounded-xl p-5 flex flex-col gap-3 border border-[#222]">
                        <div class="w-9 h-9 bg-[#C1121F] rounded-lg flex items-center justify-center">
                        <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                        </div>
                        <p class="text-gray-400 text-xs">Active rentals</p>
                        <p class="text-white text-3xl font-extrabold">18</p>
                    </div>

                    <div class="bg-[#1a1a1a] rounded-xl p-5 flex flex-col gap-3 border border-[#222]">
                        <div class="w-9 h-9 bg-[#C1121F] rounded-lg flex items-center justify-center">
                        <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                        </div>
                        <p class="text-gray-400 text-xs">Customers</p>
                        <p class="text-white text-3xl font-extrabold">67</p>
                    </div>

                </div>

                <!-- Bottom Row -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">

                    <!-- Fleet Overview -->
                    <div class="bg-[#1a1a1a] rounded-xl p-6 border border-[#222]">
                        
                        <h2 class="text-white font-bold text-base mb-5">Fleet overview</h2>
                        <div class="flex flex-col gap-4">
                        <div v-for="(item, i) in fleet" :key="i" class="flex items-center gap-4">
                            <span class="text-gray-400 text-sm w-20 flex-shrink-0">{{ item.label }}</span>
                            <div class="flex-1 bg-[#2a2a2a] rounded-full h-2">
                            <div
                                class="bg-[#C1121F] h-2 rounded-full"
                                :style="`width: ${(item.value / item.max) * 100}%`"
                            ></div>
                            </div>
                            <span class="text-gray-400 text-xs flex-shrink-0">{{ item.value }}/{{ item.max }}</span>
                        </div>
                        </div>

                    </div>

                    <!-- Quick Actions -->
                    <div class="bg-[#1a1a1a] rounded-xl p-6 border border-[#222]">
                        <h2 class="text-white font-bold text-base mb-5">Quick actions</h2>
                        <div class="flex flex-col gap-3">
                        <button class="w-full bg-[#C1121F] hover:bg-red-700 text-white text-sm font-semibold py-3 rounded-lg transition-colors duration-200">
                            Add users
                        </button>
                        <button class="w-full bg-[#C1121F] hover:bg-red-700 text-white text-sm font-semibold py-3 rounded-lg transition-colors duration-200">
                            Add cars
                        </button>
                        <button class="w-full bg-[#C1121F] hover:bg-red-700 text-white text-sm font-semibold py-3 rounded-lg transition-colors duration-200">
                            Add rental
                        </button>
                        </div>
                    </div>

                </div>

            </main>

        </div>

    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

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

type FleetItem = {
    label: string
    value: number
    max: number
}

const fleet = ref<FleetItem[]>([
    { label: 'Economy', value: 8, max: 10 },
    { label: 'Economy', value: 6, max: 10 },
    { label: 'Economy', value: 9, max: 10 },
    { label: 'Economy', value: 5, max: 10 },
])
</script>