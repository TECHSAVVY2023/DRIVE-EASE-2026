/**
 * Thin auth composable — Django is source of truth.
 * Frontend stores JWT + reactive user state only.
 */

import { useApiBase } from '~/utils/api/api';

interface AuthUser {
    id: number | string;
    given_name?: string;
    profile_picture?: string;
}

interface UserProfile extends AuthUser {
    family_name?: string;
    email?: string;
    contact_number?: string;
    address?: string;
}

type RefreshResponse = {
    access: string;
};

export const useAuth = () => {
    //const user = useState<any>('user', () => null)
    const token = useState<string | null>('token', () => null)

    const isLoggedIn = computed(() => !!token.value)

    const apiBase = useApiBase()

    // LOGIN CALLBACK
    const setAuth = async (access: string, refresh: string) => {
        console.log('setting auth with access:', access, 'and refresh:', refresh)
        
        token.value = access

        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)

    }

    // INIT APP
    const init = async () => {
        if (!import.meta.client) return
        console.log('starting init...')
        const access = localStorage.getItem('access_token')

        if (!access) return

        token.value = access
        console.log('token set to:', access)
        //console.log('token user value:', !user.value)

        // if (!user.value) {
        //     console.log('user state:', user.value)
        //     //await refreshUser()
        // }
    }

    // GET USER
    // const refreshUser = async () => {
    //     console.log('starting refreshUser...')
    //     console.log('token:', token.value)
    //     try {
    //         if (!token.value) {
    //             console.log('no token, returning')
    //             return
    //         }

    //         const data = await $fetch(`${apiBase}/auth/me/`, {
    //             headers: {
    //                 Authorization: `Bearer ${token.value}`
    //             }
    //         })

    //         user.value = data
    //         console.log('user set to:', data)
    //     } catch (err: any) {
    //         console.log('User fetch failed:', err?.response?.status)

    //         const newToken = await refreshAccessToken()

    //         if (!newToken) {
    //             logout()
    //             return
    //         }

    //         // 🔥 retry request after refresh
    //         const data = await $fetch(`${apiBase}/auth/me/`, {
    //             headers: {
    //                 Authorization: `Bearer ${newToken}`
    //             }
    //         })

    //         user.value = data
    //     }
    // }

    // REFRESH ACCESS TOKEN
    const refreshAccessToken = async () => {
        console.log(
            'activating refresh token:',
            localStorage.getItem('refresh_token')
        )
        try {
            const res = await $fetch<RefreshResponse>(`${apiBase}/auth/token/refresh/`, {
                method: 'POST',
                body: { refresh: localStorage.getItem('refresh_token') }
            })

            token.value = res.access
            localStorage.setItem('access_token', res.access)

            return res.access
        } catch {
            return null
        }
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
        login
    }
}