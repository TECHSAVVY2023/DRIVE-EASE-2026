
import type { AdminActivityLog, LogsResponse } from '~/utils/types/logs'
import { useLogs } from './useLogs'

const loading = ref(false)
const error = ref<string | null>(null)

const logs = ref<AdminActivityLog[]>([])

const count = ref(0)

const nextPage = ref<string | null>(null)
const previousPage = ref<string | null>(null)
const currentPage = ref(1)

export const useLogsList = () => {
    const { fetchAdminLogs } = useLogs()

    const pageSize = 5

    const search = ref('')
    const selectedAction = ref('')
    const selectedSort = ref('newest')

    const totalPages = computed(() =>
        Math.ceil(count.value / pageSize)
    )

    const fetchLogs = async (force = false) => {
        loading.value = true
        error.value = null

        try {
            const res: LogsResponse = await fetchAdminLogs({
                force,
                page: currentPage.value,
                search: search.value,
                action: selectedAction.value,
                sort: selectedSort.value,
            })

            logs.value = res.results
            count.value = res.count

            nextPage.value = res.next ?? null
            previousPage.value = res.previous ?? null
        } catch (fetchError: unknown) {
            error.value = fetchError instanceof Error
                ? fetchError.message
                : 'Unable to load activity logs.'
        } finally {
            loading.value = false
        }
    }

    // Fetch when page, search, or filters change
    watch(
        [
            currentPage,
            search,
            selectedAction,
            selectedSort,
        ],
        () => {
            fetchLogs()
        }
    )

    onMounted(() => {
        fetchLogs()
    })

    // Reset pagination when search or filters change
    watch(
        [
            search,
            selectedAction,
            selectedSort,
        ],
        () => {
            if (currentPage.value !== 1) {
                currentPage.value = 1
            }
        }
    )

    return {
        loading,
        error,
        logs,
        count,
        search,
        nextPage,
        previousPage,
        currentPage,
        pageSize,
        totalPages,
        selectedAction,
        selectedSort,
        fetchLogs
    }
}
