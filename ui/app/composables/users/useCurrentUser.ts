import type { User } from '~/utils/types/accounts'

let userRequest: Promise<User | null> | null = null

export function useCurrentUser() {
    const { token, isLoggedIn, authReady } = useAuth()
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
                user.value = null
                // The request has settled. Do not leave account UI loading
                // forever when the profile endpoint returns an error.
                userLoaded.value = true
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

    const authLoading = computed(() =>
        !authReady.value || (isLoggedIn.value && !userLoaded.value)
    )

    return {
        user,
        userLoaded,
        authLoading,
        fetchUser,
        refreshUser: () => fetchUser(true),
        clearUser,
    }
}
