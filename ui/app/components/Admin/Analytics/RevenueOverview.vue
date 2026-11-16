<template>
    <section class="rounded-xl border border-[#222] bg-[#1a1a1a] p-5 sm:p-6 xl:col-span-2">
        <div class="mb-8 flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
            <div>
                <h2 class="text-base font-bold">Revenue performance</h2>
                <p class="mt-1 text-xs text-gray-500">
                    Paid rental revenue for {{ data?.label.toLowerCase() || 'the selected period' }}
                </p>
            </div>
            <div class="sm:text-right">
                <p class="text-xl font-extrabold">
                    {{ loading ? 'Loading...' : formatCurrency(data?.total || 0) }}
                </p>
                <p
                    v-if="!loading && data"
                    class="mt-1 text-xs"
                    :class="changeIsPositive ? 'text-green-400' : 'text-red-400'"
                >
                    {{ formatChange(data.percentage_change) }} from previous period
                </p>
            </div>
        </div>

        <div v-if="error" class="flex h-64 items-center justify-center text-sm text-red-400">
            {{ error }}
        </div>

        <div v-else class="flex h-64 gap-3 sm:gap-5 mb-2" aria-label="Revenue bar chart">
            <div class="flex w-10 shrink-0 flex-col justify-between pb-6 text-right text-[10px] text-gray-600">
                <span v-for="label in yAxisLabels" :key="label">
                    {{ formatAxisCurrency(label) }}
                </span>
            </div>

            <div class="relative flex min-w-0 flex-1 items-end justify-around gap-1.5 border-b border-l border-[#303030] px-2 pt-2 sm:gap-2 sm:px-3">
                <div class="pointer-events-none absolute inset-0 flex flex-col justify-between">
                    <span v-for="line in 4" :key="line" class="block border-t border-dashed border-white/[0.05]" />
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
                    <span class="max-w-full truncate text-[9px] text-gray-500 sm:text-[10px]">
                        {{ point.label }}
                    </span>
                </div>

                <div
                    v-if="loading"
                    class="absolute inset-0 z-20 flex items-center justify-center bg-[#1a1a1a]/60 text-xs text-gray-500"
                >
                    Loading revenue...
                </div>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import type { AnalyticsRevenueResponse } from '~/utils/types/analytics'

const props = defineProps<{ period: string }>()
const { fetchRevenue } = useAnalytics()
const data = ref<AnalyticsRevenueResponse | null>(null)
const loading = ref(false)
const error = ref('')
let requestId = 0

const chartPoints = computed(() => data.value?.points || [])
const maximumRevenue = computed(() => Math.max(...chartPoints.value.map(point => point.value), 0))
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
const changeIsPositive = computed(() =>
    data.value?.percentage_change === null || (data.value?.percentage_change ?? 0) >= 0
)

const formatCurrency = (value: number) =>
    new Intl.NumberFormat('en-PH', {
        style: 'currency',
        currency: 'PHP',
        maximumFractionDigits: 0,
    }).format(value)

const formatChange = (value: number | null) => {
    if (value === null) return 'New'
    return `${value >= 0 ? '+' : ''}${value.toFixed(1)}%`
}

const formatAxisCurrency = (value: number) => {
    if (value >= 1_000_000) return `\u20B1${(value / 1_000_000).toFixed(1).replace('.0', '')}M`
    if (value >= 1_000) return `\u20B1${Math.round(value / 1_000)}K`
    return `\u20B1${Math.round(value)}`
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
        const response = await fetchRevenue(props.period)
        if (currentRequest === requestId) data.value = response
    } catch (fetchError) {
        console.error('Failed to load analytics revenue:', fetchError)
        if (currentRequest === requestId) error.value = 'Unable to load revenue data.'
    } finally {
        if (currentRequest === requestId) loading.value = false
    }
}

onMounted(loadRevenue)
watch(() => props.period, loadRevenue)
</script>
