<template>
    <div class="mx-auto max-w-6xl grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6 items-start">

        <!-- MAIN CARD -->
        <div class="lg:col-span-2 bg-[#141417] border border-white/10 rounded-2xl p-5 sm:p-6">

            <!-- Header -->
            <div class="flex items-start justify-between gap-4">

                <div class="flex items-center gap-4">
                    <img
                        :src="props.booking?.car.image"
                        :alt="`${props.booking?.car.brand} ${props.booking?.car.model}`"
                        class="h-16 w-20 sm:h-18 sm:w-22 rounded-xl object-cover shrink-0"
                    />
                    <div>
                        <h1 class="text-lg sm:text-xl font-semibold text-white">{{ props.booking?.car.brand }} {{ props.booking?.car.model }}</h1>
                        <p class="text-sm text-gray-400 mt-0.5">₱{{ props.booking?.daily_rate }} / day</p>
                    </div>
                </div>

            </div>

            <div class="h-px bg-white/10 my-5"></div>

            <!-- Renter Information -->
            <section>
                <h2 class="text-xs font-semibold tracking-wider text-gray-500 uppercase">Renter Information</h2>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-4 mt-4">
                    <div>
                        <p class="text-xs text-gray-500">Name</p>
                        <p class="text-sm font-medium text-white mt-1">{{ props.booking?.user.first_name }} {{ props.booking?.user.last_name }}</p>
                    </div>
                    <div>
                        <p class="text-xs text-gray-500">Contact</p>
                        <p class="text-sm font-medium text-white mt-1">{{ props.booking?.user.contact_number }}</p>
                    </div>
                    <div>
                        <p class="text-xs text-gray-500">Address</p>
                        <p class="text-sm font-medium text-white mt-1">{{ props.booking?.user.address }}</p>
                    </div>
                    <div>
                        <p class="text-xs text-gray-500">Duration</p>
                        <p class="text-sm font-medium text-white mt-1">{{ props.booking?.number_of_days }} day(s)</p>
                    </div>
                </div>
            </section>

            <div class="h-px bg-white/10 my-5"></div>

            <!-- Schedule -->
            <section>
                <h2 class="text-xs font-semibold tracking-wider text-gray-500 uppercase">Schedule</h2>
                <div class="mt-4 space-y-3">
                    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
                        <p class="text-xs text-gray-500 sm:w-20 shrink-0">Pickup</p>
                        <p class="text-sm font-medium text-white sm:text-right">
                            {{ formatDateTime(props.booking?.pickup_date) }} &middot; {{ props.booking?.pickup_location }}
                        </p>
                    </div>
                    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
                        <p class="text-xs text-gray-500 sm:w-20 shrink-0">Return</p>
                        <p class="text-sm font-medium text-white sm:text-right">
                            {{ formatDateTime(props.booking?.return_date) }} &middot; {{ props.booking?.return_location }}
                        </p>
                    </div>
                </div>
            </section>

            <div class="h-px bg-white/10 my-5"></div>

            <!-- Uploaded IDs -->
            <section>

                <h2 class="text-xs font-semibold tracking-wider text-gray-500 uppercase">Uploaded IDs</h2>
                <div class="mt-4 space-y-2">
                    <div
                    v-for="doc in documents"
                    :key="doc.name"
                    class="flex items-center justify-between bg-white/5 rounded-lg px-4 py-3"
                    >
                    <div class="flex items-center gap-3 min-w-0">
                        <svg class="h-4 w-4 text-gray-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                        </svg>
                        <span class="text-sm text-gray-300 truncate">{{ doc.name }}</span>
                    </div>
                    <button
                        type="button"
                        class="text-sm font-medium text-red-500 hover:text-red-400 transition-colors shrink-0"
                        @click="viewDocument(doc)"
                    >
                        View
                    </button>
                    </div>
                </div>

            </section>

            <!-- Expand toggle -->
            <div class="flex justify-center mt-5">
                <button
                    type="button"
                    class="h-8 w-8 flex items-center justify-center rounded-full bg-white/5 hover:bg-white/10 transition-colors"
                    :aria-expanded="expanded"
                    aria-label="Toggle details"
                    @click="expanded = !expanded"
                >
                    <svg
                    class="h-4 w-4 text-gray-400 transition-transform"
                    :class="{ 'rotate-180': expanded }"
                    fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"
                    >
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                    </svg>
                </button>
            </div>
        </div>

        <!-- SIDEBAR -->
        <div class="flex flex-col gap-4 sm:gap-6">

            <!-- Status -->
            <div class="bg-[#141417] border border-white/10 rounded-2xl p-5 sm:p-6">
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
            <div class="bg-[#141417] border border-white/10 rounded-2xl p-5 sm:p-6">
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
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Transaction } from '~/utils/api/api'

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