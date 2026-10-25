<template>
    <div class="bg-[#161616] border border-[#232323] rounded-xl overflow-hidden">

        <!-- Header / Filters -->
        <div
            class="
                flex justify-between items-center
                px-4 sm:px-5
                py-4 sm:py-[18px]
                border-b border-[#232323]
                gap-3 sm:gap-4
                flex-wrap
            "
        >
            <h3 class="text-base font-bold text-white">
                All bookings
            </h3>

            <div class="flex flex-wrap sm:flex-nowrap md:justify-evenly gap-2 w-full max-w-[600px] sm:w-full">

                <!-- Search -->
                <input
                    :value="props.search"
                    @input="handleSearch"
                    placeholder="Search bookings..."
                    class="
                        bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg px-3.5 py-[9px] text-[13px] 
                        text-[#e4e4e4] placeholder-[#8a8a8a] w-full outline-none
                        focus:border-[#C1121F] transition-colors
                    "
                />

                <!-- Status filter -->
                <div class="relative flex-1 sm:flex-none">
                    <select
                        :value="props.selectedStatus"
                        @change="handleStatusChange"
                        class="
                            appearance-none w-full sm:w-auto
                            bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg
                            pl-3.5 pr-9 py-2 text-[13px]
                            text-[#c8c8c8] cursor-pointer outline-none
                            hover:border-[#C1121F] focus:border-[#C1121F]
                            transition-colors
                        "
                    >
                        <option value="">Status</option>
                        <option value="pending_payment">Pending payment</option>
                        <option value="pending_approval">Pending approval</option>
                        <option value="confirmed">Confirmed</option>
                        <option value="picked_up">Picked up</option>
                        <option value="returned">Returned</option>
                        <option value="overdue">Overdue</option>
                        <option value="completed">Completed</option>
                        <option value="rejected">Rejected</option>
                        <option value="cancelled">Cancelled</option>
                    </select>

                    <svg
                        class="absolute right-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#8a8a8a] pointer-events-none"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <path d="m6 9 6 6 6-6" />
                    </svg>
                </div>

                <!-- Payment filter -->
                <div class="relative flex-1 sm:flex-none">
                    <select
                        :value="props.selectedPayment"
                        @change="handlePaymentChange"
                        class="
                            appearance-none w-full sm:w-auto
                            bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg
                            pl-3.5 pr-9 py-2 text-[13px]
                            text-[#c8c8c8] cursor-pointer outline-none
                            hover:border-[#C1121F] focus:border-[#C1121F]
                            transition-colors
                        "
                    >
                        <option value="">Payment</option>
                        <option value="paid">Paid</option>
                        <option value="pending">Pending</option>
                        <option value="failed">Failed</option>
                        <option value="refunded">Refunded</option>
                    </select>

                    <svg
                        class="absolute right-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#8a8a8a] pointer-events-none"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <path d="m6 9 6 6 6-6" />
                    </svg>
                </div>

            </div>
        </div>

        <!-- Table scroll container -->
        <div class="table-scroll w-full overflow-x-auto">
            <table class="w-full min-w-[1100px] border-collapse">

                <thead class="bg-[#0f0f0f]">
                    <tr
                        class="
                            text-left text-[12px]
                            text-[#8a8a8a]
                            uppercase tracking-wide
                            font-semibold
                            border-b border-[#232323]
                        "
                    >
                        <th class="px-5 py-3">Booking</th>
                        <th class="px-5 py-3">Customer</th>
                        <th class="px-5 py-3">Vehicle</th>
                        <th class="px-5 py-3">Rental Period</th>
                        <th class="px-5 py-3">Amount</th>
                        <th class="px-5 py-3">Status</th>
                        <th class="px-5 py-3">Actions</th>
                    </tr>
                </thead>

                <tbody>
                    <tr
                        v-for="(booking, i) in props.bookings"
                        :key="booking.booking_reference"
                        :class="
                            i !== props.bookings.length - 1
                                ? 'border-b border-[#1c1c1c]'
                                : ''
                        "
                    >

                        <!-- Booking -->
                        <td class="px-5 py-3.5 text-sm">
                            <div>
                                <div class="font-semibold text-white">
                                    {{ booking.booking_reference }}
                                </div>

                                <div class="text-[#8a8a8a] text-[12.5px]">
                                    {{ formatDateTime(booking.created_at) }}
                                </div>
                            </div>
                        </td>

                        <!-- Customer -->
                        <td class="px-5 py-3.5 text-sm">
                            <div class="min-w-0">
                                <div class="font-semibold text-[#e4e4e4] truncate">
                                    {{ booking.user.first_name }} {{booking.user.last_name}}
                                </div>

                                <div class="text-[#8a8a8a] text-[12.5px] truncate">
                                    {{ booking.user.email }}
                                </div>
                            </div>
                        </td>

                        <!-- Vehicle -->
                        <td class="px-5 py-3.5 text-sm">
                            <div class="flex items-center gap-2.5">

                                <div
                                    v-if="booking.car.image"
                                    class="
                                        w-10 h-8 rounded-md bg-[#2a2a2a]
                                        flex items-center justify-center
                                        flex-shrink-0 overflow-hidden
                                    "
                                >
                                    <img
                                        :src="booking.car.image"
                                        :alt="`${booking.car.brand} ${booking.car.model}`"
                                        class="w-full h-full object-cover"
                                    />
                                </div>

                                <div
                                    v-else
                                    class="
                                        w-10 h-8 rounded-md bg-[#2a2a2a]
                                        flex items-center justify-center
                                        flex-shrink-0
                                    "
                                >
                                    <svg
                                        class="w-5 h-5 text-[#8a8a8a]"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        stroke-width="1.8"
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                    >
                                        <path d="M5 17h14" />
                                        <path d="M6 17l1.5-6h9L18 17" />
                                        <circle cx="8" cy="17" r="1.5" />
                                        <circle cx="16" cy="17" r="1.5" />
                                    </svg>
                                </div>

                                <div class="min-w-0">
                                    <div class="font-semibold text-[#e4e4e4] truncate">
                                        {{ booking.car?.brand }}
                                        {{ booking.car?.model }}
                                    </div>

                                    <div class="text-[#8a8a8a] text-[12.5px] truncate">
                                        {{ booking.car?.year }}
                                    </div>
                                </div>

                            </div>
                        </td>

                        <!-- Rental Period -->
                        <td class="px-5 py-3.5 text-sm whitespace-nowrap">
                            <div class="text-[#e4e4e4]">
                                {{ formatDate(booking.pickup_date) }}
                            </div>

                            <div class="text-[#8a8a8a] text-[12.5px]">
                                to {{ formatDate(booking.return_date) }}
                            </div>
                        </td>

                        <!-- Amount -->
                        <td
                            class="
                                px-5 py-3.5 text-sm
                                text-[#e4e4e4]
                                whitespace-nowrap
                            "
                        >
                            ₱{{ formatPrice(Number(booking.total_price)) }}
                        </td>

                        <!-- Status -->
                        <td class="px-5 py-3.5 text-sm">
                            <span
                                class="
                                    text-xs px-2.5 py-1 rounded-md
                                    inline-block whitespace-nowrap
                                "
                                :class="statusClass(getBookingStatus(booking))"
                            >
                                {{ formatStatus(getBookingStatus(booking)) }}
                            </span>
                        </td>

                        <!-- Actions -->
                        <td class="px-5 py-3.5 text-sm">
                            <div class="flex items-center gap-1 text-[#8a8a8a]">

                            <button
                                type="button"
                                class="
                                    hover:border-[#c1121f] cursor-pointer
                                    hover:text-[#c1121f] inline-flex h-8 items-center 
                                    gap-1.5 rounded-lg border border-[#292929] 
                                    bg-[#151515] px-2.5 text-[11px] font-semibold 
                                    text-[#9b9b9b] transition-all
                                "
                                @click="$emit('edit', booking)"
                            >
                                <svg
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    class="h-3.5 w-3.5"
                                    stroke="currentColor"
                                    stroke-width="2"
                                >
                                    <path d="M12 20h9" />
                                    <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" />
                                </svg>
                                Edit
                            </button>

                            <button
                                type="button"
                                class="
                                    hover:border-[#c1121f] cursor-pointer
                                    hover:text-[#c1121f] inline-flex h-8 items-center 
                                    gap-1.5 rounded-lg border border-[#292929] 
                                    bg-[#151515] px-2.5 text-[11px] font-semibold 
                                    text-[#9b9b9b] transition-all
                                "
                                @click="$emit('view', booking)"
                            >
                                <svg
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    class="h-3.5 w-3.5"
                                    stroke="currentColor"
                                    stroke-width="2"
                                >
                                    <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z" />
                                    <circle cx="12" cy="12" r="3" />
                                </svg>
                                View
                            </button>

                            <button
                                type="button"
                                class="
                                    hover:border-[#c1121f] cursor-pointer
                                    hover:text-[#c1121f] inline-flex h-8 items-center 
                                    gap-1.5 rounded-lg border border-[#292929] 
                                    bg-[#151515] px-2.5 text-[11px] font-semibold 
                                    text-[#9b9b9b] transition-all
                                "
                                @click="$emit('delete', booking)"
                            >
                                <svg
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    class="h-3.5 w-3.5"
                                    stroke="currentColor"
                                    stroke-width="2"
                                >
                                    <path d="M3 6h18" />
                                    <path d="M8 6V4h8v2" />
                                    <path d="M19 6l-1 14H6L5 6" />
                                    <path d="M10 11v5M14 11v5" />
                                </svg>
                                Delete
                            </button>

                            </div>
                        </td>

                    </tr>

                    <!-- Empty state -->
                    <tr v-if="props.bookings.length === 0">
                        <td
                            colspan="8"
                            class="
                                px-5 py-10 text-center
                                text-sm text-[#8a8a8a]
                            "
                        >
                            No bookings found.
                        </td>
                    </tr>

                </tbody>

            </table>
        </div>

        <!-- Pagination -->
        <div
            class="
                flex justify-between items-center
                px-5 py-4
                text-[#8a8a8a] text-[13px]
            "
        >
            <span>
                Showing
                {{
                    props.bookings.length
                        ? (props.currentPage - 1) * props.pageSize + 1
                        : 0
                }}
                –
                {{
                    Math.min(
                        props.currentPage * props.pageSize,
                        props.count
                    )
                }}
                of {{ props.count }} bookings
            </span>

            <div class="flex gap-1.5">

                <!-- Previous -->
                <button
                    type="button"
                    :disabled="!props.previousPage"
                    @click="
                        emit(
                            'update:page',
                            props.currentPage - 1
                        )
                    "
                    class="
                        w-7 h-7 flex items-center justify-center
                        rounded-md border border-[#2a2a2a]
                    "
                    :class="
                        props.previousPage
                            ? 'cursor-pointer hover:bg-[#222]'
                            : 'opacity-40 cursor-not-allowed'
                    "
                >
                    ‹
                </button>

                <!-- Pages -->
                <button
                    v-for="p in props.totalPages"
                    :key="p"
                    type="button"
                    @click="emit('update:page', p)"
                    class="
                        w-7 h-7 flex items-center justify-center
                        rounded-md border
                    "
                    :class="
                        p === props.currentPage
                            ? 'bg-[#c81e2c] border-[#c81e2c] text-white'
                            : 'border-[#2a2a2a] hover:bg-[#222]'
                    "
                >
                    {{ p }}
                </button>

                <!-- Next -->
                <button
                    type="button"
                    :disabled="!props.nextPage"
                    @click="
                        emit(
                            'update:page',
                            props.currentPage + 1
                        )
                    "
                    class="
                        w-7 h-7 flex items-center justify-center
                        rounded-md border border-[#2a2a2a]
                    "
                    :class="
                        props.nextPage
                            ? 'cursor-pointer hover:bg-[#222]'
                            : 'opacity-40 cursor-not-allowed'
                    "
                >
                    ›
                </button>

            </div>
        </div>

    </div>
</template>

<script setup lang="ts">
import type { Transaction } from '~/utils/types/booking'

const props = defineProps<{
    bookings: any[]
    search: string
    currentPage: number
    count: number
    pageSize: number
    totalPages: number
    nextPage: string | null
    previousPage: string | null
    selectedStatus: string
    selectedPayment: string
}>()

const emit = defineEmits<{
    'update:search': [value: string]
    'update:page': [value: number]
    'update:selectedStatus': [value: string]
    'update:selectedPayment': [value: string]
    edit: [booking: Transaction]
    view: [booking: Transaction]
    delete: [booking: Transaction]
}>()

const handleSearch = (event: Event) => {
    const target = event.target as HTMLInputElement
    emit('update:search', target.value)
}

const handleStatusChange = (event: Event) => {
    const target = event.target as HTMLSelectElement
    emit('update:selectedStatus', target.value)
}

const handlePaymentChange = (event: Event) => {
    const target = event.target as HTMLSelectElement
    emit('update:selectedPayment', target.value)
}

const formatPrice = (price: number) => {
    return price.toLocaleString('en-PH')
}

const formatDate = (date: string) => {
    if (!date) return '-'

    return new Date(date).toLocaleDateString('en-PH', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    })
}

const formatDateTime = (date: string | Date) => {
    return new Date(date).toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    })
}

const formatStatus = (status: string) => {
    const labels: Record<string, string> = {
        pending_payment: 'Pending payment',
        pending_approval: 'Pending approval',
        confirmed: 'Confirmed',
        rejected: 'Rejected',
        picked_up: 'Picked up',
        returned: 'Returned',
        completed: 'Completed',
        cancelled: 'Cancelled',
        overdue: 'Overdue'
    }

    return labels[status] ?? status
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

</script>