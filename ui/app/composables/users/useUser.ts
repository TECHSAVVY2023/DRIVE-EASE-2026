import {
    type AdminEditUserPayload, type AdminEditUserResponse,
    type AssignRoleResponse, type UserRole, type UsersResponse, type UsersStats,
    type UpdateUserStatusResponse
} from "~/utils/types/accounts"

const userCacheExpiresAt: Record<string, number> = {}
const USER_CACHE_TTL_MS = 60 * 1000

const UserCache: Record<string, UsersResponse> = {}
const UserRequests = new Map<string, Promise<UsersResponse>>()

const clearUserCache = () => {
    Object.keys(UserCache).forEach(key => delete UserCache[key])
    Object.keys(userCacheExpiresAt).forEach(
        key => delete userCacheExpiresAt[key]
    )
}

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

    const assignUserRole = async (
        userId: number,
        role: UserRole,
    ): Promise<AssignRoleResponse> => {
        const response = await apiFetch<AssignRoleResponse>(
            `/users/${userId}/role/`,
            {
                method: 'PATCH',
                body: { role },
            },
        )

        clearUserCache()

        return response
    }

    const updateUserAdmin = async (
        userId: number,
        body: AdminEditUserPayload,
    ): Promise<AdminEditUserResponse> => {
        const response = await apiFetch<AdminEditUserResponse>(
            `/admin/accounts/${userId}/`,
            {
                method: "PATCH",
                body
            }
        )

        clearUserCache()

        return response
    }

    return {
        fetchUsersStats,
        fetchUsersList,
        assignUserRole,
        updateUserAdmin,
    }
}
