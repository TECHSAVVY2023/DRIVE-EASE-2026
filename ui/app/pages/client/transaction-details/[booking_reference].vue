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
                @download-receipt="handleDownloadReceipt"
                @cancel="handleCancel"
            />

        </div>

    </div>

</template>

<script setup lang="ts">
import type { Transaction } from '~/utils/types/booking';

const { isLoggedIn, authReady } = useAuth()
const { user } = useCurrentUser()

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

const route = useRoute()

const bookingReference = String(route.params.booking_reference)

console.log('booking reference:', bookingReference)

const { fetchTransactionDetail } = useTransactions()

const booking = ref<Transaction | null>(null)

onMounted(async () => {
    booking.value = await fetchTransactionDetail(bookingReference)
})

const handleDownloadReceipt = () => {
    console.log('Download receipt')
}

const handleCancel = () => {
    console.log('Cancel booking')
}

</script>
