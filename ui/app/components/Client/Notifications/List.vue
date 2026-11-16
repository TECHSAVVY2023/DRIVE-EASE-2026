<template>
    <div>
        <!-- Empty State -->
        <div
            v-if="notifications.length === 0"
            class="flex flex-col items-center justify-center gap-3 px-5 py-16 text-center"
        >
            <div class="w-14 h-14 rounded-lg flex items-center justify-center bg-[#2a2a2a]">
                <svg
                    class="w-7 h-7 text-gray-500"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                    />
                </svg>
            </div>

            <p class="text-white text-sm font-semibold">
                No notifications yet
            </p>

            <p class="text-gray-500 text-xs max-w-[220px] leading-relaxed">
                You're all caught up. We'll let you know when something new comes in.
            </p>
        </div>

        <!-- Notifications -->
        <div class="flex flex-col divide-y divide-[#1f1f1f]">
            <div
                v-for="notification in visibleNotifications"
                :key="notification.id"
                class="flex items-start gap-4 px-5 py-4 transition-colors duration-150"
                :class="
                    !notification.is_read
                        ? 'bg-[#1f1f1f]'
                        : 'hover:bg-[#1f1f1f]'
                "
            >
                <!-- Unread indicator + Icon -->
                <div class="flex flex-col items-center gap-1.5 flex-shrink-0 pt-0.5">
                    <div
                        class="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                        :class="notification.is_read
                            ? 'bg-[#2a2a2a]'
                            : 'bg-[#C1121F]'"
                    >
                        <svg
                            class="w-5 h-5 text-white"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                :d="getNotificationIcon(notification.notification_type)"
                            />
                        </svg>
                    </div>
                </div>

                <!-- Content -->
                <div class="flex-1 min-w-0">
                    <div class="flex items-start justify-between gap-3">
                        <p class="text-white text-sm font-semibold leading-snug">
                            {{ notification.title }}
                        </p>

                        <span
                            class="text-gray-500 text-xs flex-shrink-0 whitespace-nowrap"
                        >
                            {{ formatNotificationTime(notification.created_at) }}
                        </span>
                    </div>

                    <p class="text-gray-400 text-xs leading-relaxed mt-1">
                        {{ notification.message }}
                    </p>

                    <NuxtLink
                        v-if="notification.action_url"
                        :to="notification.action_url"
                        @click="handleNotificationClick(notification)"
                        class="text-[#C1121F] text-xs font-medium mt-2 inline-flex items-center gap-1 hover:underline"
                    >
                        {{ getActionLabel(notification.action_url) }}

                        <svg
                            class="w-3 h-3"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M9 5l7 7-7 7"
                            />
                        </svg>
                    </NuxtLink>
                </div>
            </div>
        </div>

        <!-- View More -->
        <div
            v-if="notifications.length > 0"
            class="flex flex-col items-center gap-2 px-5 py-5 border-t border-[#222]"
        >
            <button
                v-if="visibleCount < notifications.length"
                @click="visibleCount += 3"
                class="flex items-center gap-2 bg-[#C1121F] hover:bg-red-700 text-white text-sm font-semibold px-8 py-3 rounded-lg transition-colors duration-200"
            >
                View more

                <svg
                    class="w-4 h-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 5l7 7-7 7"
                    />
                </svg>
            </button>

            <p class="text-gray-500 text-xs">
                {{ displayedCount }} out of {{ notifications.length }} notifications
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Notification } from '~/utils/api/api'

const props = defineProps<{
    notifications: Notification[]
}>()

const visibleCount = ref(3)

const visibleNotifications = computed(() =>
    props.notifications.slice(0, visibleCount.value)
)

const displayedCount = computed(() =>
    Math.min(visibleCount.value, props.notifications.length)
)

const notificationIcons: Record<string, string> = {
    booking: 'M6.75 3v2.25M17.25 3v2.25M3.75 8.25h16.5M5.25 4.5h13.5a1.5 1.5 0 0 1 1.5 1.5v13.5H3.75V6a1.5 1.5 0 0 1 1.5-1.5Z',
    booking_status: 'm9 12.75 2.25 2.25L15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z',
    payment: 'M2.25 8.25h19.5M4.5 5.25h15A2.25 2.25 0 0 1 21.75 7.5v9A2.25 2.25 0 0 1 19.5 18.75h-15A2.25 2.25 0 0 1 2.25 16.5v-9A2.25 2.25 0 0 1 4.5 5.25ZM6.75 15h2.25',
    review: 'm11.48 3.499 2.09 4.233 4.671.679-3.38 3.294.798 4.652-4.179-2.197-4.179 2.197.798-4.652-3.38-3.294 4.671-.679 2.09-4.233Z',
    reminder: 'M12 6v6l4 2M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z',
    system: 'M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0',
}

const getNotificationIcon = (type: string): string => {
    return notificationIcons[type] ?? notificationIcons.system!
}

const getActionLabel = (actionUrl: string | null) => {
    if (actionUrl?.startsWith('/client/profile')) {
        return 'View profile'
    }

    if (actionUrl?.startsWith('/client/transaction-details')) {
        return 'View booking details'
    }

    return 'View details'
}

const formatNotificationTime = (date: string) => {
    const notificationDate = new Date(date)
    const now = new Date()

    const difference = now.getTime() - notificationDate.getTime()

    const minutes = Math.floor(difference / (1000 * 60))
    const hours = Math.floor(difference / (1000 * 60 * 60))
    const days = Math.floor(difference / (1000 * 60 * 60 * 24))

    if (minutes < 1) return 'Just now'
    if (minutes < 60) return `${minutes}m ago`
    if (hours < 24) return `${hours}h ago`
    if (days < 7) return `${days}d ago`

    return notificationDate.toLocaleDateString()
}

const { markNotificationAsRead } = useNotification()

const handleNotificationClick = async (notification: Notification) => {
    if (!notification.is_read) {
        await markNotificationAsRead(notification.id)

        notification.is_read = true
    }
}

</script>
