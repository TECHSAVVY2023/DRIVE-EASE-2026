<template>
    <MobileDrawer
        :menu-open="menuOpen"
        @close-menu="closeMenu"
    />
    
    <Navbar
        :user="user"
        :is-logged-in="isLoggedIn"
        :auth-ready="authReady"
        :menu-open="menuOpen"
        @toggle-menu="toggleMenu"
        @open-sidebar="handleOpenSidebar" 
        @close-sidebar="handleCloseSidebar"
    />

    <Banner 
        subtitle="Transaction Details"
        title="Booking Reference"
        :breadcrumbs="[
            { label: 'Home', to: '/' },
            { label: 'Transaction Details' }
        ]"
    />

    <div class="charcoal-blueprint-surface min-h-screen text-gray-200 p-4 sm:p-6 lg:p-10">

        <div class="mx-auto max-w-6xl grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6 items-start">

            <ClientBookingRefMainDetails :booking="booking"/>

            <ClientBookingRefSideBar 
                :booking="booking"
                :cancelling="cancelling"
                @cancel-booking="handleCancel"
            />

        </div>

    </div>

</template>

<script setup lang="ts">
import type { Transaction } from '~/utils/types/booking';

const { isLoggedIn, authReady } = useAuth()
const { user } = useCurrentUser()
const { $swal } = useNuxtApp()

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

const route = useRoute()

const bookingReference = String(route.params.booking_reference)

const { fetchTransactionDetail, cancelTransaction } = useTransactions()

const booking = ref<Transaction | null>(null)
const cancelling = ref(false)

onMounted(async () => {
    booking.value = await fetchTransactionDetail(bookingReference)
})

const handleCancel = async () => {
    if (!booking.value || cancelling.value) return

    const confirmation = await $swal.fire({
        icon: 'warning',
        title: 'Cancel this booking?',
        text: 'Your reserved dates will be released. This action cannot be undone.',
        input: 'textarea',
        inputLabel: 'Reason for cancellation',
        inputPlaceholder: 'Briefly tell us why you are cancelling...',
        inputAttributes: {
            maxlength: '500',
        },
        inputValidator: value => {
            if (!value?.trim()) return 'Please provide a cancellation reason.'
            return undefined
        },
        showCancelButton: true,
        confirmButtonText: 'Cancel booking',
        cancelButtonText: 'Keep booking',
        confirmButtonColor: '#C1121F',
        cancelButtonColor: '#333333',
        background: '#1a1a1a',
        color: '#ffffff',
        reverseButtons: true,
    })

    if (!confirmation.isConfirmed) return

    cancelling.value = true

    try {
        booking.value = await cancelTransaction(
            bookingReference,
            String(confirmation.value).trim(),
        )

        await $swal.fire({
            icon: 'success',
            title: 'Booking cancelled',
            text: booking.value.refund?.status === 'pending_review'
                ? 'Your dates were released and your full refund is waiting for admin review.'
                : 'Your reserved dates have been released.',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
        })
    } catch (error: unknown) {
        const requestError = error as {
            data?: { message?: string; reason?: string }
        }

        await $swal.fire({
            icon: 'error',
            title: 'Unable to cancel booking',
            text: requestError.data?.message
                ?? requestError.data?.reason
                ?? 'Please try again or contact Drive Ease.',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
        })
    } finally {
        cancelling.value = false
    }
}

</script>
