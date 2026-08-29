<template>
    <MobileDrawer
        :menu-open="menuOpen"
        @close-menu="closeMenu"
    />
    
    <Navbar
        :user="user"
        :isLoggedIn="isLoggedIn"
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

    <div class="min-h-screen bg-[#0b0b0d] text-gray-200 p-4 sm:p-6 lg:p-10">

        <ClientBookingDetails 
            :booking="booking"
            @view-id="handleViewId"
            @download-receipt="handleDownloadReceipt"
            @cancel="handleCancel"
        />

    </div>

</template>

<script setup lang="ts">
import type { Transaction } from '~/utils/api/api';

const { isLoggedIn } = useAuth()
const { apiFetch } = useApiFetch()

const user = ref<any>(null)

watch(isLoggedIn, async (val) => {
    if (val) {
        user.value = await apiFetch('/auth/me/')
    } else {
        user.value = null
    }
}, { immediate: true })

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

const handleViewId = (id: any) => {
  console.log('View ID:', id)
}

const handleDownloadReceipt = () => {
  console.log('Download receipt')
}

const handleCancel = () => {
  console.log('Cancel booking')
}

</script>