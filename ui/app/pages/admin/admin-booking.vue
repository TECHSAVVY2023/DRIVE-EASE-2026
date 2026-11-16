<template>

    <AdminBookingEditBookingModal
        v-model="showBookingModal1"
        :booking="selectedBooking"
        :isEditing="isEditing"
        :users="users"
        :cars="fleet"
        @save="handleSaveBooking"
        @close="isEditing = false"
    />

    <AdminBookingAddBookingModal
        v-model="showBookingModal2"
        :users="users"
        :cars="fleet"
        @save="handleSaveBooking"
    />

    <AdminBookingViewBookingModal
        v-model="showBookingDetails"
        :booking="selectedBooking"
        :refunding="refunding"
        @edit="handleViewEditBooking"
        @refund="handleRefund"
    />

    <div class="flex h-screen bg-[#0D0D0D] font-[poppins] overflow-hidden text-white">

        <!-- Sidebar -->
        <AdminCommonSidebarNav
            :sidebarOpen="sidebarOpen"
            @close-sidebar="sidebarOpen = false"
        />

        <!-- Main -->
        <div class="flex-1 flex flex-col overflow-hidden">

            <!-- Topbar -->
            <AdminCommonTopbarNav
                :user="user"
                @open-sidebar="handleOpenSidebar"
                @close-sidebar="handleCloseSidebar"
                title="Bookings"
                :isLoggedIn="isLoggedIn"
                :subtitle="currentDate"
            />

            <main class="flex-1 overflow-y-auto px-8 py-8">

                <!-- Page heading -->
                <div class="flex justify-between items-end mb-[22px]">
                    <div>
                        <h2 class="text-[22px] font-extrabold">
                            Bookings
                        </h2>

                        <div class="text-[#8a8a8a] text-[13px] mt-1">
                            Manage customer reservations and rental activity
                        </div>
                    </div>

                    <button
                        class="
                            bg-[#c81e2c] hover:bg-[#b31a27] transition text-white 
                            font-bold text-sm px-5 py-[11px] rounded-lg"
                        @click="showBookingModal2 = true"
                    >
                        + Add Booking
                    </button>
                </div>

                <!-- Stats -->
                <AdminCommonStatsCards :cards="statCards"/>

                <AdminBookingTable
                    :bookings="bookings"
                    :search="search"
                    :current-page="currentPage"
                    :count="count"
                    :page-size="pageSize"
                    :total-pages="totalPages"
                    :next-page="nextPage"
                    :previous-page="previousPage"
                    :selected-status="selectedStatus"
                    :selected-rental-period="selectedRentalPeriod"

                    @update:search="search = $event"
                    @update:page="currentPage = $event"
                    @update:selected-status="selectedStatus = $event"
                    @update:selected-rental-period="selectedRentalPeriod = $event"

                    @view="handleView"
                    @edit="handleEdit"
                    @delete="handleDelete"
                />

            </main>

        </div>

    </div>
</template>


<script setup lang="ts">
import { ref, computed } from 'vue'
import type { BookingForm, Transaction } from '~/utils/types/booking'

const { isLoggedIn } = useAuth()
const { $swal } = useNuxtApp()
const { apiFetch } = useApiFetch()
const { user } = useCurrentUser()

const { loading, bookings, count, nextPage, previousPage, currentPage,
        pageSize, totalPages, search, selectedStatus, selectedRentalPeriod, fetchStats,
        total_booking, pending_approval, active_rentals, completed, cancelled,  
    } = useAdminTransactionsList()

const { users, fetchUsers } = useUsersList()

const { fleet, fetchCars } = useFleetList()

const sidebarOpen = ref<boolean>(false)

const handleCloseSidebar = (): void => {
    sidebarOpen.value = false
}

const handleOpenSidebar = (): void => {
    sidebarOpen.value = true
}

const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
})

const statCards = computed(() => [
    {
        label: 'Total bookings',
        value: total_booking.value,
        icon: `<svg viewBox="0 0 24 24" fill="none">
            <rect x="4" y="5" width="16" height="15" rx="2"/>
            <path d="M8 3v4M16 3v4M4 9h16"/>
            <path d="M8 13h2M14 13h2M8 16h2M14 16h2"/>
        </svg>`
    },
    {
        label: 'Pending approval',
        value: pending_approval.value,
        icon: `<svg viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="9"/>
            <path d="M12 7v5l3 2"/>
        </svg>`
    },
    {
        label: 'Active rentals',
        value: active_rentals.value,
        icon: `<svg viewBox="0 0 24 24" fill="none">
            <path d="M5 16l1.5-6h11L19 16"/>
            <path d="M4 16h16v3H4z"/>
            <circle cx="7.5" cy="19" r="1.5"/>
            <circle cx="16.5" cy="19" r="1.5"/>
            <path d="M8 10l1.5-3h5L16 10"/>
        </svg>`
    },
    {
        label: 'Completed',
        value: completed.value,
        icon: `<svg viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="9"/>
            <path d="M7.5 12l3 3 6-6"/>
        </svg>`
    },
    {
        label: 'Cancelled',
        value: cancelled.value,
        icon: `<svg viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="9"/>
            <path d="M8.5 8.5l7 7M15.5 8.5l-7 7"/>
        </svg>`
    },
])

