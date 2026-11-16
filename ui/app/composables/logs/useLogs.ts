
import type { LogsResponse } from '~/utils/types/logs'

const logsCacheExpiresAt: Record<string, number> = {}
const LOGS_CACHE_TTL_MS = 60 * 1000

const LogsCache: Record<string, LogsResponse> = {}
const LogsRequests = new Map<string, Promise<LogsResponse>>()

export const useLogs = () => {
    const { apiFetch } = useApiFetch()

    const fetchAdminLogs = async (
        {
            force = false,
            page = 1,
            search,
            action,
            sort,
        }: {
            force?: boolean
            page?: number
            search?: string
            action?: string
            sort?: string
        } = {}
    ): Promise<LogsResponse> => {

        const cacheKey =
            `logs-page-${page}` +
            `-search-${search ?? 'all'}` +
            `-action-${action ?? 'all'}` +
            `-sort-${sort ?? 'newest'}`

        const now = Date.now()

        const expiresAt = logsCacheExpiresAt[cacheKey]

        if (!force && cacheKey in LogsCache && expiresAt && now < expiresAt) {
            return LogsCache[cacheKey]!
        }

        const existingRequest = LogsRequests.get(cacheKey)

        if (!force && existingRequest) {
            return existingRequest
        }

        const params = new URLSearchParams()

        params.append('page', String(page))

        if (search?.trim()) params.append('search', search.trim())
        if (action) params.append('action', action)
        if (sort) params.append('sort', sort)

        const request = apiFetch<LogsResponse>(
            `/admin/logs/?${params.toString()}`
        )
            .then((data) => {
                LogsCache[cacheKey] = data
                logsCacheExpiresAt[cacheKey] = Date.now() + LOGS_CACHE_TTL_MS
                return data
            })
            .finally(() => {
                LogsRequests.delete(cacheKey)
            })

        LogsRequests.set(cacheKey, request)

        return request
    }

    return {
        fetchAdminLogs,
    }
}
