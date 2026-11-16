<template>
    <Teleport to="body">
        <Transition
            enter-active-class="transition duration-150"
            leave-active-class="transition duration-100"
            enter-from-class="opacity-0"
            leave-to-class="opacity-0"
        >
            <div
                v-if="open && booking"
                class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 p-4"
                @click.self="close"
            >
                <div
                    class="
                        flex max-h-[90vh] w-full max-w-xl flex-col overflow-hidden 
                        rounded-2xl bg-[#111111] border-t-[#C1121F] border-t-5 shadow-2xl
                    "
                    role="dialog"
                    aria-modal="true"
                >

                    <!-- Header -->
                    <header class="flex items-start justify-between px-4 sm:px-6 pt-5 sm:pt-4 pb-4 border-b border-white/10">
                        
                        <div>
                            
                            <p class="text-[15px] font-medium text-white">
                                Booking details
                            </p>

                            <p class="mt-0.5 text-xs text-neutral-500">
                                Review the details of this booking
                            </p>

                        </div>

                        <button 
                            @click="close" 
                            class="text-white/40 hover:text-white transition-colors mt-0.5"
                        >
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>

                    </header>

                <!-- Body -->
                <div class="flex-1 overflow-y-auto px-5 py-5">

                    <!-- Reference + status -->
                    <div class="mb-6 flex items-start justify-between gap-3">
                        <div class="min-w-0">
                            <p class="truncate text-base font-bold text-white">{{ booking.booking_reference }}</p>
                            <p class="mt-0.5 text-xs text-[#929292]">
                            Booked on {{ fmtDateTime(booking.created_at) }}
                            </p>
                        </div>

                        <span
                            class="shrink-0 rounded-md border px-2.5 py-1 text-xs font-medium capitalize"
                            :class="statusClass(getBookingStatus(booking))"
                        >
                            {{ getBookingStatus(booking) }}
                        </span>
                    </div>

                    <!-- Cancellation details only appear when a reason was recorded. -->
                    <div
                        v-if="booking.cancel_reason"
                        class="mb-6 rounded-xl border border-[#C1121F]/30 bg-[#C1121F]/10 px-4 py-3"
                    >
                        <div class="flex items-start gap-3">
                            <div class="mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-lg bg-[#C1121F] text-white">
                                <svg class="size-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z" />
                                </svg>
                            </div>

                            <div class="min-w-0">
                                <p class="text-xs font-medium text-white">Cancellation reason</p>
                                <p class="mt-1 whitespace-pre-wrap break-words text-sm leading-5 text-neutral-300">
                                    {{ booking.cancel_reason }}
                                </p>
                                <p v-if="booking.cancelled_at" class="mt-1.5 text-[11px] text-neutral-500">
                                    Cancelled on {{ fmtDateTime(booking.cancelled_at) }}
                                </p>
                            </div>
                        </div>
                    </div>

                <!-- Booking -->
                <section :class="detailCard">
                    <p :class="section">Booking details</p>
                    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2">
                        <div>
                        <span :class="label">User</span>
                        <div class="flex items-center gap-3">
                        <UserAvatar
                            :src="booking.user.profile_picture"
                            :alt="`${booking.user.first_name} ${booking.user.last_name}`"
                            class="h-9 w-9"
                        />
                        <div class="min-w-0">
                            <p :class="[value, 'truncate']">{{ booking.user.first_name }} {{ booking.user.last_name }}</p>
                            <p class="truncate text-xs text-[#929292]">{{ booking.user.email }}</p>
                            <p v-if="booking.user.contact_number" class="truncate text-xs text-[#929292]">
                            {{ booking.user.contact_number }}
                            </p>
                        </div>
                        </div>
                        </div>

                        <div>
                        <span :class="label">Car</span>
                        <div class="flex items-center gap-3">
                        <div
                            class="flex size-9 w-12 shrink-0 items-center justify-center overflow-hidden rounded bg-[#1a1a1a]"
                        >
                            <img
                                v-if="booking.car.image"
                                :src="booking.car.image"
                                :alt="`${booking.car.brand} ${booking.car.model}`"
                                class="size-full object-cover"
                            />
                        </div>
                        <div class="min-w-0">
                            <p :class="[value, 'truncate']">
                            {{ booking.car.brand }} {{ booking.car.model }}
                            </p>
                            <p class="text-xs text-[#929292]">{{ booking.car.year }}</p>
                        </div>
                        </div>
                        </div>
                    </div>
                </section>

                <!-- Schedule -->
                <section :class="detailCard">
                    <p :class="section">Rental schedule</p>
                    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2">
                        <div>
                            <span :class="label">Pickup date</span>
                            <p :class="value">{{ fmtDateTime(booking.pickup_date) }}</p>
                        </div>
                        <div>
                            <span :class="label">Pickup location</span>
                            <p :class="value">{{ booking.pickup_location }}</p>
                        </div>
                        <div>
                            <span :class="label">Return date</span>
                            <p :class="value">{{ fmtDateTime(booking.return_date) }}</p>
                        </div>
                        <div>
                            <span :class="label">Return location</span>
                            <p :class="value">{{ booking.return_location }}</p>
                        </div>
                    </div>
                </section>

                <!-- Price -->
                <section :class="detailCard">
                    <p :class="section">Price summary</p>
                    <div class="flex justify-between gap-3 text-sm text-[#929292]">
                        <span>{{ booking.number_of_days }} day(s) × {{ peso(booking.car.price_per_day) }}</span>
                        <span>{{ peso(booking.subtotal) }}</span>
                    </div>
                    <div class="mt-2 flex justify-between gap-3 text-sm">
                        <span class="text-[#929292]">Discount</span>
                        <span class="text-[#C1121F]">-{{ peso(booking.discount) }}</span>
                    </div>
                    <div class="mt-4 flex items-center justify-between gap-3 rounded-lg bg-[#C1121F]/10 px-3 py-2.5">
                        <span class="text-sm text-white">Total</span>
                        <span class="text-lg font-bold text-[#C1121F]">{{ peso(booking.total_price) }}</span>
                    </div>
                </section>

                <!-- Refund -->
                <section
                    v-if="booking.refund || booking.refund_unavailable_reason"
                    :class="detailCard"
                >
                    <div class="flex items-start justify-between gap-3">
                        <div>
                            <p :class="section">Refund</p>
                            <p v-if="booking.refund" class="text-lg font-bold text-white">
                                {{ peso(booking.refund.amount) }}
                            </p>
                        </div>
                        <span
                            v-if="booking.refund"
                            class="rounded-full px-2.5 py-1 text-[10px] font-semibold"
                            :class="refundStatusClass(booking.refund.status)"
                        >
                            {{ refundStatusLabel(booking.refund.status) }}
                        </span>
                    </div>

                    <template v-if="booking.refund">
                        <p class="mt-2 text-xs leading-5 text-neutral-400">
                            Requested {{ fmtDateTime(booking.refund.requested_at) }}
                        </p>
                        <p v-if="booking.refund.admin_note" class="mt-2 text-xs leading-5 text-neutral-300">
                            <span class="text-neutral-500">Admin note:</span>
                            {{ booking.refund.admin_note }}
                        </p>
                        <p v-if="booking.refund.failure_message" class="mt-2 text-xs leading-5 text-red-400">
                            {{ booking.refund.failure_message }}
                        </p>
                    </template>

                    <p
                        v-if="booking.refund_unavailable_reason"
                        class="mt-2 text-xs leading-5 text-neutral-400"
                    >
                        {{ booking.refund_unavailable_reason }}
                    </p>
                </section>

                <!-- Valid IDs -->
                <section class="rounded-xl border border-[#292929] bg-[#171717] p-4">
                    <p :class="section">Valid IDs</p>
                    <div v-if="booking.user.id_images?.images?.length" class="flex flex-col gap-2">
                        <ClientProfileIDImageItems
                            v-for="(url, index) in booking.user.id_images.images"
                            :key="'id-' + index"
                            :url="url"
                            :index="Number(index)"
                        />
                    </div>
                    <p v-else class="text-sm text-neutral-500">No valid IDs uploaded.</p>
                </section>

                <!-- <div v-if="booking.user.id_images?.images?.length" class="grid grid-cols-1 gap-3 sm:grid-cols-2">
                    <a
                        v-for="(url, index) in booking.user.id_images.images"
                        :key="url"
                        :href="url"
                        target="_blank"
                        class="group relative aspect-[16/10] overflow-hidden rounded-lg border border-[#222] bg-[#0f0f0f]"
                    >
                        <img :src="url" :alt="`Valid ID ${index + 1}`" class="size-full object-cover" />
                        <span
                        class="absolute inset-x-0 bottom-0 bg-black/70 px-3 py-1.5 text-xs text-white transition-colors group-hover:text-[#C1121F]"
                        >
                        Valid ID {{ index + 1 }}
                        </span>
                    </a>
                </div>
                <p v-else class="text-sm text-[#929292]">No IDs uploaded.</p> -->

                </div>

                <!-- Footer -->
                <footer class="flex justify-end gap-2.5 border-t border-neutral-800 px-5 py-4">

                    <button
                        class="rounded-lg border border-neutral-700 px-4 py-2 text-xs text-neutral-400 hover:text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-red-600"
                        @click="close"
                        >
                        Cancel
                    </button>

                    <button
                        v-if="booking.can_refund"
                        class="rounded-lg border border-[#C1121F] px-4 py-2 text-xs font-medium text-[#E63946] transition hover:bg-[#C1121F]/10 disabled:cursor-not-allowed disabled:opacity-50"
                        :disabled="refunding"
                        @click="emit('refund', booking)"
                    >
                        {{ refunding ? 'Processing refund...' : 'Issue refund' }}
                    </button>
                    
                    <button
                        class="rounded-lg bg-[#c1121f] px-4 py-2 text-xs font-medium text-white hover:bg-[#b31a27] focus:outline-none focus-visible:ring-2 focus-visible:ring-red-400 disabled:cursor-not-allowed disabled:opacity-50"
                        @click="emit('edit', booking)"
                    >
                        Edit booking
                    </button>

                </footer>

                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup lang="ts">
import type { Transaction } from '~/utils/types/booking'
import { computed } from 'vue'

const open = defineModel<boolean>({ required: true })

const props = withDefaults(defineProps<{
    booking: Transaction | null
    refunding?: boolean
}>(), {
    refunding: false,
})

const emit = defineEmits<{
    edit: [booking: Transaction]
    refund: [booking: Transaction]
}>()

watch(
    () => [open.value] as const,
    ([isOpen]) => {
        if (!isOpen) return
    },
    { immediate: true },
)

function close() {
    open.value = false
}

function getBookingStatus(booking: Transaction) {
    if (
        ['confirmed', 'picked_up'].includes(booking.status) &&
        new Date(booking.return_date) < new Date()
    ) {
        return 'overdue'
    }

    return booking.status
}

const statusClass = (status: string) => {
    const classes: Record<string, string> = {
        pending_payment: 'bg-yellow-500/10 text-yellow-400',
        pending_approval: 'bg-orange-500/10 text-orange-400',
        confirmed: 'bg-blue-500/10 text-blue-400',
        picked_up: 'bg-purple-500/10 text-purple-400',
        returned: 'bg-cyan-500/10 text-cyan-400',
        completed: 'bg-green-500/10 text-green-400',
        rejected: 'bg-red-500/10 text-red-400',
        cancelled: 'bg-red-500/10 text-red-400',
        overdue: 'bg-red-500/10 text-red-400'
    }

    return classes[status] ?? 'bg-[#232323] text-[#c8c8c8]'
}

const refundStatusLabel = (status: string) => ({
    pending_review: 'Pending review',
    processing: 'Processing',
    succeeded: 'Refunded',
    failed: 'Failed',
    rejected: 'Rejected',
}[status] ?? status)

const refundStatusClass = (status: string) => ({
    pending_review: 'bg-amber-500/10 text-amber-400',
    processing: 'bg-blue-500/10 text-blue-400',
    succeeded: 'bg-emerald-500/10 text-emerald-400',
    failed: 'bg-[#C1121F]/10 text-[#E63946]',
    rejected: 'bg-neutral-500/10 text-neutral-400',
}[status] ?? 'bg-white/5 text-neutral-400')

const fmtDateTime = (d: string) =>
    new Date(d).toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
    })

const label = 'mb-1.5 block text-[11px] text-neutral-400'
const section = 'mb-3 text-[11px] font-semibold uppercase tracking-[0.12em] text-[#C1121F]'
const detailCard = 'mb-4 rounded-xl border border-[#292929] bg-[#171717] p-4'
const value = 'text-sm font-medium text-white'
const peso = (n: number | null | undefined) =>
    `₱${(n ?? 0).toLocaleString()}`
</script>