const showBookingModal1 = ref(false)
const showBookingModal2 = ref(false)

const isEditing = ref(false)

const selectedBooking = ref<Transaction | null>(null)
const refunding = ref(false)

const handleEdit = (booking: Transaction) => {
    isEditing.value = true
    selectedBooking.value = {
        ...booking,
    }
    showBookingModal1.value = true
}

const { handleCreateBooking: createBooking } = useAdminTransactionAdd()

async function handleCreateBooking(form: BookingForm) {
    const result = await createBooking(form)

    if (!result.success) return

    showBookingModal2.value = false
    window.location.reload()
}

const { handleUpdateBooking: updateBooking, handleDeleteBooking: deleteBooking } = useAdminTransactionEdit()

async function handleUpdateBooking(form: BookingForm) {
    const result = await updateBooking(form)

    if (!result.success) return

    showBookingModal1.value = false
    window.location.reload()
}

async function handleDelete(booking: Transaction) {
    const result = await $swal.fire({
        title: 'Delete booking?',
        text: `Are you sure you want to delete booking ${booking.booking_reference}?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        background: '#1a1a1a',
        confirmButtonColor: '#C1121F',
        color: '#ffffff',
    })

    if (!result.isConfirmed) return

    const response = await deleteBooking(booking.booking_reference)

    if (!response.success) return

    window.location.reload()
}

async function handleSaveBooking(form: BookingForm) {
    if (form.booking_reference) {
        await handleUpdateBooking(form)
        isEditing.value = false
    } else {
        await handleCreateBooking(form)
    }
}
const showBookingDetails = ref(false)
const showBookingDetails1 = ref(false)

const handleView = (booking: Transaction) => {
    selectedBooking.value = { ...booking }
    showBookingDetails.value = true
    console.log('selectedBooking:', selectedBooking.value)
}

const handleViewEditBooking = (booking: Transaction) => {
    selectedBooking.value = { ...booking }
    showBookingDetails.value = false
    isEditing.value = true
    showBookingModal1.value = true
}

const { issueRefund } = useAdminTransactions()

const handleRefund = async (booking: Transaction) => {
    if (refunding.value || !booking.can_refund) return

    const confirmation = await $swal.fire({
        icon: 'warning',
        title: 'Issue full refund?',
        text: `PayMongo will refund the full amount for ${booking.booking_reference}.`,
        input: 'textarea',
        inputLabel: 'Admin note (optional)',
        inputPlaceholder: 'Reason or internal note for this refund...',
        inputAttributes: { maxlength: '255' },
        showCancelButton: true,
        confirmButtonText: 'Issue refund',
        cancelButtonText: 'Not yet',
        confirmButtonColor: '#C1121F',
        cancelButtonColor: '#333333',
        background: '#1a1a1a',
        color: '#ffffff',
        reverseButtons: true,
    })

    if (!confirmation.isConfirmed) return

    refunding.value = true
    try {
        selectedBooking.value = await issueRefund(
            booking.booking_reference,
            String(confirmation.value ?? '').trim(),
        )

        const refundStatus = selectedBooking.value.refund?.status
        await $swal.fire({
            icon: refundStatus === 'failed' ? 'error' : 'success',
            title: refundStatus === 'succeeded' ? 'Refund submitted' : 'Refund processing',
            text: refundStatus === 'succeeded'
                ? 'PayMongo accepted the full refund.'
                : 'The refund was sent to PayMongo and is awaiting confirmation.',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
        })
    } catch (error: unknown) {
        const requestError = error as { data?: { message?: string } }
        await $swal.fire({
            icon: 'error',
            title: 'Refund unsuccessful',
            text: requestError.data?.message ?? 'The refund could not be processed.',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
        })
    } finally {
        refunding.value = false
    }
}

onMounted(async () => {
    await Promise.all([
        fetchUsers(),
        fetchStats(),
        fetchCars(),
    ])
})

watch(
    [showBookingDetails, showBookingModal1],
    ([detailsOpen, editOpen]) => {
        if (!detailsOpen && !editOpen) {
            selectedBooking.value = null
            isEditing.value = false
        }
    }
)

onMounted(() => {
    document.documentElement.classList.add('admin-page')
})

onBeforeUnmount(() => {
    document.documentElement.classList.remove('admin-page')
})

</script>
