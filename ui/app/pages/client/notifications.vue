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
                <NotificationHeader
                    :notifications="notifications"
                    :total="count"
                    :unread-count="unreadCount"
                />

                <NotificationList
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
} = useNotificationList()

onMounted(async () => {
    await fetchNotificationList()
})

</script>
