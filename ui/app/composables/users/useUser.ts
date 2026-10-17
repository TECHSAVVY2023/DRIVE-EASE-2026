import { type UsersResponse, type UsersStats } from "~/utils/api/api"

const userCacheExpiresAt: Record<string, number> = {}
const USER_CACHE_TTL_MS = 60 * 1000

const UserCache: Record<string, UsersResponse> = {}
const UserRequests = new Map<string, Promise<UsersResponse>>()

export const useUsers = () => {
    const { apiFetch } = useApiFetch()

    const fetchUsersList = async (
        {
            force = false,
            page = 1,
            search,
            status,
            role,
        }: {
            force?: boolean
            page?: number
            search?: string
            status?: string
            role?: string
        } = {}
    ): Promise<UsersResponse> => {

        const cacheKey =
            `users-page-${page}` +
            `-search-${search ?? "all"}` +
            `-status-${status ?? "all"}` +
            `-role-${role ?? "all"}`

        const now = Date.now()
        const expiresAt = userCacheExpiresAt[cacheKey]

        // Return cached response if still valid
        if (
            !force &&
            cacheKey in UserCache &&
            expiresAt &&
            now < expiresAt
        ) {
            return UserCache[cacheKey]
        }

        // Reuse an existing request
        const existingRequest = UserRequests.get(cacheKey)

        if (!force && existingRequest) {
            return existingRequest
        }

        const params = new URLSearchParams()

        params.append("page", String(page))

        if (search) {
            params.append("search", search)
        }

        if (status) {
            params.append("status", status)
        }

        if (role) {
            params.append("role", role)
        }

        const request = apiFetch<UsersResponse>(
            `/users/?${params.toString()}`
        )
            .then((data) => {
                UserCache[cacheKey] = data

                userCacheExpiresAt[cacheKey] =
                    Date.now() + USER_CACHE_TTL_MS

                return data
            })
            .finally(() => {
                UserRequests.delete(cacheKey)
            })

        UserRequests.set(cacheKey, request)

        return request
    }

    const fetchUsersStats = async (): Promise<UsersStats> => {
        return await apiFetch<UsersStats>('/users/stats/')
    }

    return {
        fetchUsersStats,
        fetchUsersList,
    }
}