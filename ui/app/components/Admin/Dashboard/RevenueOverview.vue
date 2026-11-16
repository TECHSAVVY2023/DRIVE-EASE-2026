<template>
    <div class="rounded-xl border border-[#222] bg-[#1a1a1a] pl-5 pr-5 pt-5 pb-8 sm:pl-6 sm:pr-6 sm:pb-9 xl:col-span-2">
        <div class="mb-8 flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
            <div>
                <h2 class="text-base font-bold text-white">Revenue overview</h2>
                <p class="mt-1 text-xs text-gray-500">
                    Paid revenue for {{ data?.label || selectedMonthLabel }}
                </p>
            </div>

            <div class="sm:text-right">
                <p class="text-xl font-extrabold text-white">
                    {{ loading ? 'Loading…' : formatCurrency(data?.total || 0) }}
                </p>
                <p
                    v-if="!loading && data"
                    class="mt-1 text-xs"
                    :class="data.percentage_change >= 0 ? 'text-green-400' : 'text-red-400'"
                >
                    {{ formatChange(data.percentage_change) }} from last month
                </p>
            </div>
        </div>

        <div v-if="error" class="flex h-64 items-center justify-center text-sm text-red-400">
            {{ error }}
        </div>

        <div v-else class="flex h-64 gap-3 sm:gap-5" aria-label="Weekly revenue chart">
            <div class="flex w-8 shrink-0 flex-col justify-between pb-6 text-right text-[10px] text-gray-600">
                <span v-for="label in yAxisLabels" :key="label">
                    {{ formatAxisCurrency(label) }}
                </span>
            </div>

            <div class="relative flex min-w-0 flex-1 items-end justify-around gap-2 border-b border-l border-[#303030] px-2 pt-2 sm:px-5">
                <div class="pointer-events-none absolute inset-0 flex flex-col justify-between">
                    <span
                        v-for="line in 4"
                        :key="line"
                        class="block border-t border-dashed border-white/[0.05]"
                    />
                </div>

                <div
                    v-for="point in chartPoints"
                    :key="point.label"
                    class="relative z-10 flex h-full min-w-0 flex-1 flex-col items-center justify-end gap-2"
                >
                    <div
                        class="group relative flex w-full flex-1 items-end justify-center"
                        :title="`${point.label}: ${formatCurrency(point.value)}`"
                    >
                        <div
                            class="w-full max-w-12 rounded-t-md bg-[#C1121F]/80 transition hover:bg-[#C1121F]"
                            :class="point.value === 0 ? 'min-h-px opacity-30' : ''"
                            :style="{ height: `${barHeight(point.value)}%` }"
                        />
                    </div>
                    <span class="max-w-full truncate text-[10px] text-gray-500">
                        {{ point.label }}
                    </span>
                </div>

                <div
                    v-if="loading"
                    class="absolute inset-0 z-20 flex items-center justify-center bg-[#1a1a1a]/60 text-xs text-gray-500"
                >
                    Loading revenue…
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { DashboardRevenueResponse } from '~/utils/api/api'

const props = defineProps<{
    month: string
}>()

const { fetchRevenue } = useDashboard()

const data = ref<DashboardRevenueResponse | null>(null)
const loading = ref(false)
const error = ref('')
let requestId = 0

const selectedMonthLabel = computed(() => {
    const [year, month] = props.month.split('-').map(Number)
    if (year === undefined || month === undefined) return props.month

    return new Date(year, month - 1, 1).toLocaleDateString('en-US', {
        month: 'long',
        year: 'numeric',
    })
})

const chartPoints = computed(() => data.value?.points || [])
const maximumRevenue = computed(() =>
    Math.max(...chartPoints.value.map(point => point.value), 0)
)
const axisMaximum = computed(() => {
    if (!maximumRevenue.value) return 1000

    const magnitude = 10 ** Math.floor(Math.log10(maximumRevenue.value))
    const interval = magnitude / 2
    return Math.ceil(maximumRevenue.value / interval) * interval
})
const yAxisLabels = computed(() => [
    axisMaximum.value,
    axisMaximum.value * (2 / 3),
    axisMaximum.value * (1 / 3),
    0,
])

const formatCurrency = (value: number) =>
    new Intl.NumberFormat('en-PH', {
        style: 'currency',
        currency: 'PHP',
        maximumFractionDigits: 0,
    }).format(value)

const formatChange = (value: number) =>
    `${value >= 0 ? '+' : ''}${value.toFixed(1)}%`

const formatAxisCurrency = (value: number) => {
    if (value >= 1_000_000) {
        return `₱${(value / 1_000_000).toFixed(1).replace('.0', '')}M`
    }
    if (value >= 1_000) return `₱${Math.round(value / 1_000)}K`
    return `₱${Math.round(value)}`
}

const barHeight = (value: number) => {
    if (!axisMaximum.value || !value) return 0
    return Math.max((value / axisMaximum.value) * 100, 4)
}

const loadRevenue = async () => {
    const currentRequest = ++requestId
    loading.value = true
    error.value = ''

    try {
        const response = await fetchRevenue(props.month)

        if (currentRequest === requestId) {
            data.value = response
        }
    } catch (fetchError) {
        console.error('Failed to load revenue:', fetchError)

        if (currentRequest === requestId) {
            error.value = 'Unable to load revenue data.'
        }
    } finally {
        if (currentRequest === requestId) {
            loading.value = false
        }
    }
}

onMounted(loadRevenue)

watch(
    () => props.month,
    () => loadRevenue(),
)
</script>
