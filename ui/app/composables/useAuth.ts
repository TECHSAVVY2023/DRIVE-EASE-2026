/**
 * Thin auth composable — Django is source of truth.
 * Frontend stores JWT + reactive user state only.
 */

import { useApiBase } from '~/utils/api/api';

type RefreshResponse = {
    access: string;
    refresh?: string;
};

let refreshPromise: Promise<string | null> | null = null

export const useAuth = () => {
    //const user = useState<any>('user', () => null)
    const token = useState<string | null>('token', () => null)
    const authReady = useState<boolean>('authReady', () => false)

    const isLoggedIn = computed(() => !!token.value)

    const apiBase = useApiBase()

    // LOGIN CALLBACK
    const setAuth = async (access: string, refresh: string) => {

        token.value = access

        if (import.meta.client) {
            localStorage.setItem('access_token', access)
            localStorage.setItem('refresh_token', refresh)

            // console.log(
            //     'STORED REFRESH TOKEN:',
            //     localStorage.getItem('refresh_token')
            // )
        }
    }

    // INIT APP
    const init = () => {
        if (!import.meta.client) return

        const access = localStorage.getItem('access_token')

        if (access) {
            token.value = access
        }

        authReady.value = true
    }

    // REFRESH ACCESS TOKEN
    const refreshAccessToken = async () => {
        if (!import.meta.client) {
            return null
        }

        if (refreshPromise) {
            return refreshPromise
        }

        refreshPromise = (async () => {
            const refreshToken =
                localStorage.getItem('refresh_token')

            if (!refreshToken) {
                return null
            }

            try {
                const res = await $fetch<RefreshResponse>(
                    `${apiBase}/auth/token/refresh/`,
                    {
                        method: 'POST',
                        body: {
                            refresh: refreshToken
                        }
                    }
                )

                token.value = res.access

                localStorage.setItem(
                    'access_token',
                    res.access
                )

                if (res.refresh) {
                    localStorage.setItem(
                        'refresh_token',
                        res.refresh
                    )
                }

                return res.access
            } catch (error) {
                console.error(
                    'Failed to refresh access token:',
                    error
                )

                return null
            } finally {
                refreshPromise = null
            }
        })()

        return refreshPromise
    }

    const login = (): void => {
        if (!import.meta.client) return;
        const apiBase = useApiBase();
        const origin = window.location.origin;
        window.location.href = `${apiBase}/auth/google/?origin=${encodeURIComponent(origin)}`;
    };

    const logout = () => {
        if (import.meta.client) {
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
        }

        token.value = null

        if (import.meta.client) {
            navigateTo('/')
        }
    }

    return {
        token,
        isLoggedIn,
        init,
        setAuth,
        refreshAccessToken,
        logout,
        login,
        authReady
    }
}