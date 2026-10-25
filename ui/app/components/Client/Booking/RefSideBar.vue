<template>
    <!-- SIDEBAR -->
    <div class="flex flex-col gap-4 sm:gap-6">

        <!-- Status -->
        <div class="smoked-charcoal-panel rounded-2xl p-5 sm:p-6">
            <h2 class="text-xs font-semibold tracking-wider text-gray-500 uppercase">
                Status
            </h2>

            <ul class="mt-4">
                <li
                    v-for="(step, idx) in statusSteps"
                    :key="step.label"
                    class="relative flex gap-3 pb-5 last:pb-0"
                >
                    <!-- Line -->
                    <span
                        v-if="idx !== statusSteps.length - 1"
                        class="absolute left-[5px] top-3 bottom-0 w-px"
                        :class="step.state !== 'pending'
                            ? 'bg-white/15'
                            : 'bg-white/5'"
                    ></span>

                    <!-- Dot -->
                    <span
                        class="relative z-10 mt-1 h-2.5 w-2.5 shrink-0 rounded-full"
                        :class="dotClass(step.state)"
                    ></span>

                    <!-- Content -->
                    <div>
                        <p
                            class="text-sm font-medium"
                            :class="step.state === 'pending'
                                ? 'text-gray-500'
                                : 'text-white'"
                        >
                            {{ step.label }}
                        </p>

                        <p class="mt-0.5 text-xs text-gray-500">
                            {{ step.timestamp ? formatDateTime(step.timestamp) : '—' }}
                        </p>
                    </div>
                </li>
            </ul>
        </div>

        <!-- Payment -->
        <div class="smoked-charcoal-panel rounded-2xl p-5 sm:p-6">

            <h2 class="text-xs font-semibold tracking-wider text-gray-500 uppercase">Payment</h2>
            <div class="mt-4 space-y-3">
                <div class="flex items-center justify-between text-sm">
                    <span class="text-gray-400">Rate &times; {{ props.booking?.number_of_days }} days</span>
                    <span class="text-white">₱{{ props.booking?.daily_rate }}</span>
                </div>
            </div>

            <div class="h-px bg-white/10 my-4"></div>

            <div class="flex items-center justify-between">
                <span class="text-sm font-semibold text-white">Total paid</span>
                <span class="text-base font-bold text-white">₱{{ props.booking?.total_price }}</span>
            </div>
            <div class="flex items-center gap-2 mt-2">
                <span class="h-2 w-2 rounded-full bg-emerald-500"></span>
                <span class="text-sm font-medium text-emerald-500">Paid in full</span>
            </div>
            
            <div class="flex flex-col mt-5 gap-2">
                <button
                    type="button"
                    class="w-full rounded-xl bg-red-600 hover:bg-red-500 transition-colors text-white font-semibold py-3 text-sm"
                    @click="$emit('download-receipt')"
                    >
                    Download receipt
                </button>

                <button
                    type="button"
                    class="w-full rounded-xl border border-white/15 bg-transparent hover:border-white/30 hover:bg-white/5 transition-colors text-white font-medium py-3 text-sm"
                    @click="$emit('cancel-booking')"
                    >
                    Cancel booking
                </button>
            </div>

        </div>

    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Transaction } from '~/utils/types/booking'

defineEmits(['download-receipt', 'cancel-booking'])

const props = defineProps<{
    booking: Transaction | null
}>()

const expanded = ref(false)

const formatDateTime = (date: string | null | undefined) => {
    if (!date) return null

    return new Date(date).toLocaleString('en-PH', {
        month: 'long',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
    })
}

const statusSteps = computed(() => {
    if (!props.booking) return []

    const booking = props.booking

    if (booking.status === 'cancelled') {
        return [
            {
                label: 'Cancelled',
                status: 'cancelled',
                timestamp: booking.cancelled_at,
                state: 'cancelled',
            },
        ]
    }

    const steps = [
        {
            label: 'Pending Approval',
            status: 'pending_approval',
            timestamp: booking.pending_approval_at,
        },
        {
            label: 'Confirmed',
            status: 'confirmed',
            timestamp: booking.confirmed_at,
        },
        {
            label: 'Picked Up',
            status: 'picked_up',
            timestamp: booking.picked_up_at,
        },
        {
            label: 'Returned',
            status: 'returned',
            timestamp: booking.returned_at,
        },
        {
            label: 'Completed',
            status: 'completed',
            timestamp: booking.completed_at,
        },
    ]

    const currentIndex = steps.findIndex(step => !step.timestamp)

    return steps.map((step, index) => ({
        ...step,
        state: step.timestamp
            ? 'done'
            : index === currentIndex
                ? 'active'
                : 'pending',
    }))
})

const booking = {
    durationDays: 2,
    pickup: { date: 'May 10, 2026, 9:00 AM', location: 'CDO Main Branch' },
    return: { date: 'May 12, 2026, 9:00 AM', location: 'CDO Main Branch' },
}

const payment = {
    rateTotal: 2200,
    serviceFee: 100,
    total: 2300,
}

const documents = [
    { name: 'drivers_license_front.jpg', url: '#' },
    { name: 'postal_id_back.jpg', url: '#' },
]

function dotClass(state: string): string {
    if (state === 'done') return 'bg-emerald-500'

    if (state === 'active') return 'bg-yellow-500'

    if (state === 'cancelled') return 'bg-[#C1121F]'

    return 'bg-white/15'
}

function formatMoney(value: number): string {
    return value.toLocaleString('en-PH', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    })
}

function viewDocument(doc: { url?: string }): void {
    if (doc.url && doc.url !== '#') {
        window.open(doc.url, '_blank')
    }
}

</script>
