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

const getNotificationIcon = (type: string) => {
    switch (type) {
        case 'booking':
            return 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z'

        case 'payment':
            return 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2-.448 2-1s-.89-1-2-1-2 .448-2 1 .89 1 2 1zm0 0V5m0 14v-2'

        default:
            return 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9'
    }
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
