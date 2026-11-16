<template>
    <div class="flex h-screen overflow-hidden bg-[#0D0D0D] font-[poppins] text-white">
        <AdminCommonSidebarNav
            :sidebar-open="sidebarOpen"
            @close-sidebar="sidebarOpen = false"
        />

        <div class="flex min-w-0 flex-1 flex-col overflow-hidden">
            <AdminCommonTopbarNav
                :user="user"
                title="Analytics"
                :subtitle="currentDate"
                :is-logged-in="isLoggedIn"
                @open-sidebar="sidebarOpen = true"
                @close-sidebar="sidebarOpen = false"
            />

            <main class="min-h-0 flex-1 overflow-y-auto px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
                <div class="mb-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
                    <div>
                        <h1 class="text-xl font-extrabold text-white sm:text-[22px]">Analytics</h1>
                        <p class="mt-1 text-xs text-[#8a8a8a] sm:text-[13px]">
                            Track business performance and rental trends
                        </p>
                    </div>

                    <div class="relative w-full sm:w-44">
                        <select
                            v-model="selectedPeriod"
                            aria-label="Analytics period"
                            class="w-full appearance-none rounded-lg border border-[#292929] bg-[#1a1a1a] py-2.5 pl-3.5 pr-9 text-sm text-gray-300 outline-none transition hover:bg-[#222] focus:border-[#C1121F]"
                        >
                            <option value="30">Last 30 days</option>
                            <option value="90">Last 3 months</option>
                            <option value="180">Last 6 months</option>
                            <option value="365">Last 12 months</option>
                        </select>
                        <svg class="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[#8a8a8a]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m6 9 6 6 6-6" />
                        </svg>
                    </div>
                </div>

                <AdminDashboardStats :stat-cards="stats" />

                <div class="mb-6 grid grid-cols-1 gap-4 xl:grid-cols-3">

                    <AdminAnalyticsRevenueOverview :period="selectedPeriod" />

                    <AdminAnalyticsStatusDistribution :period="selectedPeriod" />

                </div>

                <div class="grid grid-cols-1 gap-4 xl:grid-cols-2">
                    <AdminAnalyticsTopPerformingVehicles :period="selectedPeriod" />
                    <AdminAnalyticsCustomerInsights :period="selectedPeriod" />
                </div>
            </main>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { StatCard } from '~/utils/types/dashboard'

const { isLoggedIn } = useAuth()
const { user } = useCurrentUser()
const { loadStats: fetchAdminStats } = useAnalyticsList()

const sidebarOpen = ref(false)
const selectedPeriod = ref('30')
const stats = ref<StatCard[]>([])
const statsRequestId = ref(0)

const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
})

const loadStats = async () => {
    const currentRequest = ++statsRequestId.value

    try {
        const result = await fetchAdminStats(
            selectedPeriod.value,
            currentRequest,
            () => currentRequest === statsRequestId.value
        )

        if (result) {
            stats.value = result
        }
    } catch {
        if (currentRequest === statsRequestId.value) {
            stats.value = []
        }
    }
}

watch(selectedPeriod, loadStats)

onMounted(() => {
    document.documentElement.classList.add('admin-page')
    loadStats()
})
onBeforeUnmount(() => document.documentElement.classList.remove('admin-page'))
</script>
