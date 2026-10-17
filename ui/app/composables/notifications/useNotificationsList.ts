import type { Notification } from '~/utils/api/api'

const loading = ref(false)

const notifications = ref<Notification[]>([])

const count = ref(0)

const nextPage = ref<string | null>(null)
const previousPage = ref<string | null>(null)

const currentPage = ref(1)

export function useNotificationList() {
    const { fetchNotifications } = useNotification()

    const pageSize = 9

    const totalPages = computed(() =>
        Math.ceil(count.value / pageSize)
    )

    const unreadCount = computed(() =>
        notifications.value.filter(
            notification => !notification.is_read
        ).length
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

        } finally {
            loading.value = false
        }
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
    }
}