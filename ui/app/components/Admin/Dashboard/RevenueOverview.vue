<template>
    <div class="xl:col-span-2 rounded-xl border border-[#222] bg-[#1a1a1a] p-6">
        <div class="mb-6 flex items-center justify-between gap-4">
            <div>
                <h2 class="text-base font-bold text-white">Revenue overview</h2>
                <p class="mt-1 text-xs text-gray-500">
                    Paid revenue for {{ data?.label || selectedMonthLabel }}
                </p>
            </div>

            <div class="text-right">
                <p class="text-lg font-bold text-white">
                    {{ loading ? 'Loading…' : formatCurrency(data?.total || 0) }}
                </p>
                <p
                    v-if="!loading && data"
                    class="text-xs"
                    :class="data.percentage_change >= 0 ? 'text-green-400' : 'text-red-400'"
                >
                    {{ formatChange(data.percentage_change) }} from last month
                </p>
            </div>
        </div>

        <div v-if="error" class="flex h-56 items-center justify-center text-sm text-red-400">
            {{ error }}
        </div>

        <template v-else>
            <div class="flex h-56 items-end gap-2 sm:gap-4" aria-label="Weekly revenue chart">
                <div
                    v-for="point in chartPoints"
                    :key="point.label"
                    class="flex h-full flex-1 items-end"
                    :title="`${point.label}: ${formatCurrency(point.value)}`"
                >
                    <div
                        class="w-full rounded-t-md bg-[#C1121F]/80 transition hover:bg-[#C1121F]"
                        :class="point.value === 0 ? 'min-h-px opacity-30' : ''"
                        :style="{ height: `${barHeight(point.value)}%` }"
                    />
                </div>
            </div>

            <div class="mt-3 grid text-center text-[10px] text-gray-500" :style="labelGridStyle">
                <span v-for="point in chartPoints" :key="`label-${point.label}`">
                    {{ point.label }}
                </span>
            </div>
        </template>
    </div>
</template>

<script setup lang="ts">
import type { DashboardRevenueResponse } from '~/utils/api/api'

const props = defineProps<{
    month: string
}>()

const { apiFetch } = useApiFetch()
const data = ref<DashboardRevenueResponse | null>(null)
const loading = ref(false)
const error = ref('')
let requestId = 0

const selectedMonthLabel = computed(() => {
    const [year, month] = props.month.split('-').map(Number)
    return new Date(year, month - 1, 1).toLocaleDateString('en-US', {
        month: 'long',
        year: 'numeric',
    })
})

const chartPoints = computed(() => data.value?.points || [])
const maximumRevenue = computed(() =>
    Math.max(...chartPoints.value.map(point => point.value), 0)
)
const labelGridStyle = computed(() => ({
    gridTemplateColumns: `repeat(${Math.max(chartPoints.value.length, 1)}, minmax(0, 1fr))`,
}))

const formatCurrency = (value: number) =>
    new Intl.NumberFormat('en-PH', {
        style: 'currency',
        currency: 'PHP',
        maximumFractionDigits: 0,
    }).format(value)

const formatChange = (value: number) => `${value >= 0 ? '+' : ''}${value.toFixed(1)}%`

const barHeight = (value: number) => {
    if (!maximumRevenue.value || !value) return 0
    return Math.max((value / maximumRevenue.value) * 100, 4)
}

const fetchRevenue = async () => {
    const currentRequest = ++requestId
    loading.value = true
    error.value = ''

    try {
        const response = await apiFetch<DashboardRevenueResponse>(
            `/admin/dashboard/revenue/?month=${encodeURIComponent(props.month)}`
        )

        if (currentRequest === requestId) data.value = response
    } catch (fetchError) {
        console.error('Failed to load dashboard revenue:', fetchError)
        if (currentRequest === requestId) error.value = 'Unable to load revenue data.'
    } finally {
        if (currentRequest === requestId) loading.value = false
    }
}

watch(() => props.month, fetchRevenue, { immediate: true })
</script>
