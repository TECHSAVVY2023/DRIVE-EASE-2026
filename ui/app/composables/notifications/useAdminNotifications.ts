import {
    API_ENDPOINTS,
    type AdminNotification,
    type NotificationResponse,
} from '~/utils/api/api'

export const useAdminNotifications = () => {
    const { apiFetch } = useApiFetch()
    const unreadCount = useState<number>(
        'adminNotificationUnreadCount',
        () => 0,
    )

    const fetchNotifications = async (): Promise<AdminNotification[]> => {
        const response = await apiFetch<NotificationResponse>(
            `${API_ENDPOINTS.ADMIN_NOTIFICATIONS.LIST}?page_size=100`,
        )

        return response.results as AdminNotification[]
    }

    const fetchUnreadCount = async (): Promise<number> => {
        const response = await apiFetch<{ unread_count: number }>(
            API_ENDPOINTS.ADMIN_NOTIFICATIONS.UNREAD_COUNT,
        )
        unreadCount.value = response.unread_count
        return response.unread_count
    }

    const markAsRead = async (id: number): Promise<void> => {
        await apiFetch(API_ENDPOINTS.ADMIN_NOTIFICATIONS.READ(id), {
            method: 'PATCH',
        })
        unreadCount.value = Math.max(0, unreadCount.value - 1)
    }

    const markAllAsRead = async (): Promise<void> => {
        await apiFetch(API_ENDPOINTS.ADMIN_NOTIFICATIONS.READ_ALL, {
            method: 'PATCH',
        })
        unreadCount.value = 0
    }

    const deleteNotification = async (
        id: number,
        wasUnread = false,
    ): Promise<void> => {
        await apiFetch(API_ENDPOINTS.ADMIN_NOTIFICATIONS.DELETE(id), {
            method: 'DELETE',
        })
        if (wasUnread) {
            unreadCount.value = Math.max(0, unreadCount.value - 1)
        }
    }

    return {
        fetchNotifications,
        fetchUnreadCount,
        markAsRead,
        markAllAsRead,
        deleteNotification,
        unreadCount,
    }
}
