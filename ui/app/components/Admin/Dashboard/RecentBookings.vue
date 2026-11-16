<template>
    <div class="rounded-xl border border-[#222] bg-[#1a1a1a] p-6 xl:col-span-2">
        <div class="mb-5 flex items-center justify-between">
            <div>
                <h2 class="text-base font-bold text-white">Recent bookings</h2>
                <p class="mt-1 text-xs text-gray-500">Latest rental activity</p>
            </div>
            <NuxtLink to="/admin/admin-booking" class="text-xs font-semibold text-[#C1121F] hover:text-red-400">
                View all
            </NuxtLink>
        </div>

        <div v-if="loading" class="flex h-40 items-center justify-center text-xs text-gray-500">
            Loading recent bookings...
        </div>
        <div v-else-if="error" class="flex h-40 items-center justify-center text-xs text-red-400">
            {{ error }}
        </div>
        <div v-else-if="bookings.length" class="overflow-x-auto">
            <table class="w-full min-w-[600px]">
                <thead>
                    <tr class="border-b border-[#292929] text-left text-[10px] uppercase tracking-wide text-gray-500">
                        <th class="pb-3 font-medium">Booking</th>
                        <th class="pb-3 font-medium">Customer</th>
                        <th class="pb-3 font-medium">Vehicle</th>
                        <th class="pb-3 font-medium">Amount</th>
                        <th class="pb-3 font-medium">Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="booking in bookings" :key="booking.booking_reference" class="border-b border-[#222] last:border-0">
                        <td class="py-4 text-xs font-semibold text-white">{{ booking.booking_reference }}</td>
                        <td class="py-4 text-xs text-gray-400">{{ booking.customer }}</td>
                        <td class="py-4 text-xs text-gray-400">{{ booking.vehicle }}</td>
                        <td class="py-4 text-xs text-white">{{ formatCurrency(booking.amount) }}</td>
                        <td class="py-4">
                            <span :class="['rounded-full px-2.5 py-1 text-[10px] font-semibold', statusClass(booking.status)]">
                                {{ booking.status_label }}
                            </span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p v-else class="flex h-40 items-center justify-center text-xs text-gray-500">
            No bookings found.
        </p>
    </div>
</template>

<script setup lang="ts">
import type { DashboardRecentBooking } from '~/utils/types/dashboard'

const { fetchRecentBookings } = useDashboard()
const bookings = ref<DashboardRecentBooking[]>([])
const loading = ref(false)
const error = ref('')

const formatCurrency = (value: number) => new Intl.NumberFormat('en-PH', {
    style: 'currency', currency: 'PHP', maximumFractionDigits: 0,
}).format(value)

const statusClass = (status: string) => {
    if (['confirmed', 'picked_up'].includes(status)) return 'bg-green-400/10 text-green-400'
    if (['pending_payment', 'pending_approval'].includes(status)) return 'bg-yellow-400/10 text-yellow-400'
    if (['cancelled', 'rejected'].includes(status)) return 'bg-red-400/10 text-red-400'
    return 'bg-gray-400/10 text-gray-400'
}

const loadRecentBookings = async () => {
    loading.value = true
    error.value = ''
    try {
        bookings.value = (await fetchRecentBookings()).bookings
    } catch (fetchError) {
        console.error('Failed to load recent bookings:', fetchError)
        error.value = 'Unable to load recent bookings.'
    } finally {
        loading.value = false
    }
}

onMounted(loadRecentBookings)
</script>
