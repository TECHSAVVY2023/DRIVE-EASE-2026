<template>
    <div class="flex flex-col gap-4 sm:gap-6">
        <div class="smoked-charcoal-panel rounded-2xl p-5 sm:p-6">
            <h2 class="text-xs font-semibold uppercase tracking-wider text-gray-500">
                Status
            </h2>

            <ul class="mt-4">
                <li
                    v-for="(step, index) in statusSteps"
                    :key="step.label"
                    class="relative flex gap-3 pb-5 last:pb-0"
                >
                    <span
                        v-if="index !== statusSteps.length - 1"
                        class="absolute bottom-0 left-[5px] top-3 w-px"
                        :class="step.state !== 'pending' ? 'bg-white/15' : 'bg-white/5'"
                    />

                    <span
                        class="relative z-10 mt-1 h-2.5 w-2.5 shrink-0 rounded-full"
                        :class="dotClass(step.state)"
                    />

                    <div>
                        <p
                            class="text-sm font-medium"
                            :class="step.state === 'pending' ? 'text-gray-500' : 'text-white'"
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

        <div class="smoked-charcoal-panel overflow-hidden rounded-2xl">
            <div class="p-5 sm:p-6">
                <div class="flex items-center justify-between gap-3">
                    <h2 class="text-xs font-semibold uppercase tracking-wider text-gray-500">
                        Payment summary
                    </h2>
                    <span
                        class="inline-flex min-h-6 items-center justify-center rounded-full px-2.5 py-1 text-center text-[10px] font-semibold leading-none"
                        :class="paymentStatusClass"
                    >
                        {{ paymentStatusLabel }}
                    </span>
                </div>

                <div class="mt-5 space-y-3">
                    <div class="flex items-center justify-between gap-4 text-sm">
                        <span class="text-gray-400">
                            ₱{{ formatMoney(booking?.daily_rate ?? 0) }} ×
                            {{ booking?.number_of_days ?? 0 }} days
                        </span>
                        <span class="font-medium text-white">
                            ₱{{ formatMoney(booking?.subtotal ?? 0) }}
                        </span>
                    </div>

                    <div
                        v-if="Number(booking?.discount ?? 0) > 0"
                        class="flex items-center justify-between gap-4 text-sm"
                    >
                        <span class="text-gray-400">Discount</span>
                        <span class="font-medium text-emerald-400">
                            −₱{{ formatMoney(booking?.discount ?? 0) }}
                        </span>
                    </div>
                </div>

                <div class="my-4 h-px bg-white/10" />

                <div class="flex items-end justify-between gap-4">
                    <span class="text-sm font-semibold text-white">
                        {{ ['paid', 'refunded'].includes(booking?.payment_status ?? '') ? 'Total paid' : 'Total amount' }}
                    </span>
                    <span class="text-lg font-extrabold text-white">
                        ₱{{ formatMoney(booking?.total_price ?? 0) }}
                    </span>
                </div>
            </div>

            <div
                v-if="canCancel"
                class="border-t border-white/10 bg-[#C1121F]/[0.045] p-5 sm:p-6"
            >
                <p class="text-sm font-semibold text-white">Need to cancel?</p>
                <p class="mt-1 text-xs leading-5 text-gray-400">
                    Cancelling releases your reserved dates. Paid bookings may require refund review by Drive Ease.
                </p>
                <button
                    type="button"
                    :disabled="cancelling"
                    class="mt-4 w-full rounded-xl bg-[#C1121F] py-3 text-sm font-semibold text-white transition-colors hover:bg-[#9B0E18] disabled:cursor-not-allowed disabled:opacity-60"
                    @click="emit('cancel-booking')"
                >
                    {{ cancelling ? 'Cancelling booking...' : 'Cancel booking' }}
                </button>
            </div>

            <div
                v-else-if="booking?.status === 'cancelled'"
                class="border-t border-[#C1121F]/20 bg-[#C1121F]/[0.045] p-5 sm:p-6"
            >
                <p class="text-xs font-semibold uppercase tracking-wider text-[#E63946]">
                    Cancellation reason
                </p>
                <p class="mt-2 text-sm leading-6 text-gray-300">
                    {{ booking.cancel_reason || 'No reason was provided.' }}
                </p>

                <div
                    v-if="booking.refund"
                    class="mt-4 rounded-xl border border-white/10 bg-black/20 p-4"
                >
                    <div class="flex items-center justify-between gap-3">
                        <p class="text-xs font-semibold text-white">Refund</p>
                        <span
                            class="rounded-full px-2.5 py-1 text-[10px] font-semibold"
                            :class="refundStatusClass"
                        >
                            {{ refundStatusLabel }}
                        </span>
                    </div>
                    <p class="mt-2 text-sm font-bold text-white">
                        &#8369;{{ formatMoney(booking.refund.amount) }}
                    </p>
                    <p class="mt-1 text-xs leading-5 text-gray-400">
                        {{ refundStatusMessage }}
                    </p>
                    <p
                        v-if="booking.refund.processed_at"
                        class="mt-2 text-xs text-gray-500"
                    >
                        Completed {{ formatDateTime(booking.refund.processed_at) }}
                    </p>
                </div>

                <p
                    v-else-if="booking.refund_unavailable_reason"
                    class="mt-4 rounded-xl border border-white/10 bg-black/20 p-4 text-xs leading-5 text-gray-400"
                >
                    {{ booking.refund_unavailable_reason }}
                </p>
            </div>

            <div
                v-else-if="booking"
                class="border-t border-white/10 px-5 py-4 text-xs leading-5 text-gray-500 sm:px-6"
            >
                This booking can no longer be cancelled online. Contact Drive Ease if you need assistance.
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Transaction } from '~/utils/types/booking'

