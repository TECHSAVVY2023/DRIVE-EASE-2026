<template>
    <section class="h-full rounded-xl border border-[#222] bg-[#1a1a1a] p-5 sm:p-6">
        <div class="mb-5">
            <h2 class="text-base font-bold">Customer insights</h2>
            <p class="mt-1 text-xs text-gray-500">
                Rental behavior for {{ data?.label.toLowerCase() || 'the selected period' }}
            </p>
        </div>

        <div v-if="loading" class="flex min-h-40 items-center justify-center text-xs text-gray-500">
            Loading customer insights...
        </div>

        <div v-else-if="error" class="flex min-h-40 items-center justify-center text-sm text-red-400">
            {{ error }}
        </div>

        <div v-else class="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div
                v-for="insight in customerInsights"
                :key="insight.label"
                class="rounded-lg border border-[#292929] bg-[#151515] p-4"
            >
                <p class="text-[11px] text-gray-500">{{ insight.label }}</p>
                <p class="mt-2 text-xl font-extrabold">{{ insight.value }}</p>
                <p class="mt-1 text-[10px] text-gray-500">{{ insight.note }}</p>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import type { AnalyticsCustomerInsightsResponse } from '~/utils/types/analytics'

const props = defineProps<{ period: string }>()
const { fetchCustomerInsights } = useAnalytics()
const data = ref<AnalyticsCustomerInsightsResponse | null>(null)
const loading = ref(false)
const error = ref('')
let requestId = 0

const formatCurrency = (value: number) =>
    new Intl.NumberFormat('en-PH', {
        style: 'currency',
        currency: 'PHP',
        maximumFractionDigits: 0,
    }).format(value)

const formatPercentage = (value: number) => `${value.toFixed(1)}%`

const customerInsights = computed(() => [
    {
        label: 'New customers',
        value: String(data.value?.new_customers ?? 0),
        note: `${formatPercentage(data.value?.new_customer_percentage ?? 0)} of completed renters`,
    },
    {
        label: 'Returning customers',
        value: String(data.value?.returning_customers ?? 0),
        note: `${formatPercentage(data.value?.return_rate ?? 0)} return rate`,
    },
    {
        label: 'Average rental',
        value: `${(data.value?.average_rental_days ?? 0).toFixed(1)} days`,
        note: 'Per completed rental',
    },
    {
        label: 'Average booking',
        value: formatCurrency(data.value?.average_booking_value ?? 0),
        note: 'Per completed rental',
    },
])

const loadCustomerInsights = async () => {
    const currentRequest = ++requestId
    loading.value = true
    error.value = ''

    try {
        const response = await fetchCustomerInsights(props.period)
        if (currentRequest === requestId) data.value = response
    } catch (fetchError) {
        console.error('Failed to load customer insights:', fetchError)
        if (currentRequest === requestId) {
            data.value = null
            error.value = 'Unable to load customer insights.'
        }
    } finally {
        if (currentRequest === requestId) loading.value = false
    }
}

onMounted(loadCustomerInsights)
watch(() => props.period, loadCustomerInsights)
</script>
