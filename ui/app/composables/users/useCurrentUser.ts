import type { User } from '~/utils/types/accounts'

let userRequest: Promise<User | null> | null = null

export function useCurrentUser() {
    const { token, isLoggedIn } = useAuth()
    const { apiFetch } = useApiFetch()

    const user = useState<User | null>('currentUser', () => null)
    const userLoaded = useState<boolean>('currentUserLoaded', () => false)

    const clearUser = () => {
        user.value = null
        userLoaded.value = false
    }

    const fetchUser = async (force = false): Promise<User | null> => {
        if (!isLoggedIn.value) {
            clearUser()
            return null
        }

        if (!force && userLoaded.value) return user.value
        if (userRequest) return userRequest

        userRequest = (async () => {
            const requestToken = token.value

            try {
                const currentUser = await apiFetch<User>('/auth/me/')

                // Do not restore user data if logout occurred during the request.
                if (!isLoggedIn.value || token.value !== requestToken) return null

                user.value = currentUser
                userLoaded.value = true
                return currentUser
            } catch (error) {
                clearUser()
                throw error
            } finally {
                userRequest = null
            }
        })()

        return userRequest
    }

    watch(
        isLoggedIn,
        (loggedIn) => {
            if (loggedIn) void fetchUser().catch(() => {})
            else clearUser()
        },
        { immediate: true }
    )

    return {
        user,
        fetchUser,
        refreshUser: () => fetchUser(true),
        clearUser,
    }
}
