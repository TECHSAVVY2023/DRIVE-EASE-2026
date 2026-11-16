<template>
    <section class="h-full rounded-xl border border-[#222] bg-[#1a1a1a] p-5 sm:p-6">
        <div class="mb-5">
            <h2 class="text-base font-bold">Top performing vehicles</h2>
            <p class="mt-1 text-xs text-gray-500">
                Ranked by completed bookings for {{ data?.label.toLowerCase() || 'the selected period' }}
            </p>
        </div>

        <div v-if="loading" class="flex min-h-40 items-center justify-center text-xs text-gray-500">
            Loading vehicle performance...
        </div>

        <div v-else-if="error" class="flex min-h-40 items-center justify-center text-sm text-red-400">
            {{ error }}
        </div>

        <div v-else-if="vehicles.length" class="space-y-4">
            <div
                v-for="(vehicle, index) in vehicles"
                :key="vehicle.car_reference"
                class="flex items-center gap-3"
            >
                <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-[#252525] text-xs font-bold text-gray-400">
                    {{ index + 1 }}
                </span>
                <div class="min-w-0 flex-1">
                    <div class="mb-2 flex justify-between gap-3 text-xs">
                        <span class="truncate font-semibold text-gray-200">{{ vehicle.name }}</span>
                        <span class="shrink-0 text-gray-400">
                            {{ vehicle.bookings }} {{ vehicle.bookings === 1 ? 'booking' : 'bookings' }}
                        </span>
                    </div>
                    <div class="h-1.5 overflow-hidden rounded-full bg-[#2a2a2a]">
                        <div
                            class="h-full rounded-full bg-[#C1121F] transition-[width] duration-300"
                            :style="{ width: `${vehicle.score}%` }"
                        />
                    </div>
                </div>
            </div>
        </div>

        <div v-else class="flex min-h-40 items-center justify-center text-center text-xs text-gray-500">
            No completed bookings in this period.
        </div>
    </section>
</template>

<script setup lang="ts">
import type {
    AnalyticsTopVehicle,
    AnalyticsTopVehiclesResponse,
} from '~/utils/types/analytics'

const props = defineProps<{ period: string }>()
const { fetchTopVehicles } = useAnalytics()
const data = ref<AnalyticsTopVehiclesResponse | null>(null)
const vehicles = computed<AnalyticsTopVehicle[]>(() => data.value?.vehicles || [])
const loading = ref(false)
const error = ref('')
let requestId = 0

const loadVehicles = async () => {
    const currentRequest = ++requestId
    loading.value = true
    error.value = ''

    try {
        const response = await fetchTopVehicles(props.period)
        if (currentRequest === requestId) data.value = response
    } catch (fetchError) {
        console.error('Failed to load top performing vehicles:', fetchError)
        if (currentRequest === requestId) {
            data.value = null
            error.value = 'Unable to load vehicle performance.'
        }
    } finally {
        if (currentRequest === requestId) loading.value = false
    }
}

onMounted(loadVehicles)
watch(() => props.period, loadVehicles)
</script>
