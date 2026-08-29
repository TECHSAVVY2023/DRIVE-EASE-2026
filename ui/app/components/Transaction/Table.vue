<template>
    <!-- Table -->
    <div class="overflow-x-auto">
        <table class="w-full text-sm">
            <thead>
                <tr class="border-b border-[#222]">
                    <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">
                        Vehicle
                    </th>

                    <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">
                        Transaction
                    </th>

                    <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">
                        Amount
                    </th>

                    <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">
                        Method
                    </th>

                    <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">
                        Status
                    </th>
                </tr>
            </thead>

            <tbody>
                <!-- Empty -->
                <tr v-if="transactions.length === 0">
                    <td
                        colspan="5"
                        class="text-center text-gray-500 text-sm py-12"
                    >
                        No transactions found.
                    </td>
                </tr>

                <!-- Transactions -->
                <tr
                    v-for="transaction in transactions"
                    :key="transaction.booking_reference"
                    @click="emit('select', transaction)"
                    class="border-b border-[#1f1f1f] hover:bg-[#222] transition-colors duration-150 cursor-pointer"
                >
                    <!-- Vehicle -->
                    <td class="px-5 py-4">
                        <div class="flex items-center gap-3">
                            <div
                                class="w-10 h-8 bg-[#111] rounded-lg overflow-hidden flex-shrink-0"
                            >
                                <img
                                    v-if="transaction.car?.image"
                                    :src="transaction.car.image"
                                    :alt="`${transaction.car.brand} ${transaction.car.model}`"
                                    class="w-full h-full object-cover"
                                    @error="handleImageError"
                                />
                            </div>

                            <span
                                class="text-white text-xs font-medium whitespace-nowrap"
                            >
                                {{ transaction.car?.brand }}
                                {{ transaction.car?.model }}
                            </span>
                        </div>
                    </td>

                    <!-- Transaction -->
                    <td class="px-5 py-4">
                        <p class="text-gray-400 text-xs">
                            {{ formatDate(transaction.created_at) }}
                        </p>

                        <p class="text-gray-500 text-[10px] font-mono mt-0.5">
                            {{ transaction.booking_reference }}
                        </p>
                    </td>

                    <!-- Amount -->
                    <td class="px-5 py-4 text-white text-xs font-semibold">
                        {{ formatAmount(transaction.total_price) }}
                    </td>

                    <!-- Method -->
                    <td class="px-5 py-4 text-gray-300 text-xs">
                        {{ transaction.payment_method ?? '—' }}
                    </td>

                    <!-- Status -->
                    <td class="px-5 py-4">
                        <div
                            class="text-xs font-semibold px-2.5 py-1 rounded-full"
                            :class="statusClass(transaction.status)"
                        >
                            {{ formatStatus(transaction.status) }}
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- Pagination -->
    <div class="flex items-center justify-center gap-2 px-5 pb-5 pt-4">
        <button
            @click="emit('previous')"
            :disabled="currentPage === 1"
            class="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs border border-[#2a2a2a] text-gray-400 hover:border-white hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors duration-200"
        >
            <svg
                class="w-3 h-3"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 19l-7-7 7-7"
                />
            </svg>

            Previous
        </button>

        <template v-for="page in totalPages" :key="page">
            <button
                @click="emit('update:currentPage', page)"
                class="w-8 h-8 rounded-lg text-xs font-semibold transition-colors duration-200"
                :class="
                    currentPage === page
                        ? 'bg-[#C1121F] text-white'
                        : 'border border-[#2a2a2a] text-gray-400 hover:border-white hover:text-white'
                "
            >
                {{ page }}
            </button>
        </template>

        <button
            @click="emit('next')"
            :disabled="currentPage === totalPages"
            class="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs border border-[#2a2a2a] text-gray-400 hover:border-white hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors duration-200"
        >
            Next

            <svg
                class="w-3 h-3"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 5l7 7-7 7"
                />
            </svg>
        </button>
    </div>
</template>

<script setup lang="ts">
import type { Transaction } from '~/utils/api/api'

const props = defineProps<{
    transactions: Transaction[]
    currentPage: number
    totalPages: number
}>()

const emit = defineEmits<{
    (e: 'update:currentPage', value: number): void
    (e: 'previous'): void
    (e: 'next'): void
    (e: 'select', transaction: Transaction): void
}>()

const formatAmount = (amount: string | number | null | undefined) => {
    if (amount === null || amount === undefined) {
        return '—'
    }

    return new Intl.NumberFormat('en-PH', {
        style: 'currency',
        currency: 'PHP',
    }).format(Number(amount))
}

const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
    })
}

const formatStatus = (status: string) => {
    const statusMap: Record<string, string> = {
        pending_payment: 'Pending',
        payment_failed: 'Payment Failed',
        pending_approval: 'Pending',
        confirmed: 'Confirmed',
        rejected: 'Rejected',
        picked_up: 'Picked Up',
        returned: 'Returned',
        completed: 'Completed',
        cancelled: 'Cancelled',
    }

    return statusMap[status] ?? status
}

const statusClass = (status: string) => {
    const statusMap: Record<string, string> = {
        pending_payment: 'bg-yellow-500/10 text-yellow-400',
        payment_failed: 'bg-red-500/10 text-red-400',
        pending_approval: 'bg-yellow-500/10 text-yellow-400',
        confirmed: 'bg-green-500/10 text-green-400',
        rejected: 'bg-red-500/10 text-red-400',
        picked_up: 'bg-blue-500/10 text-blue-400',
        returned: 'bg-blue-500/10 text-blue-400',
        completed: 'bg-green-500/10 text-green-400',
        cancelled: 'bg-gray-500/10 text-gray-400',
    }

    return statusMap[status] ?? 'bg-gray-500/10 text-gray-400'
}

const handleImageError = (event: Event) => {
    const image = event.target as HTMLImageElement
    image.style.display = 'none'
}
</script>