<template>
    <section class="flex h-full flex-col rounded-xl border border-[#222] bg-[#1a1a1a] p-5 sm:p-6">
        <h2 class="text-base font-bold">Booking status distribution</h2>
        <p class="mt-1 text-xs text-gray-500">
            Bookings created in {{ data?.label.toLowerCase() || 'the selected period' }}
        </p>

        <div v-if="loading" class="flex min-h-60 flex-1 items-center justify-center text-xs text-gray-500">
            Loading booking statuses...
        </div>

        <div v-else-if="error" class="flex min-h-60 flex-1 items-center justify-center text-center text-sm text-red-400">
            {{ error }}
        </div>

        <div v-else class="flex flex-1 flex-col items-center justify-center pt-2">
            <div class="flex h-32 w-32 shrink-0 items-center justify-center rounded-full" :style="statusChartStyle">
                <div class="flex h-20 w-20 flex-col items-center justify-center rounded-full bg-[#1a1a1a]">
                    <span class="text-lg font-extrabold">{{ totalBookings }}</span>
                    <span class="text-[12px] text-gray-500">bookings</span>
                </div>
            </div>

            <div
                v-if="visibleBookingStatuses.length"
                class="mt-4 grid w-full grid-cols-1 gap-2 sm:grid-cols-2 xl:grid-cols-2"
            >
                <div
                    v-for="status in visibleBookingStatuses"
                    :key="status.label"
                    class="flex min-w-0 items-center justify-between gap-3 rounded-lg border border-[#292929] bg-[#151515] px-3 py-2 text-[10px]"
                    :class="{ 'sm:col-span-2 xl:col-span-2': visibleBookingStatuses.length === 1 }"
                >
                    <div class="flex min-w-0 items-center gap-2 text-gray-400">
                        <span class="h-2.5 w-2.5 shrink-0 rounded-full" :style="{ backgroundColor: status.color }" />
                        <span class="truncate">{{ status.label }}</span>
                    </div>
                    <span class="shrink-0 font-semibold">{{ status.value }}%</span>
                </div>
            </div>

            <p v-else class="mt-4 text-center text-xs text-gray-500">
                No booking data yet
            </p>
        </div>
    </section>
</template>

<script setup lang="ts">
import type { AnalyticsStatusDistributionResponse } from '~/utils/types/analytics'

const props = defineProps<{ period: string }>()
const { fetchStatusDistribution } = useAnalytics()
const data = ref<AnalyticsStatusDistributionResponse | null>(null)
const loading = ref(false)
const error = ref('')
let requestId = 0

const totalBookings = computed(() => data.value?.total ?? 0)

const statusColors: Record<string, string> = {
    pending_payment: '#F8B4BA',
    payment_failed: '#F28B94',
    pending_approval: '#EA626E',
    confirmed: '#E13F4D',
    rejected: '#D62B39',
    picked_up: '#CD1E2C',
    returned: '#C71926',
    completed: '#C1121F',
    cancelled: '#7F0C14',
}

const bookingStatuses = computed(() =>
    (data.value?.status_distribution || []).map(status => ({
        status: status.status,
        label: status.label,
        value: status.percentage,
        count: status.count,
        color: statusColors[status.status] ?? '#888888',
    }))
)

const visibleBookingStatuses = computed(() =>
    bookingStatuses.value.filter(status =>
        status.count > 0 || status.status === 'cancelled'
    )
)

// Zero-value statuses are useful in the legend, but should not become chart segments.
const chartBookingStatuses = computed(() =>
    bookingStatuses.value.filter(status => status.count > 0)
)

const statusChartStyle = computed(() => {
    const visibleStatuses = chartBookingStatuses.value

    if (!visibleStatuses.length) {
        return { background: '#2a2a2a' }
    }

    let start = 0
    const segments = visibleStatuses.map((status, index) => {
        const end = index === visibleStatuses.length - 1
            ? 100
            : Math.min(start + status.value, 100)
        const segment = `${status.color} ${start}% ${end}%`
        start = end
        return segment
    })

    return {
        background: `conic-gradient(${segments.join(', ')})`,
    }
})

const loadStatusDistribution = async () => {
    const currentRequest = ++requestId
    loading.value = true
    error.value = ''

    try {
        const response = await fetchStatusDistribution(props.period)
        if (currentRequest === requestId) data.value = response
    } catch (fetchError) {
        console.error('Failed to load booking status distribution:', fetchError)
        if (currentRequest === requestId) {
            data.value = null
            error.value = 'Unable to load booking status distribution.'
        }
    } finally {
        if (currentRequest === requestId) loading.value = false
    }
}

onMounted(loadStatusDistribution)
watch(() => props.period, loadStatusDistribution)
</script>
