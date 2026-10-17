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

    <div class="min-h-screen bg-[#0D0D0D] font-[poppins]">

        <Banner 
            subtitle="Stay updated"
            title="Notifications"
            :breadcrumbs="[
                { label: 'Home', to: '/' },
                { label: 'Notifications' }
            ]"
        />

        <div class="max-w-2xl mx-auto px-4 py-8">
            <div class="bg-[#1a1a1a] border border-[#222] rounded-xl overflow-hidden flex flex-col">

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