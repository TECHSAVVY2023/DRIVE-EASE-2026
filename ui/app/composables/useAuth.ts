import { useApiBase } from '~/utils/api/api'

type RefreshResponse = {
    access: string
}

let refreshPromise: Promise<string | null> | null = null
let initPromise: Promise<void> | null = null
let authGeneration = 0

const TOKEN_EXPIRY_SKEW_MS = 30_000

const tokenIsUsable = (token: string): boolean => {
    try {
        const payload = token.split('.')[1]
        if (!payload) return false

        const base64 = payload.replace(/-/g, '+').replace(/_/g, '/')
        const normalized = base64.padEnd(Math.ceil(base64.length / 4) * 4, '=')
        const decoded = JSON.parse(atob(normalized)) as { exp?: number }

        return typeof decoded.exp === 'number'
            && decoded.exp * 1000 > Date.now() + TOKEN_EXPIRY_SKEW_MS
    } catch {
        return false
    }
}

export const useAuth = () => {
    const token = useState<string | null>('token', () => null)
    const authReady = useState<boolean>('authReady', () => false)
    const isLoggedIn = computed(() => Boolean(token.value))
    const apiBase = useApiBase()

    const clearAuth = () => {
        authGeneration += 1
        token.value = null
        useState('currentUser').value = null
        useState<boolean>('currentUserLoaded', () => false).value = false
    }

    const setAuth = (access: string) => {
        token.value = access
    }

    const refreshAccessToken = (): Promise<string | null> => {
        if (!import.meta.client) return Promise.resolve(null)
        if (refreshPromise) return refreshPromise

        refreshPromise = (async () => {
            const requestGeneration = authGeneration

            try {
                const response = await $fetch<RefreshResponse>(
                    `${apiBase}/auth/token/refresh/`,
                    {
                        method: 'POST',
                        credentials: 'include',
                    },
                )

                // A logout may have happened while the request was in flight.
                if (requestGeneration !== authGeneration) return null

                token.value = response.access

                return response.access
            } catch {
                clearAuth()
                return null
            } finally {
                refreshPromise = null
            }
        })()

        return refreshPromise
    }

    const init = (): Promise<void> => {
        if (!import.meta.client || authReady.value) return Promise.resolve()
        if (initPromise) return initPromise

        initPromise = (async () => {
            // Remove tokens stored by versions prior to the HttpOnly-cookie migration.
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')

            if (!token.value || !tokenIsUsable(token.value)) {
                await refreshAccessToken()
            }

            authReady.value = true
        })().finally(() => {
            initPromise = null
        })

        return initPromise
    }

    const login = () => {
        if (!import.meta.client) return

        const origin = window.location.origin
        window.location.assign(
            `${apiBase}/auth/google/?origin=${encodeURIComponent(origin)}`,
        )
    }

    const invalidateAuth = () => {
        clearAuth()
        authReady.value = true
    }

    const logout = async () => {
        invalidateAuth()

        if (import.meta.client) {
            try {
                await $fetch(`${apiBase}/auth/logout/`, {
                    method: 'POST',
                    credentials: 'include',
                })
            } catch {
                // Local logout must still complete if the API is offline.
            }

            await navigateTo('/')
        }
    }

    return {
        token,
        isLoggedIn,
        authReady,
        init,
        setAuth,
        refreshAccessToken,
        invalidateAuth,
        logout,
        login,
    }
}
