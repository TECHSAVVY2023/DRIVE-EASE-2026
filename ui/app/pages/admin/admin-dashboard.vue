<template>
    <AdminFleetAddCarModal
        v-model="addCarModalOpen"
        :vehicle="null"
        :is-editing="false"
        @save="handleCreateCar"
    />

    <AdminBookingAddBookingModal
        v-model="addBookingModalOpen"
        :users="bookingUsers"
        :cars="bookingCars"
        @save="handleCreateBooking"
    />

    <AdminUsersAddUserModal
        v-model="addUserModalOpen"
        :can-manage-roles="isSuperAdmin"
        @save="handleCreateUser"
    />

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
                    <div class="relative flex-1 sm:flex-none">
                        <select
                            v-model="selectedRevenueMonth"
                            aria-label="Revenue period"
                            class="
                                w-full rounded-lg border border-[#292929] bg-[#1a1a1a] py-2.5 pl-3.5 pr-9
                                text-sm text-gray-300 transition hover:bg-[#222] focus:border-[#C1121F] focus:outline-none
                                appearance-none"
                        >
                            <option
                                v-for="option in revenueMonthOptions"
                                :key="option.value"
                                :value="option.value"
                            >
                                {{ option.label }}
                            </option>
                        </select>

                        <svg
                            class="absolute right-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#8a8a8a] pointer-events-none"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        >
                            <path d="m6 9 6 6 6-6" />
                        </svg>
                    </div>
                </div>


                <!-- ========================= -->
                <!-- STAT CARDS -->
                <!-- ========================= -->

                <AdminDashboardStats :stat-cards="statCards" />

                <!-- ========================= -->
                <!-- MAIN ANALYTICS -->
                <!-- ========================= -->

                <div class="grid grid-cols-1 xl:grid-cols-3 gap-4 mb-6">

                    <AdminDashboardRevenueOverview :month="selectedRevenueMonth" />

                    <AdminDashboardFleetStatus />

                </div>


                <!-- ========================= -->
                <!-- BOOKINGS + ATTENTION -->
                <!-- ========================= -->

                <div class="grid grid-cols-1 xl:grid-cols-3 gap-4 mb-6">

                    <AdminDashboardRecentBookings />
                    <AdminDashboardNeedsAttention
                        v-if="!attentionResolved || hasAttention"
                        @loaded="handleAttentionLoaded"
                    />
                    <AdminDashboardQuickActions
                        v-else
                        compact
                        @select="handleQuickAction"
                    />

                </div>


                <!-- ========================= -->
                <!-- QUICK ACTIONS -->
                <!-- ========================= -->

                <AdminDashboardQuickActions
                    v-if="!attentionResolved || hasAttention"
                    @select="handleQuickAction"
                />

            </main>

        </div>

    </div>
</template>


<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import type { BookingForm } from '~/utils/types/booking'
import type { StatCard } from '~/utils/types/dashboard'
import type { CarForm } from '~/utils/types/fleet'
import type { AdminCreateUserFormPayload } from '~/utils/types/accounts'

type DashboardQuickAction = 'car' | 'booking' | 'user'

const { isLoggedIn } = useAuth()
const { user } = useCurrentUser()
const isSuperAdmin = computed(() => user.value?.role === 'Super Admin')

const sidebarOpen = ref(false)
const attentionResolved = ref(false)
const hasAttention = ref(false)

const addCarModalOpen = ref(false)
const addBookingModalOpen = ref(false)
const addUserModalOpen = ref(false)

const {
    users: bookingUsers,
    fetchUsers: fetchBookingUsers,
    resetFilters: resetUserFilters,
} = useUsersList()
const {
    fleet: bookingCars,
    fetchCars: fetchBookingCars,
    resetFilters: resetFleetFilters,
} = useFleetList()

const { handleCreateVehicle: createCar } = useCarAdminAdd()
const { handleCreateBooking: createBooking } = useAdminTransactionAdd()
const { handleCreateUser: createUser } = useUserAdminEdit()

const handleQuickAction = async (action: DashboardQuickAction) => {
    if (action === 'car') {
        addCarModalOpen.value = true
        return
    }

    if (action === 'user') {
        addUserModalOpen.value = true
        return
    }

    // The booking form searches the user and car arrays locally, so load the
    // same collections used by the booking page before displaying the modal.
    await Promise.all([
        resetUserFilters(),
        resetFleetFilters(),
    ])
    await Promise.all([
        fetchBookingUsers(true),
        fetchBookingCars(),
    ])
    addBookingModalOpen.value = true
}

const handleCreateCar = async (form: CarForm) => {
    const result = await createCar(form)
    if (!result.success) return

    addCarModalOpen.value = false
    window.location.reload()
}

const handleCreateBooking = async (form: BookingForm) => {
    const result = await createBooking(form)
    if (!result.success) return

    addBookingModalOpen.value = false
    window.location.reload()
}

const handleCreateUser = async ({
    body,
    idFiles,
}: {
    body: AdminCreateUserFormPayload
    idFiles: File[]
}) => {
    const result = await createUser(body, idFiles)
    if (!result.success) return

    addUserModalOpen.value = false
    await loadStats()
}

const handleAttentionLoaded = (value: boolean) => {
    hasAttention.value = value
    attentionResolved.value = true
}

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

const { fetchStats } = useDashboard()
const statCards = ref<StatCard[]>([])

/* =========================
   STAT CARDS
========================= */

const formatChange = (value: number | null) => {
    if (value === null) return 'New'
    return `${value >= 0 ? '+' : ''}${value}%`
}

const formatCurrency = (value: number) =>
    new Intl.NumberFormat('en-PH', {
        style: 'currency',
        currency: 'PHP',
        notation: 'compact',
    }).format(value)

const loadStats = async () => {
    const stats = await fetchStats(selectedRevenueMonth.value)
    statCards.value = [
        {
            label: 'Bookings',
            value: String(stats.total_bookings),
            change: formatChange(stats.bookings_change),
            positive: stats.bookings_change === null
                || stats.bookings_change >= 0,
            icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
        },

        {
            label: 'Revenue',
            value: formatCurrency(stats.total_revenue),
            change: formatChange(stats.revenue_change),
            positive: stats.revenue_change === null
                || stats.revenue_change >= 0,
            icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
        },

        {
            label: 'Active rentals',
            value: String(stats.active_rentals),
            change: 'Current',
            positive: true,
            icon: 'M13 10V3L4 14h7v7l9-11h-7z',
        },

        {
            label: 'Customers',
            value: String(stats.customers),
            change: formatChange(stats.customers_change),
            positive: stats.customers_change === null
                || stats.customers_change >= 0,
            icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z',
        },
    ]
}

onMounted(loadStats)

const currentMonth = new Date()
const selectedRevenueMonth = ref(
    `${currentMonth.getFullYear()}-${String(currentMonth.getMonth() + 1).padStart(2, '0')}`
)

watch(selectedRevenueMonth, loadStats)

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
   ADMIN PAGE CLASS
========================= */

onMounted(() => {
    document.documentElement.classList.add('admin-page')
})

onBeforeUnmount(() => {
    document.documentElement.classList.remove('admin-page')
})
</script>
