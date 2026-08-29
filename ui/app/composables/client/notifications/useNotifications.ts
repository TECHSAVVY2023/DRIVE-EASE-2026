import { type NotificationResponse } from '~/utils/api/api'

const notificationCacheExpiresAt: Record<string, number> = {}
const NOTIFICATION_CACHE_TTL_MS = 60 * 1000
const NotificationCache: Record<string, NotificationResponse> = {}
const NotificationRequests = new Map<string, Promise<NotificationResponse>>()

export const useNotification = () => {
    const { apiFetch } = useApiFetch()
    
    const fetchNotifications = async (
        { force = false, page = 1 }: { force?: boolean; page?: number } = {}
    ): Promise<NotificationResponse> => {
        const cacheKey = `notifications-page-${page}`
        const now = Date.now()
        const expiresAt = notificationCacheExpiresAt[cacheKey]
        
        if (!force && cacheKey in NotificationCache && expiresAt && now < expiresAt) {
        return NotificationCache[cacheKey]
        }
        
        const existingRequest = NotificationRequests.get(cacheKey)
        if (!force && existingRequest) {
        return existingRequest
        }
        
        const params = new URLSearchParams()
        params.append('page', String(page))
        
        const request = apiFetch<NotificationResponse>(`/notifications/?${params.toString()}`)
        .then((data) => {
            NotificationCache[cacheKey] = data
            notificationCacheExpiresAt[cacheKey] = Date.now() + NOTIFICATION_CACHE_TTL_MS
            return data
        })
        .finally(() => {
            NotificationRequests.delete(cacheKey)
        })
        
        NotificationRequests.set(cacheKey, request)
        return request
    }

    const fetchUnreadCount = async (): Promise<number> => {
        const response = await apiFetch<{ unread_count: number }>(
            '/notifications/unread-count/'
        )

        return response.unread_count
    }

    const markNotificationAsRead = async (notificationId: number) => {
        return await apiFetch(
            `/notifications/${notificationId}/read/`,
            {
                method: 'PATCH',
            }
        )
    }
    
    return { fetchNotifications, fetchUnreadCount, markNotificationAsRead }
}