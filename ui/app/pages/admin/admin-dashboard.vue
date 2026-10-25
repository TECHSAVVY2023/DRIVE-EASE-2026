<template>
    <div class="flex h-screen bg-[#0D0D0D] font-[poppins] overflow-hidden">

        <!-- Sidebar -->
        <AdminCommonSidebarNav
            :sidebarOpen="sidebarOpen"
            @close-sidebar="sidebarOpen = false"
        />

        <!-- Main -->
        <div class="flex-1 flex flex-col overflow-hidden">

            <!-- Topbar -->
            <AdminCommonTopbarNav
                :user="user"
                @open-sidebar="handleOpenSidebar"
                @close-sidebar="handleCloseSidebar"
                title="Dashboard"
                :isLoggedIn="isLoggedIn"
                :subtitle="currentDate"
            />

            <!-- Content -->
            <main
                class="flex-1 min-h-0 min-w-0 overflow-y-auto
                       px-4 sm:px-6 lg:px-8 py-6 sm:py-8"
            >

                <!-- Header -->
                <div class="flex flex-col sm:flex-row sm:items-center
                            sm:justify-between gap-4 mb-8">

                    <div>
                        <h1 class="text-white text-xl font-extrabold">
                            Dashboard
                        </h1>

                        <p class="text-gray-400 text-xs mt-1">
                            Overview of your rental business
                        </p>
                    </div>

                    <select
                        v-model="selectedRevenueMonth"
                        aria-label="Revenue month"
                        class="rounded-lg border border-[#292929] bg-[#1a1a1a] px-4 py-2.5 text-sm text-gray-300 transition hover:bg-[#222] focus:border-[#C1121F] focus:outline-none"
                    >
                        <option
                            v-for="option in revenueMonthOptions"
                            :key="option.value"
                            :value="option.value"
                        >
                            {{ option.label }}
                        </option>
                    </select>

                </div>


                <!-- ========================= -->
                <!-- STAT CARDS -->
                <!-- ========================= -->

                <div class="grid grid-cols-2 xl:grid-cols-4 gap-4 mb-6">

                    <div
                        v-for="stat in statCards"
                        :key="stat.label"
                        class="bg-[#1a1a1a] rounded-xl p-5
                               border border-[#222]"
                    >

                        <div class="flex items-start justify-between">

                            <div
                                class="w-9 h-9 rounded-lg
                                       bg-[#C1121F]
                                       flex items-center justify-center"
                            >
                                <svg
                                    class="w-5 h-5 text-white"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path
                                        :d="stat.icon"
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                    />
                                </svg>
                            </div>

                            <span
                                :class="[
                                    'text-[11px] font-semibold px-2 py-1 rounded-md',
                                    stat.positive
                                        ? 'text-green-400 bg-green-400/10'
                                        : 'text-red-400 bg-red-400/10'
                                ]"
                            >
                                {{ stat.change }}
                            </span>

                        </div>

                        <p class="text-gray-400 text-xs mt-4">
                            {{ stat.label }}
                        </p>

                        <p class="text-white text-2xl sm:text-3xl
                                  font-extrabold mt-1">
                            {{ stat.value }}
                        </p>

                    </div>

                </div>


                <!-- ========================= -->
                <!-- MAIN ANALYTICS -->
                <!-- ========================= -->

                <div class="grid grid-cols-1 xl:grid-cols-3 gap-4 mb-6">

                    <AdminDashboardRevenueOverview :month="selectedRevenueMonth" />

                    <!-- Fleet Status -->
                    <div
                        class="bg-[#1a1a1a] rounded-xl
                               p-6 border border-[#222]"
                    >

                        <div class="mb-6">
                            <h2 class="text-white font-bold text-base">
                                Fleet status
                            </h2>

                            <p class="text-gray-500 text-xs mt-1">
                                Current vehicle condition
                            </p>
                        </div>

                        <div class="space-y-5">

                            <div
                                v-for="item in fleetStatus"
                                :key="item.label"
                            >

                                <div class="flex justify-between mb-2">

                                    <span class="text-gray-400 text-xs">
                                        {{ item.label }}
                                    </span>

                                    <span class="text-white text-xs font-semibold">
                                        {{ item.value }}
                                    </span>

                                </div>

                                <div
                                    class="h-2 rounded-full
                                           bg-[#292929] overflow-hidden"
                                >
                                    <div
                                        class="h-full rounded-full
                                               bg-[#C1121F]"
                                        :style="{
                                            width: `${item.percentage}%`
                                        }"
                                    ></div>
                                </div>

                            </div>

                        </div>

                        <button
                            class="w-full mt-7 text-xs font-semibold
                                   text-gray-300 border border-[#303030]
                                   rounded-lg py-2.5
                                   hover:bg-[#222] transition"
                        >
                            View fleet
                        </button>

                    </div>

                </div>


                <!-- ========================= -->
                <!-- BOOKINGS + ATTENTION -->
                <!-- ========================= -->

                <div class="grid grid-cols-1 xl:grid-cols-3 gap-4 mb-6">

                    <!-- Recent bookings -->
                    <div
                        class="xl:col-span-2 bg-[#1a1a1a]
                               rounded-xl p-6 border border-[#222]"
                    >

                        <div class="flex items-center justify-between mb-5">

                            <div>
                                <h2 class="text-white font-bold text-base">
                                    Recent bookings
                                </h2>

                                <p class="text-gray-500 text-xs mt-1">
                                    Latest rental activity
                                </p>
                            </div>

                            <button
                                class="text-[#C1121F] text-xs
                                       font-semibold hover:text-red-400"
                            >
                                View all
                            </button>

                        </div>


                        <div class="overflow-x-auto">

                            <table class="w-full min-w-[600px]">

                                <thead>
                                    <tr
                                        class="text-left text-[10px]
                                               uppercase tracking-wide
                                               text-gray-500
                                               border-b border-[#292929]"
                                    >
                                        <th class="pb-3 font-medium">
                                            Booking
                                        </th>

                                        <th class="pb-3 font-medium">
                                            Customer
                                        </th>

                                        <th class="pb-3 font-medium">
                                            Vehicle
                                        </th>

                                        <th class="pb-3 font-medium">
                                            Amount
                                        </th>

                                        <th class="pb-3 font-medium">
                                            Status
                                        </th>
                                    </tr>
                                </thead>

                                <tbody>

                                    <tr
                                        v-for="booking in recentBookings"
                                        :key="booking.id"
                                        class="border-b border-[#222]
                                               last:border-0"
                                    >

                                        <td class="py-4 text-xs text-white
                                                   font-semibold">
                                            {{ booking.id }}
                                        </td>

                                        <td class="py-4 text-xs text-gray-400">
                                            {{ booking.customer }}
                                        </td>

                                        <td class="py-4 text-xs text-gray-400">
                                            {{ booking.vehicle }}
                                        </td>

                                        <td class="py-4 text-xs text-white">
                                            {{ booking.amount }}
                                        </td>

                                        <td class="py-4">

                                            <span
                                                :class="[
                                                    'text-[10px] font-semibold px-2.5 py-1 rounded-full',
                                                    booking.status === 'Confirmed'
                                                        ? 'text-green-400 bg-green-400/10'
                                                        : booking.status === 'Pending'
                                                            ? 'text-yellow-400 bg-yellow-400/10'
                                                            : 'text-gray-400 bg-gray-400/10'
                                                ]"
                                            >
                                                {{ booking.status }}
                                            </span>

                                        </td>

                                    </tr>

                                </tbody>

                            </table>

                        </div>

                    </div>


                    <!-- Needs attention -->
                    <div
                        class="bg-[#1a1a1a] rounded-xl
                               p-6 border border-[#222]"
                    >

                        <div class="mb-5">
                            <h2 class="text-white font-bold text-base">
                                Needs attention
                            </h2>

                            <p class="text-gray-500 text-xs mt-1">
                                Items requiring action
                            </p>
                        </div>


                        <div class="space-y-3">

                            <div
                                v-for="item in attentionItems"
                                :key="item.label"
                                class="flex items-center gap-3
                                       p-3 rounded-lg
                                       bg-[#222]"
                            >

                                <div
                                    class="w-8 h-8 rounded-lg
                                           bg-[#C1121F]/10
                                           flex items-center justify-center
                                           flex-shrink-0"
                                >
                                    <span class="text-[#C1121F] text-sm">
                                        !
                                    </span>
                                </div>

                                <div class="flex-1 min-w-0">

                                    <p class="text-white text-xs font-semibold">
                                        {{ item.label }}
                                    </p>

                                    <p class="text-gray-500 text-[10px] mt-0.5">
                                        {{ item.description }}
                                    </p>

                                </div>

                                <span
                                    class="text-white text-xs font-bold"
                                >
                                    {{ item.count }}
                                </span>

                            </div>

                        </div>

                    </div>

                </div>


                <!-- ========================= -->
                <!-- QUICK ACTIONS -->
                <!-- ========================= -->

                <div
                    class="bg-[#1a1a1a] rounded-xl p-6
                           border border-[#222]"
                >

                    <div class="mb-5">
                        <h2 class="text-white font-bold text-base">
                            Quick actions
                        </h2>

                        <p class="text-gray-500 text-xs mt-1">
                            Common administrative tasks
                        </p>
                    </div>

                    <div
                        class="grid grid-cols-1 sm:grid-cols-3 gap-3"
                    >

                        <button
                            v-for="action in quickActions"
                            :key="action.label"
                            class="flex items-center gap-3
                                   p-4 rounded-lg
                                   bg-[#222]
                                   border border-[#292929]
                                   hover:border-[#C1121F]
                                   hover:bg-[#252525]
                                   transition text-left"
                        >

                            <div
                                class="w-9 h-9 rounded-lg
                                       bg-[#C1121F]
                                       flex items-center justify-center"
                            >
                                <span class="text-white text-sm">
                                    +
                                </span>
                            </div>

                            <div>
                                <p class="text-white text-xs font-semibold">
                                    {{ action.label }}
                                </p>

                                <p class="text-gray-500 text-[10px] mt-1">
                                    {{ action.description }}
                                </p>
                            </div>

                        </button>

                    </div>

                </div>

            </main>

        </div>

    </div>
</template>


<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

const { isLoggedIn } = useAuth()
const { apiFetch } = useApiFetch()
const { user } = useCurrentUser()

const sidebarOpen = ref(false)

const handleCloseSidebar = (): void => {
    sidebarOpen.value = false
}

const handleOpenSidebar = (): void => {
    sidebarOpen.value = true
}


const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
})


/* =========================
   STAT CARDS
========================= */

const statCards = [
    {
        label: 'Bookings',
        value: '20',
        change: '+12.5%',
        positive: true,
        icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
    },

    {
        label: 'Revenue',
        value: '₱184K',
        change: '+8.2%',
        positive: true,
        icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    },

    {
        label: 'Active rentals',
        value: '18',
        change: '+3',
        positive: true,
        icon: 'M13 10V3L4 14h7v7l9-11h-7z',
    },

    {
        label: 'Customers',
        value: '67',
        change: '+15.4%',
        positive: true,
        icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z',
    },
]


const currentMonth = new Date()
const selectedRevenueMonth = ref(
    `${currentMonth.getFullYear()}-${String(currentMonth.getMonth() + 1).padStart(2, '0')}`
)

const revenueMonthOptions = Array.from({ length: 12 }, (_, index) => {
    const date = new Date(currentMonth.getFullYear(), currentMonth.getMonth() - index, 1)

    return {
        value: `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`,
        label: date.toLocaleDateString('en-US', {
            month: 'long',
            year: 'numeric',
        }),
    }
})


/* =========================
   FLEET
========================= */

type FleetStatus = {
    label: string
    value: number
    percentage: number
}

const fleetStatus = ref<FleetStatus[]>([
    {
        label: 'Available',
        value: 18,
        percentage: 55,
    },
    {
        label: 'Rented',
        value: 12,
        percentage: 36,
    },
    {
        label: 'Maintenance',
        value: 3,
        percentage: 9,
    },
])


/* =========================
   RECENT BOOKINGS
========================= */

const recentBookings = ref([
    {
        id: '#BK-001',
        customer: 'Juan Dela Cruz',
        vehicle: 'Toyota Wigo',
        amount: '₱2,200',
        status: 'Confirmed',
    },
    {
        id: '#BK-002',
        customer: 'Maria Santos',
        vehicle: 'Ford Raptor',
        amount: '₱8,500',
        status: 'Pending',
    },
    {
        id: '#BK-003',
        customer: 'Carlos Reyes',
        vehicle: 'Toyota Vios',
        amount: '₱3,600',
        status: 'Confirmed',
    },
    {
        id: '#BK-004',
        customer: 'Anna Garcia',
        vehicle: 'Toyota Wigo',
        amount: '₱2,200',
        status: 'Completed',
    },
])


/* =========================
   ATTENTION
========================= */

const attentionItems = ref([
    {
        label: 'Pending approvals',
        description: 'Bookings waiting for review',
        count: 4,
    },
    {
        label: 'Payment issues',
        description: 'Transactions requiring attention',
        count: 2,
    },
    {
        label: 'Vehicles in maintenance',
        description: 'Cars currently unavailable',
        count: 3,
    },
])


/* =========================
   QUICK ACTIONS
========================= */

const quickActions = [
    {
        label: 'Add car',
        description: 'Add a vehicle to your fleet',
    },
    {
        label: 'View bookings',
        description: 'Review and manage bookings',
    },
    {
        label: 'Add user',
        description: 'Create a new customer account',
    },
]


/* =========================
   ADMIN PAGE CLASS
========================= */

onMounted(() => {
    document.documentElement.classList.add('admin-page')
})

onBeforeUnmount(() => {
    document.documentElement.classList.remove('admin-page')
})
</script>
