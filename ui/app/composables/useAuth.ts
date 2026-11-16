import { useApiBase } from '~/utils/api/api'

type RefreshResponse = {
    access: string
}

let refreshPromise: Promise<string | null> | null = null
let initPromise: Promise<void> | null = null
let authGeneration = 0

const TOKEN_EXPIRY_SKEW_MS = 30_000
const REFRESH_LOCK_NAME = 'driveease-auth-refresh'

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
    const authFailureReason = useState<string | null>('authFailureReason', () => null)
    const isLoggedIn = computed(() => Boolean(token.value))
    const apiBase = useApiBase()

    const clearAuth = () => {
        authGeneration += 1
        token.value = null
        useState('currentUser').value = null
        useState<boolean>('currentUserLoaded', () => false).value = false
    }

    const setAuth = (access: string) => {
        // Prevent an older in-flight refresh from replacing or clearing a
        // newer authenticated session.
        authGeneration += 1
        token.value = access
    }

    const refreshAccessToken = (): Promise<string | null> => {
        if (!import.meta.client) return Promise.resolve(null)
        if (refreshPromise) return refreshPromise

        refreshPromise = (async () => {
            const requestGeneration = authGeneration

            try {
                const requestRefresh = async (): Promise<RefreshResponse | null> => {
                    // The auth state may have changed while this page was
                    // waiting for another tab or reload to finish refreshing.
                    if (requestGeneration !== authGeneration) return null

                    return await $fetch<RefreshResponse>(
                        `${apiBase}/auth/token/refresh/`,
                        {
                            method: 'POST',
                            credentials: 'include',
                            // Let an already-started rotation finish during a
                            // reload so its Set-Cookie response is not lost.
                            keepalive: true,
                        },
                    )
                }

                // The module-level promise deduplicates requests in this page.
                // Web Locks extends that protection across tabs and reloads.
                const response = 'locks' in navigator
                    ? await navigator.locks.request(REFRESH_LOCK_NAME, requestRefresh)
                    : await requestRefresh()

                if (!response) return null

                // A logout may have happened while the request was in flight.
                if (requestGeneration !== authGeneration) return null

                token.value = response.access

                return response.access
            } catch (error: unknown) {
                const fetchError = error as {
                    data?: { code?: string }
                    response?: { _data?: { code?: string } }
                }
                const code = fetchError.data?.code
                    ?? fetchError.response?._data?.code

                if (code === 'account_suspended') {
                    authFailureReason.value = 'suspended'
                }

                if (requestGeneration === authGeneration) clearAuth()
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

        authFailureReason.value = null
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
        authFailureReason,
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
