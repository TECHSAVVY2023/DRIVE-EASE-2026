```vue
<script setup lang="ts">
const search = ref("")
const selectedStatus = ref("")
const selectedPayment = ref("")
const currentPage = ref(1)

const bookings = ref([
    {
        booking_reference: "DE-2026-00124",
        customer: "Juan Dela Cruz",
        email: "juan@email.com",
        car: "Ford Ranger Raptor",
        dates: "Sep 20 - Sep 23, 2026",
        amount: 5400,
        status: "pending_approval",
        payment: "paid",
    },
    {
        booking_reference: "DE-2026-00123",
        customer: "Mark Santos",
        email: "mark@email.com",
        car: "Toyota Fortuner",
        dates: "Sep 19 - Sep 21, 2026",
        amount: 4200,
        status: "confirmed",
        payment: "paid",
    },
    {
        booking_reference: "DE-2026-00122",
        customer: "Alex Garcia",
        email: "alex@email.com",
        car: "Mitsubishi Montero",
        dates: "Sep 18 - Sep 20, 2026",
        amount: 3800,
        status: "picked_up",
        payment: "paid",
    },
    {
        booking_reference: "DE-2026-00121",
        customer: "Kevin Ramos",
        email: "kevin@email.com",
        car: "Toyota Vios",
        dates: "Sep 17 - Sep 18, 2026",
        amount: 1800,
        status: "completed",
        payment: "paid",
    },
    {
        booking_reference: "DE-2026-00120",
        customer: "Michael Tan",
        email: "michael@email.com",
        car: "Honda Civic",
        dates: "Sep 16 - Sep 18, 2026",
        amount: 3200,
        status: "rejected",
        payment: "refunded",
    },
])

const recentActivity = [
    {
        type: "new",
        title: "New booking submitted",
        customer: "Juan Dela Cruz",
        reference: "DE-2026-00124",
        time: "5 min ago",
    },
    {
        type: "confirmed",
        title: "Booking confirmed",
        customer: "Mark Santos",
        reference: "DE-2026-00123",
        time: "18 min ago",
    },
    {
        type: "pickup",
        title: "Vehicle picked up",
        customer: "Alex Garcia",
        reference: "DE-2026-00122",
        time: "42 min ago",
    },
    {
        type: "completed",
        title: "Booking completed",
        customer: "Kevin Ramos",
        reference: "DE-2026-00121",
        time: "1 hr ago",
    },
]

const filteredBookings = computed(() => {
    return bookings.value.filter((booking) => {
        const matchesSearch =
            !search.value ||
            booking.booking_reference
                .toLowerCase()
                .includes(search.value.toLowerCase()) ||
            booking.customer
                .toLowerCase()
                .includes(search.value.toLowerCase()) ||
            booking.car
                .toLowerCase()
                .includes(search.value.toLowerCase())

        const matchesStatus =
            !selectedStatus.value ||
            booking.status === selectedStatus.value

        const matchesPayment =
            !selectedPayment.value ||
            booking.payment === selectedPayment.value

        return matchesSearch && matchesStatus && matchesPayment
    })
})

const stats = computed(() => [
    {
        label: "Total Bookings",
        value: bookings.value.length,
        description: "All booking records",
        icon: "▣",
    },
    {
        label: "Pending Approval",
        value: bookings.value.filter(
            (booking) => booking.status === "pending_approval"
        ).length,
        description: "Require your attention",
        icon: "!",
    },
    {
        label: "Active Rentals",
        value: bookings.value.filter(
            (booking) => booking.status === "picked_up"
        ).length,
        description: "Currently on the road",
        icon: "↗",
    },
    {
        label: "Completed",
        value: bookings.value.filter(
            (booking) => booking.status === "completed"
        ).length,
        description: "Successfully completed",
        icon: "✓",
    },
])

const formatStatus = (status: string) => {
    const labels: Record<string, string> = {
        pending_payment: "Pending Payment",
        pending_approval: "Pending Approval",
        confirmed: "Confirmed",
        rejected: "Rejected",
        picked_up: "Picked Up",
        returned: "Returned",
        completed: "Completed",
        cancelled: "Cancelled",
    }

    return labels[status] ?? status
}

const statusClass = (status: string) => {
    const classes: Record<string, string> = {
        pending_payment: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
        pending_approval: "bg-orange-500/10 text-orange-400 border-orange-500/20",
        confirmed: "bg-blue-500/10 text-blue-400 border-blue-500/20",
        rejected: "bg-red-500/10 text-red-400 border-red-500/20",
        picked_up: "bg-purple-500/10 text-purple-400 border-purple-500/20",
        returned: "bg-cyan-500/10 text-cyan-400 border-cyan-500/20",
        completed: "bg-green-500/10 text-green-400 border-green-500/20",
        cancelled: "bg-gray-500/10 text-gray-400 border-gray-500/20",
    }

    return classes[status] ?? "bg-gray-500/10 text-gray-400 border-gray-500/20"
}

const paymentClass = (payment: string) => {
    if (payment === "paid") return "text-green-400"
    if (payment === "refunded") return "text-blue-400"

    return "text-yellow-400"
}

const activityIconClass = (type: string) => {
    const classes: Record<string, string> = {
        new: "bg-orange-500/10 text-orange-400",
        confirmed: "bg-blue-500/10 text-blue-400",
        pickup: "bg-purple-500/10 text-purple-400",
        completed: "bg-green-500/10 text-green-400",
    }

    return classes[type] ?? "bg-gray-500/10 text-gray-400"
}
</script>

<template>
    <div class="space-y-6">

        <!-- Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
                <h1 class="text-2xl font-bold text-white">
                    Bookings
                </h1>

                <p class="text-sm text-gray-400 mt-1">
                    Manage customer reservations and rental activity.
                </p>
            </div>

            <button
                class="flex items-center justify-center gap-2 bg-[#C1121F] hover:bg-[#a80f1b] transition-colors text-white text-sm font-semibold px-4 py-2.5 rounded-lg"
            >
                <span class="text-lg leading-none">+</span>
                Create Booking
            </button>
        </div>


        <!-- Stats -->
        <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-[18px]">

            <div
                v-for="stat in stats"
                :key="stat.label"
                class="bg-[#161616] border border-[#232323] rounded-xl p-4 sm:p-5"
            >
                <div class="flex items-start justify-between">

                    <div>
                        <p class="text-xs text-gray-400">
                            {{ stat.label }}
                        </p>

                        <p class="text-2xl font-bold text-white mt-2">
                            {{ stat.value }}
                        </p>

                        <p class="text-[11px] text-gray-500 mt-1">
                            {{ stat.description }}
                        </p>
                    </div>

                    <div
                        class="w-9 h-9 rounded-lg bg-[#C1121F]/10 flex items-center justify-center text-[#C1121F] font-bold"
                    >
                        {{ stat.icon }}
                    </div>

                </div>
            </div>

        </div>


        <!-- Needs Attention + Recent Activity -->
        <div class="grid grid-cols-1">


            <!-- Recent Activity -->
            <div class="bg-[#161616] border border-[#232323] rounded-xl p-4 sm:p-5">

                <div class="flex items-start justify-between mb-5">

                    <div>
                        <h3 class="text-base font-bold text-white">
                            Recent Activity
                        </h3>

                        <p class="text-xs text-gray-500 mt-1">
                            Latest booking updates.
                        </p>
                    </div>

                    <button
                        class="text-xs font-semibold text-gray-500 hover:text-white transition-colors"
                    >
                        View all
                    </button>

                </div>


                <div class="space-y-4">

                    <div
                        v-for="activity in recentActivity"
                        :key="activity.reference"
                        class="flex items-start gap-3"
                    >

                        <div
                            class="w-8 h-8 shrink-0 rounded-full flex items-center justify-center text-xs font-bold"
                            :class="activityIconClass(activity.type)"
                        >
                            <span v-if="activity.type === 'new'">+</span>
                            <span v-else-if="activity.type === 'confirmed'">✓</span>
                            <span v-else-if="activity.type === 'pickup'">↗</span>
                            <span v-else>✓</span>
                        </div>

                        <div class="min-w-0 flex-1">

                            <div class="flex items-start justify-between gap-3">

                                <div>
                                    <p class="text-sm text-gray-200">
                                        {{ activity.title }}
                                    </p>

                                    <p class="text-[11px] text-gray-500 mt-1">
                                        {{ activity.customer }}
                                        ·
                                        {{ activity.reference }}
                                    </p>
                                </div>

                                <span
                                    class="text-[10px] text-gray-600 whitespace-nowrap"
                                >
                                    {{ activity.time }}
                                </span>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </div>


        <!-- Bookings Table -->
        <div class="bg-[#161616] border border-[#232323] rounded-xl overflow-hidden">

            <!-- Table Header -->
            <div class="p-4 sm:p-5 border-b border-[#232323]">

                <div class="flex flex-col xl:flex-row xl:items-center xl:justify-between gap-4">

                    <div>
                        <h3 class="text-base font-bold text-white">
                            All Bookings
                        </h3>

                        <p class="text-xs text-gray-500 mt-1">
                            View and manage customer reservations.
                        </p>
                    </div>

                    <div class="flex flex-col sm:flex-row gap-2">

                        <input
                            v-model="search"
                            type="text"
                            placeholder="Search bookings..."
                            class="w-full sm:w-64 bg-[#121212] border border-[#292929] focus:border-[#C1121F] outline-none rounded-lg px-3 py-2.5 text-sm text-white placeholder:text-gray-600"
                        />

                        <select
                            v-model="selectedStatus"
                            class="bg-[#121212] border border-[#292929] outline-none rounded-lg px-3 py-2.5 text-sm text-gray-300 focus:border-[#C1121F]"
                        >
                            <option value="">All Status</option>
                            <option value="pending_payment">
                                Pending Payment
                            </option>
                            <option value="pending_approval">
                                Pending Approval
                            </option>
                            <option value="confirmed">
                                Confirmed
                            </option>
                            <option value="picked_up">
                                Picked Up
                            </option>
                            <option value="returned">
                                Returned
                            </option>
                            <option value="completed">
                                Completed
                            </option>
                            <option value="cancelled">
                                Cancelled
                            </option>
                            <option value="rejected">
                                Rejected
                            </option>
                        </select>

                        <select
                            v-model="selectedPayment"
                            class="bg-[#121212] border border-[#292929] outline-none rounded-lg px-3 py-2.5 text-sm text-gray-300 focus:border-[#C1121F]"
                        >
                            <option value="">Payment</option>
                            <option value="paid">Paid</option>
                            <option value="pending">Pending</option>
                            <option value="refunded">Refunded</option>
                        </select>

                    </div>

                </div>

            </div>


            <!-- Table -->
            <div class="overflow-x-auto">

                <table class="w-full min-w-[1050px]">

                    <thead>
                        <tr class="border-b border-[#232323] text-left">

                            <th class="px-5 py-3 text-[11px] uppercase tracking-wide text-gray-500 font-semibold">
                                Booking
                            </th>

                            <th class="px-5 py-3 text-[11px] uppercase tracking-wide text-gray-500 font-semibold">
                                Customer
                            </th>

                            <th class="px-5 py-3 text-[11px] uppercase tracking-wide text-gray-500 font-semibold">
                                Vehicle
                            </th>

                            <th class="px-5 py-3 text-[11px] uppercase tracking-wide text-gray-500 font-semibold">
                                Rental Period
                            </th>

                            <th class="px-5 py-3 text-[11px] uppercase tracking-wide text-gray-500 font-semibold">
                                Amount
                            </th>

                            <th class="px-5 py-3 text-[11px] uppercase tracking-wide text-gray-500 font-semibold">
                                Payment
                            </th>

                            <th class="px-5 py-3 text-[11px] uppercase tracking-wide text-gray-500 font-semibold">
                                Status
                            </th>

                            <th class="px-5 py-3 text-[11px] uppercase tracking-wide text-gray-500 font-semibold text-right">
                                Action
                            </th>

                        </tr>
                    </thead>


                    <tbody>

                        <tr
                            v-for="booking in filteredBookings"
                            :key="booking.booking_reference"
                            class="border-b border-[#202020] hover:bg-[#1a1a1a] transition-colors"
                        >

                            <!-- Booking -->
                            <td class="px-5 py-4">
                                <p class="text-sm font-semibold text-white">
                                    {{ booking.booking_reference }}
                                </p>

                                <p class="text-[11px] text-gray-500 mt-1">
                                    Reservation
                                </p>
                            </td>


                            <!-- Customer -->
                            <td class="px-5 py-4">
                                <p class="text-sm font-medium text-white">
                                    {{ booking.customer }}
                                </p>

                                <p class="text-[11px] text-gray-500 mt-1">
                                    {{ booking.email }}
                                </p>
                            </td>


                            <!-- Vehicle -->
                            <td class="px-5 py-4">
                                <p class="text-sm text-gray-200">
                                    {{ booking.car }}
                                </p>
                            </td>


                            <!-- Rental Period -->
                            <td class="px-5 py-4">
                                <p class="text-sm text-gray-300">
                                    {{ booking.dates }}
                                </p>
                            </td>


                            <!-- Amount -->
                            <td class="px-5 py-4">
                                <p class="text-sm font-semibold text-white">
                                    ₱{{ booking.amount.toLocaleString() }}
                                </p>
                            </td>


                            <!-- Payment -->
                            <td class="px-5 py-4">
                                <span
                                    class="text-xs font-medium capitalize"
                                    :class="paymentClass(booking.payment)"
                                >
                                    {{ booking.payment }}
                                </span>
                            </td>


                            <!-- Status -->
                            <td class="px-5 py-4">
                                <span
                                    class="inline-flex items-center px-2.5 py-1 rounded-full border text-[11px] font-medium whitespace-nowrap"
                                    :class="statusClass(booking.status)"
                                >
                                    {{ formatStatus(booking.status) }}
                                </span>
                            </td>


                            <!-- Action -->
                            <td class="px-5 py-4 text-right">
                                <button
                                    class="text-xs font-semibold text-gray-400 hover:text-white transition-colors"
                                >
                                    View
                                </button>
                            </td>

                        </tr>


                        <!-- Empty State -->
                        <tr v-if="filteredBookings.length === 0">

                            <td
                                colspan="8"
                                class="px-5 py-12 text-center"
                            >
                                <p class="text-sm text-gray-400">
                                    No bookings found.
                                </p>

                                <p class="text-xs text-gray-600 mt-1">
                                    Try changing your search or filters.
                                </p>
                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>


            <!-- Pagination -->
            <div
                class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 px-5 py-4"
            >

                <p class="text-xs text-gray-500">
                    Showing {{ filteredBookings.length }} bookings
                </p>

                <div class="flex items-center gap-2">

                    <button
                        class="px-3 py-1.5 text-xs rounded-lg border border-[#292929] text-gray-500 hover:text-white hover:bg-[#202020] transition-colors"
                    >
                        Previous
                    </button>

                    <button
                        class="px-3 py-1.5 text-xs rounded-lg bg-[#C1121F] text-white"
                    >
                        1
                    </button>

                    <button
                        class="px-3 py-1.5 text-xs rounded-lg border border-[#292929] text-gray-400 hover:text-white hover:bg-[#202020] transition-colors"
                    >
                        Next
                    </button>

                </div>

            </div>

        </div>

    </div>
</template>
```
