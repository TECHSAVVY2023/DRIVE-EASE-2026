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

    <div class="charcoal-blueprint-surface min-h-screen font-[poppins]">

        <Banner 
            subtitle="Stay updated"
            title="Notifications"
            :breadcrumbs="[
                { label: 'Home', to: '/' },
                { label: 'Notifications' }
            ]"
        />

        <div class="max-w-2xl mx-auto px-4 py-8">
            <div class="smoked-charcoal-panel rounded-xl overflow-hidden flex flex-col">

                <!-- Header -->
                <ClientNotificationsHeader
                    :notifications="notifications"
                    :total="count"
                    :unread-count="unreadCount"
                    :marking-all="markingAll"
                    :deleting-all="deletingAll"
                    @mark-all-read="handleMarkAllAsRead"
                    @delete-all="handleDeleteAll"
                />

                <ClientNotificationsList
                    :notifications="notifications"
                />

            </div>
        </div>

    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

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

const {
    loading,
    notifications,
    count,
    unreadCount,
    nextPage,
    previousPage,
    currentPage,
    totalPages,
    fetchNotificationList,
    markAllAsRead,
    deleteAll,
} = useNotificationList()

const markingAll = ref(false)
const deletingAll = ref(false)

const handleMarkAllAsRead = async () => {
    if (unreadCount.value === 0 || markingAll.value) return

    markingAll.value = true
    try {
        await markAllAsRead()
    } catch (error) {
        console.error('Failed to mark all notifications as read:', error)
        await $swal.fire({
            icon: 'error',
            title: 'Unable to update notifications',
            text: 'Please try again.',
            background: '#1a1a1a',
            color: '#ffffff',
            confirmButtonColor: '#C1121F',
        })
    } finally {
        markingAll.value = false
    }
}

const handleDeleteAll = async () => {
    if (count.value === 0 || deletingAll.value) return

    const confirmation = await $swal.fire({
        icon: 'warning',
        title: 'Delete all notifications?',
        text: 'This action cannot be undone.',
        showCancelButton: true,
        confirmButtonText: 'Delete all',
        confirmButtonColor: '#C1121F',
        cancelButtonColor: '#333333',
        background: '#1a1a1a',
        color: '#ffffff',
    })

    if (!confirmation.isConfirmed) return

    deletingAll.value = true
    try {
        await deleteAll()
    } catch (error) {
        console.error('Failed to delete all notifications:', error)
        await $swal.fire({
            icon: 'error',
            title: 'Unable to delete notifications',
            text: 'Please try again.',
            background: '#1a1a1a',
            color: '#ffffff',
            confirmButtonColor: '#C1121F',
        })
    } finally {
        deletingAll.value = false
    }
}

onMounted(async () => {
    await fetchNotificationList()
})

</script>
