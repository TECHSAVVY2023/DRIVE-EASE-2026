<template>
   <MobileDrawer
      :menu-open="menuOpen"
      @close-menu="closeMenu"
   />

   <Navbar
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
                <div class="flex items-start justify-between gap-4 px-5 pt-5 pb-4 border-b border-[#222]">
                <div>
                    <h2 class="text-white font-extrabold text-base">All notifications</h2>
                    <p class="text-gray-400 text-xs mt-0.5">
                    {{ notifications.length }} total / {{ unreadCount }} unread
                    </p>
                </div>
                <div class="flex items-center gap-2 flex-shrink-0">
                    <button class="text-xs border border-[#2a2a2a] text-gray-400 px-3 py-1.5 rounded-lg hover:border-white hover:text-white transition-colors duration-200">
                    Mark all as read
                    </button>
                    <button class="text-xs border border-[#2a2a2a] text-gray-400 px-3 py-1.5 rounded-lg hover:border-red-500 hover:text-red-400 transition-colors duration-200">
                    Delete all
                    </button>
                </div>
                </div>

                <!-- Notification List -->
                <div class="flex flex-col divide-y divide-[#1f1f1f]">
                <div
                    v-for="(notif, i) in visibleNotifications"
                    :key="i"
                    class="flex items-start gap-4 px-5 py-4 transition-colors duration-150"
                    :class="!notif.read ? 'bg-[#1f1f1f]' : 'hover:bg-[#1f1f1f]'"
                >
                    <!-- Unread indicator + Icon -->
                    <div class="flex flex-col items-center gap-1.5 flex-shrink-0 pt-0.5">
                    <div
                        class="w-1.5 h-1.5 rounded-full flex-shrink-0"
                        :class="!notif.read ? 'bg-[#C1121F]' : 'bg-transparent'"
                    ></div>
                    <div
                        class="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                        :class="notif.iconBg"
                    >
                        <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="notif.iconPath"/>
                        </svg>
                    </div>
                    </div>

                    <!-- Content -->
                    <div class="flex-1 min-w-0">
                    <div class="flex items-start justify-between gap-3">
                        <p class="text-white text-sm font-semibold leading-snug">{{ notif.title }}</p>
                        <span class="text-gray-500 text-xs flex-shrink-0 whitespace-nowrap">{{ notif.time }}</span>
                    </div>
                    <p class="text-gray-400 text-xs leading-relaxed mt-1">{{ notif.message }}</p>
                    <a href="#" class="text-[#C1121F] text-xs font-medium mt-2 inline-flex items-center gap-1 hover:underline">
                        View booking details
                        <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                        </svg>
                    </a>
                    </div>
                </div>
                </div>

                <!-- View More -->
                <div class="flex flex-col items-center gap-2 px-5 py-5 border-t border-[#222]">
                <button
                    v-if="visibleCount < notifications.length"
                    @click="visibleCount += 3"
                    class="flex items-center gap-2 bg-[#C1121F] hover:bg-red-700 text-white text-sm font-semibold px-8 py-3 rounded-lg transition-colors duration-200"
                >
                    View more
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                    </svg>
                </button>
                <p class="text-gray-500 text-xs">{{ displayedCount }} out of {{ notifications.length }} notifications</p>
                </div>

            </div>
        </div>

    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const route = useRoute()
const { setAuth } = useAuth()

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

if (route.query.token) {
    await setAuth(route.query.token as string)
}

const displayedCount = computed(() =>
  Math.min(visibleCount.value, notifications.value.length)
)

interface Notification {
  title: string
  message: string
  time: string
  read: boolean
  iconPath: string
  iconBg: string
}

const visibleCount = ref<number>(3)

const notifications = ref<Notification[]>([
    {
        title: 'Booking confirmed — Toyota Wigo',
        message: 'Your booking #1042 for Toyota Wigo 2026 has been confirmed. Pickup is scheduled on May 10, 2026 at 9:00 AM at CDO Main Branch.',
        time: '1 hour ago',
        read: false,
        iconPath: 'M5 13l4 4L19 7',
        iconBg: 'bg-[#C1121F]',
    },
    {
        title: 'New booking request submitted',
        message: 'You\'ve successfully submitted a booking request for Honda CRV · 3 days · May 14–17, 2026. Awaiting confirmation from our team.',
        time: '1 hour ago',
        read: false,
        iconPath: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
        iconBg: 'bg-[#C1121F]',
    },
    {
        title: 'Booking cancelled — Ford Explorer',
        message: 'Your booking #1038 for Ford Explorer has been cancelled as requested. A refund of ₱5,000 has been processed and will reflect in 3–5 business days.',
        time: '1 hour ago',
        read: false,
        iconPath: 'M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636',
        iconBg: 'bg-[#C1121F]',
    },
    {
        title: 'Payment received — Toyota Vios',
        message: 'We have received your payment of ₱1,800 for Toyota Vios rental on May 5, 2026. Thank you!',
        time: '2 hours ago',
        read: true,
        iconPath: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
        iconBg: 'bg-[#2a2a2a]',
    },
    {
        title: 'Reminder — Return your rental',
        message: 'This is a reminder that your Toyota Innova rental is due for return tomorrow, May 8, 2026 at 5:00 PM. Please ensure the car is returned on time.',
        time: '5 hours ago',
        read: true,
        iconPath: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
        iconBg: 'bg-[#2a2a2a]',
    },
    {
        title: 'Review request — Toyota Wigo',
        message: 'How was your experience with Toyota Wigo? Leave a review to help other renters make better decisions.',
        time: '1 day ago',
        read: true,
        iconPath: 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z',
        iconBg: 'bg-[#2a2a2a]',
    },
    {
        title: 'Account verified',
        message: 'Your account has been successfully verified. You can now book cars and access all features.',
        time: '2 days ago',
        read: true,
        iconPath: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z',
        iconBg: 'bg-[#2a2a2a]',
    },
])

const unreadCount = computed<number>(() => notifications.value.filter(n => !n.read).length)
const visibleNotifications = computed<Notification[]>(() => notifications.value.slice(0, visibleCount.value))
</script>