<template>
    <!-- Sidebar -->
    <aside
        :class="[
            'fixed top-0 left-0 z-50 h-screen w-80 md:static sm:w-80 md:w-56 bg-[#1B1B1B] border-r border-[#1f1f1f] flex flex-col transition-transform duration-300',
            sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        ]"
    >

        <!-- Nav -->
        <nav class="flex flex-col flex-1 gap-1 py-6 gap-1 text-xs overflow-y-auto">
            
            <!-- Mobile Close Button -->
            <div class="flex items-center justify-between md:hidden px-4 py-2">

                <p class="text-white text-lg font-semibold">Menu</p>

                <button
                    @click="$emit('close-sidebar')"
                    class="
                        w-fit p-2
                        flex items-center justify-center
                        rounded-md
                        text-white hover:text-white
                        transition-colors duration-200
                    "
                >
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <router-link
                :key="dashboardItem.key"
                :to="dashboardItem.link" 
                class="
                    flex items-center gap-3 mb-1
                    px-4 py-3 md:py-2.5
                    font-semibold
                "
                :class="activeItem === dashboardItem.key
                ? 'bg-[#252525] text-white font-semibold border-l-4 border-[#c1121f]'
                : 'text-[#7E7E7E] hover:text-white hover:bg-[#232323]'"
            >
                <div v-html="icons.home"></div>
                <span>{{ dashboardItem.label }}</span>
            </router-link>

            <p class="text-[#444] uppercase font-bold text-[10px] px-4 mb-1">
                Main
            </p>

            <router-link
                v-for="item in menu.filter(i => i.section === 'main')"
                :key="item.key"
                :to="item.link"
                class="flex items-center justify-between gap-3 px-4 py-3 md:py-2.5 transition-colors duration-200"
                :class="activeItem === item.key
                    ? 'bg-[#252525] text-white font-semibold border-l-4 border-[#c1121f]'
                    : 'text-[#7E7E7E] hover:text-white hover:bg-[#232323]'"
            >
                <div class="flex items-center gap-3 min-w-0">
                    
                    <div v-html="icons[item.icon]"></div>
                    <span class="truncate">
                        {{ item.label }}
                    </span>

                </div>

                <span
                v-if="item.badge"
                class="bg-[#C1121F] text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full"
                >
                {{ item.badge }}
                </span>
            </router-link>
            
            <p class="text-[#444] uppercase font-bold text-[10px] px-4 mb-1">
                Report
            </p>

            <router-link
                v-for="item in menu.filter(i => i.section === 'report')"
                :key="item.key"
                :to="item.link"
                class="flex items-center justify-between gap-3 px-4 py-3 md:py-2.5 transition-colors duration-200"
                :class="activeItem === item.key
                    ? 'bg-[#252525] text-white font-semibold border-l-4 border-[#c1121f]'
                    : 'text-[#7E7E7E] hover:text-white hover:bg-[#232323]'"
            >
                <div class="flex items-center gap-3 min-w-0">
                    
                    <div v-html="icons[item.icon]"></div>
                    <span class="truncate">
                        {{ item.label }}
                    </span>

                </div>

                <span
                v-if="item.badge"
                class="bg-[#C1121F] text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full"
                >
                {{ item.badge }}
                </span>
            </router-link>

        </nav>

    </aside>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

defineProps<{
    sidebarOpen: boolean
}>()

defineEmits<{
    (e: 'close-sidebar'): void
}>()

const icons: Record<string, any> = {
    home: `
        <svg class="w-5 h-5 md:w-4 md:h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
            />
        </svg>
    `,
    bell: `
        <svg class="w-5 h-5 md:w-4 md:h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
            />
        </svg>
    `,
    clipboard: `
        <svg class="w-5 h-5 md:w-4 md:h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
        </svg>
    `,
    bolt: `
        <svg class="w-5 h-5 md:w-4 md:h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13 10V3L4 14h7v7l9-11h-7z"
            />
        </svg>
    `,
    users: `
        <svg class="w-5 h-5 md:w-4 md:h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0"
            />
        </svg>
    `,
    clock: `
        <svg class="w-5 h-5 md:w-4 md:h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
            />
        </svg>
    `,
    chart: `
        <svg class="w-5 h-5 md:w-4 md:h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
        </svg>
    `
}

const dashboardItem = {
    key: 'dashboard',
    label: 'Dashboard',
    icon: 'home',
    link: '/admin-dashboard'
}

const menu = [
    {
        key: 'notifications',
        label: 'Notifications',
        icon: 'bell',
        badge: 67,
        section: 'main',
        link: '/admin/notifications'
    },
    {
        key: 'bookings',
        label: 'Bookings',
        icon: 'clipboard',
        section: 'main',
        link: '/admin/bookings'
    },
    {
        key: 'fleet',
        label: 'Fleet',
        icon: 'bolt',
        section: 'main',
        link: '/admin-fleet'
    },
    {
        key: 'users',
        label: 'Users',
        icon: 'users',
        section: 'main',
        link: '/admin/users'
    },
    {
        key: 'analytics',
        label: 'Analytics',
        icon: 'chart',
        section: 'report',
        link: '/admin/analytics'    
    },
    {
        key: 'logs',
        label: 'Activity logs',
        icon: 'clock',
        section: 'report',
        link: '/admin/logs'
    }
]

const activeItem = computed(() => {
    const match = menu.find(item => item.link === route.path)
    return match?.key || 'dashboard'
})
</script>