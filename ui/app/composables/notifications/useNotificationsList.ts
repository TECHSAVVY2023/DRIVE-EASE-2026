import type { Notification } from '~/utils/api/api'

const loading = ref(false)

const notifications = ref<Notification[]>([])

const count = ref(0)

const nextPage = ref<string | null>(null)
const previousPage = ref<string | null>(null)

const currentPage = ref(1)

export function useNotificationList() {
    const {
        fetchNotifications,
        fetchUnreadCount,
        markAllNotificationsAsRead: markAllNotificationsAsReadRequest,
        deleteAllNotifications: deleteAllNotificationsRequest,
        unreadCount,
    } = useNotification()

    const pageSize = 9

    const totalPages = computed(() =>
        Math.ceil(count.value / pageSize)
    )

    const fetchNotificationList = async () => {
        loading.value = true

        try {
            const res = await fetchNotifications({
                page: currentPage.value,
            })

            notifications.value = res.results

            count.value = res.count

            nextPage.value = res.next ?? null
            previousPage.value = res.previous ?? null
            await fetchUnreadCount()

        } finally {
            loading.value = false
        }
    }

    const markAllAsRead = async () => {
        await markAllNotificationsAsReadRequest()
        const readAt = new Date().toISOString()

        notifications.value.forEach(notification => {
            notification.is_read = true
            notification.read_at = readAt
        })
    }

    const deleteAll = async () => {
        await deleteAllNotificationsRequest()
        notifications.value = []
        count.value = 0
        nextPage.value = null
        previousPage.value = null
        currentPage.value = 1
    }

    watch(
        currentPage,
        () => {
            fetchNotificationList()
        }
    )

    return {
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
    }
}