const props = withDefaults(defineProps<{
    booking: Transaction | null
    cancelling?: boolean
}>(), {
    cancelling: false,
})

const emit = defineEmits<{
    'cancel-booking': []
}>()

const cancellableStatuses = [
    'pending_payment',
    'payment_failed',
    'pending_approval',
    'confirmed',
]

const canCancel = computed(() => {
    if (!props.booking || !cancellableStatuses.includes(props.booking.status)) {
        return false
    }

    return !(
        props.booking.status === 'confirmed' &&
        new Date(props.booking.pickup_date) <= new Date()
    )
})

const paymentStatusLabel = computed(() => {
    const labels: Record<string, string> = {
        paid: 'Paid',
        pending: 'Pending',
        failed: 'Failed',
        refunded: 'Refunded',
    }
    return labels[props.booking?.payment_status ?? ''] ?? 'Not recorded'
})

const paymentStatusClass = computed(() => {
    const classes: Record<string, string> = {
        paid: 'bg-emerald-500/10 text-emerald-400',
        pending: 'bg-amber-500/10 text-amber-400',
        failed: 'bg-[#C1121F]/10 text-[#E63946]',
        refunded: 'bg-blue-500/10 text-blue-400',
    }
    return classes[props.booking?.payment_status ?? ''] ?? 'bg-white/5 text-gray-400'
})

const refundStatusLabel = computed(() => {
    const labels: Record<string, string> = {
        pending_review: 'Pending review',
        processing: 'Processing',
        succeeded: 'Refunded',
        failed: 'Needs attention',
        rejected: 'Rejected',
    }
    return labels[props.booking?.refund?.status ?? ''] ?? 'Not requested'
})

const refundStatusClass = computed(() => {
    const classes: Record<string, string> = {
        pending_review: 'bg-amber-500/10 text-amber-400',
        processing: 'bg-blue-500/10 text-blue-400',
        succeeded: 'bg-emerald-500/10 text-emerald-400',
        failed: 'bg-[#C1121F]/10 text-[#E63946]',
        rejected: 'bg-white/5 text-gray-400',
    }
    return classes[props.booking?.refund?.status ?? ''] ?? 'bg-white/5 text-gray-400'
})

const refundStatusMessage = computed(() => {
    const messages: Record<string, string> = {
        pending_review: 'Drive Ease will review your full refund request.',
        processing: 'PayMongo is processing your refund to the original payment method.',
        succeeded: 'The refund was submitted successfully. Its arrival time depends on your payment method.',
        failed: 'The refund could not be completed. Drive Ease will review it.',
        rejected: 'This refund request was not approved. Contact Drive Ease for assistance.',
    }
    return messages[props.booking?.refund?.status ?? ''] ?? ''
})

const statusSteps = computed(() => {
    if (!props.booking) return []

    if (props.booking.status === 'cancelled') {
        return [{
            label: 'Cancelled',
            timestamp: props.booking.cancelled_at,
            state: 'cancelled',
        }]
    }

    const steps = [
        { label: 'Pending Approval', timestamp: props.booking.pending_approval_at },
        { label: 'Confirmed', timestamp: props.booking.confirmed_at },
        { label: 'Picked Up', timestamp: props.booking.picked_up_at },
        { label: 'Returned', timestamp: props.booking.returned_at },
        { label: 'Completed', timestamp: props.booking.completed_at },
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

function dotClass(state: string): string {
    if (state === 'done') return 'bg-emerald-500'
    if (state === 'active') return 'bg-yellow-500'
    if (state === 'cancelled') return 'bg-[#C1121F]'
    return 'bg-white/15'
}

function formatDateTime(date: string | null | undefined): string {
    if (!date) return ''
    return new Date(date).toLocaleString('en-PH', {
        month: 'long',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
    })
}

function formatMoney(value: number | string): string {
    return Number(value).toLocaleString('en-PH', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    })
}
</script>
