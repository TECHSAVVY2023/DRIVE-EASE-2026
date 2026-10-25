import { useApiBase } from '~/utils/api/api'

export const useApiFetch = () => {
    const { token, authReady, init, refreshAccessToken, invalidateAuth } = useAuth()
    const apiBase = useApiBase()

    const apiFetch = async <T>(
        url: string,
        options: any = {},
    ): Promise<T> => {
        if (import.meta.client && !authReady.value) {
            await init()
        }

        const makeRequest = (accessToken?: string) => {
            const headers = new Headers(options.headers as HeadersInit | undefined)

            if (accessToken) {
                headers.set('Authorization', `Bearer ${accessToken}`)
            }

            return $fetch<T>(`${apiBase}${url}`, {
                ...options,
                headers,
            })
        }

        try {
            return await makeRequest(token.value ?? undefined)
        } catch (error: unknown) {
            const fetchError = error as {
                response?: { status?: number }
                status?: number
            }
            const status = fetchError.response?.status ?? fetchError.status

            if (status !== 401 || !import.meta.client) throw error

            const newToken = await refreshAccessToken()

            if (!newToken) {
                invalidateAuth()
                throw error
            }

            return await makeRequest(newToken)
        }
    }

    return { apiFetch }
}
