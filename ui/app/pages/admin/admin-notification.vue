<template>
    <div class="flex h-screen overflow-hidden bg-[#0D0D0D] font-[poppins] text-white">
        <AdminCommonSidebarNav :sidebar-open="sidebarOpen" @close-sidebar="sidebarOpen = false" />

        <div class="flex min-w-0 flex-1 flex-col overflow-hidden">
            <AdminCommonTopbarNav
                :user="user"
                :is-logged-in="isLoggedIn"
                title="Notifications"
                @open-sidebar="handleOpenSidebar"
                @close-sidebar="handleCloseSidebar"
            />

            <main class="flex-1 overflow-y-auto px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
                <div class="mb-6 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
                    <div>
                        <h1 class="text-[22px] font-extrabold">Notifications</h1>
                        <p class="mt-1 text-[13px] text-[#8a8a8a]">Stay updated on bookings, payments, reviews, and system activity</p>
                    </div>
                    <button v-if="unreadCount" type="button" class="text-xs font-semibold text-[#C1121F] transition hover:text-red-400" @click="markAllAsRead">Mark all as read</button>
                </div>

                <div class="mb-5 flex flex-wrap gap-2">
                    <button v-for="filter in filters" :key="filter.value" type="button" class="rounded-lg border px-3.5 py-2 text-xs font-semibold transition" :class="selectedFilter === filter.value ? 'border-[#C1121F] bg-[#C1121F]/10 text-white' : 'border-[#292929] bg-[#171717] text-[#8f8f8f] hover:text-white'" @click="selectedFilter = filter.value">
                        {{ filter.label }}
                        <span v-if="filter.value === 'unread'" class="ml-1 text-[#C1121F]">{{ unreadCount }}</span>
                    </button>
                </div>

                <section class="overflow-hidden rounded-xl border border-[#232323] bg-[#161616]">
                    <div class="border-b border-[#252525] p-4">
                        <label class="relative block max-w-xl">
                            <span class="sr-only">Search notifications</span>
                            <svg class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[#666]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path stroke-linecap="round" d="m20 20-3.5-3.5"/></svg>
                            <input v-model="search" type="search" placeholder="Search notifications..." class="h-10 w-full rounded-lg border border-[#2b2b2b] bg-[#0f0f0f] pl-10 pr-3 text-sm text-white outline-none placeholder:text-[#5f5f5f] focus:border-[#C1121F]" />
                        </label>
                    </div>

                    <div v-if="filteredNotifications.length" class="divide-y divide-[#242424]">
                        <article v-for="notification in filteredNotifications" :key="notification.id" class="group relative flex gap-4 p-4 transition hover:bg-white/[0.025] sm:p-5" :class="!notification.read ? 'bg-[#C1121F]/[0.035]' : ''">
                            <span v-if="!notification.read" class="absolute left-0 top-0 h-full w-0.5 bg-[#C1121F]" />
                            <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl" :class="notificationStyle[notification.type].container" v-html="notificationStyle[notification.type].icon" />

                            <button type="button" class="min-w-0 flex-1 text-left" @click="markAsRead(notification.id)">
                                <div class="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
                                    <h2 class="text-sm font-semibold" :class="notification.read ? 'text-[#c0c0c0]' : 'text-white'">{{ notification.title }}</h2>
                                    <time class="shrink-0 text-[10px] text-[#696969]">{{ relativeTime(notification.createdAt) }}</time>
                                </div>
                                <p class="mt-1.5 max-w-3xl text-xs leading-5 text-[#898989]">{{ notification.message }}</p>
                                <span class="mt-2 inline-block rounded-full bg-white/5 px-2 py-1 text-[9px] font-semibold uppercase tracking-wider text-[#777]">{{ notification.type }}</span>
                            </button>

                            <button type="button" class="self-center rounded-lg p-2 text-[#555] opacity-0 transition hover:bg-red-500/10 hover:text-red-400 group-hover:opacity-100 focus:opacity-100" aria-label="Delete notification" @click="removeNotification(notification.id)">
                                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 7h12m-10 0 1 13h6l1-13m-6 0V4h4v3"/></svg>
                            </button>
                        </article>
                    </div>

                    <div v-else class="flex flex-col items-center px-6 py-16 text-center">
                        <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-white/5 text-[#666]">
                            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.7"><path stroke-linecap="round" stroke-linejoin="round" d="M15 17H9m9-5a6 6 0 10-12 0c0 4-2 5-2 5h16s-2-1-2-5M10 21h4"/></svg>
                        </div>
                        <p class="text-sm font-semibold text-gray-300">No notifications found</p>
                        <p class="mt-1 text-xs text-[#666]">Try another filter or search term.</p>
                    </div>
                </section>
            </main>
        </div>
    </div>
</template>

<script setup lang="ts">
type NotificationType = 'booking' | 'payment' | 'review' | 'system'
type AdminNotification = { id: number; type: NotificationType; title: string; message: string; read: boolean; createdAt: string }

const { isLoggedIn } = useAuth()
const { user } = useCurrentUser()
const sidebarOpen = ref(false)
const search = ref('')
const selectedFilter = ref<'all' | 'unread' | NotificationType>('all')

// Replace this array with the result of the admin notifications API later.
const notifications = ref<AdminNotification[]>([
    { id: 1, type: 'booking', title: 'New booking requires approval', message: 'Booking BKG-71A2 for the Toyota Vios was submitted and is waiting for review.', read: false, createdAt: new Date(Date.now() - 8 * 60000).toISOString() },
    { id: 2, type: 'payment', title: 'Payment received', message: 'A payment of ₱8,500 was completed successfully for booking BKG-48CF.', read: false, createdAt: new Date(Date.now() - 42 * 60000).toISOString() },
    { id: 3, type: 'review', title: 'New customer review', message: 'A customer submitted a five-star review for the Ford Raptor.', read: false, createdAt: new Date(Date.now() - 3 * 3600000).toISOString() },
    { id: 4, type: 'system', title: 'Vehicle marked for maintenance', message: 'Toyota Wigo 003 was automatically marked unavailable after its inspection date passed.', read: true, createdAt: new Date(Date.now() - 26 * 3600000).toISOString() },
    { id: 5, type: 'booking', title: 'Rental returned', message: 'Booking BKG-193B has been marked as returned and is ready for completion.', read: true, createdAt: new Date(Date.now() - 2 * 86400000).toISOString() },
    { id: 6, type: 'payment', title: 'Payment needs attention', message: 'The payment attempt for booking BKG-92D1 failed and may require follow-up.', read: true, createdAt: new Date(Date.now() - 4 * 86400000).toISOString() },
])

const filters: { label: string; value: typeof selectedFilter.value }[] = [
    { label: 'All', value: 'all' }, { label: 'Unread', value: 'unread' }, { label: 'Bookings', value: 'booking' },
    { label: 'Payments', value: 'payment' }, { label: 'Reviews', value: 'review' }, { label: 'System', value: 'system' },
]
const notificationStyle: Record<NotificationType, { container: string; icon: string }> = {
    booking: { container: 'bg-blue-500/10 text-blue-400', icon: '<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M7 3v3m10-3v3M4 9h16M5 5h14a1 1 0 011 1v14H4V6a1 1 0 011-1Z"/></svg>' },
    payment: { container: 'bg-emerald-500/10 text-emerald-400', icon: '<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M7 15h3"/></svg>' },
    review: { container: 'bg-amber-500/10 text-amber-400', icon: '<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9L12 3Z"/></svg>' },
    system: { container: 'bg-violet-500/10 text-violet-400', icon: '<svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 00.3 1.9l.1.1-2.8 2.8-.1-.1a1.7 1.7 0 00-1.9-.3 1.7 1.7 0 00-1 1.6v.2h-4V21a1.7 1.7 0 00-1-1.6 1.7 1.7 0 00-1.9.3l-.1.1L4.2 17l.1-.1a1.7 1.7 0 00.3-1.9A1.7 1.7 0 003 14H3v-4h.1a1.7 1.7 0 001.5-1 1.7 1.7 0 00-.3-1.9L4.2 7 7 4.2l.1.1A1.7 1.7 0 009 4.6a1.7 1.7 0 001-1.5V3h4v.1a1.7 1.7 0 001 1.5 1.7 1.7 0 001.9-.3l.1-.1L19.8 7l-.1.1a1.7 1.7 0 00-.3 1.9 1.7 1.7 0 001.6 1h.1v4H21a1.7 1.7 0 00-1.6 1Z"/></svg>' },
}

const unreadCount = computed(() => notifications.value.filter(item => !item.read).length)
const filteredNotifications = computed(() => {
    const query = search.value.trim().toLowerCase()
    return notifications.value.filter(item => {
        if (selectedFilter.value === 'unread' && item.read) return false
        if (!['all', 'unread'].includes(selectedFilter.value) && item.type !== selectedFilter.value) return false
        return !query || `${item.title} ${item.message}`.toLowerCase().includes(query)
    })
})

// These handlers are intentionally isolated so API calls can replace the local mutations later.
const markAsRead = (id: number) => { const item = notifications.value.find(entry => entry.id === id); if (item) item.read = true }
const markAllAsRead = () => { notifications.value.forEach(item => { item.read = true }) }
const removeNotification = (id: number) => { notifications.value = notifications.value.filter(item => item.id !== id) }
const relativeTime = (value: string) => {
    const minutes = Math.max(1, Math.floor((Date.now() - new Date(value).getTime()) / 60000))
    if (minutes < 60) return `${minutes}m ago`
    if (minutes < 1440) return `${Math.floor(minutes / 60)}h ago`
    return `${Math.floor(minutes / 1440)}d ago`
}
const handleOpenSidebar = () => { sidebarOpen.value = true }
const handleCloseSidebar = () => { sidebarOpen.value = false }

onMounted(() => document.documentElement.classList.add('admin-page'))
onBeforeUnmount(() => document.documentElement.classList.remove('admin-page'))
</script>
