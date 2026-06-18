import { useApiBase } from '~/utils/api/api'

export const useApiFetch = () => {
    const { token, refreshAccessToken, logout } = useAuth()
    const apiBase = useApiBase()

    const apiFetch = async <T>(
        url: string,
        options: any = {}
    ): Promise<T> => {

        const makeRequest = (jwt?: string) => {
            console.log('making request with token:', jwt)
            console.log('url:', `${apiBase}${url}`)
            
            return $fetch<T>(`${apiBase}${url}`, {
                ...options,
                headers: {
                    ...options.headers,
                    ...(jwt ? { Authorization: `Bearer ${jwt}` } : {}),
                },
            })
        }

        try {
            // 1st attempt
            console.log('checking if token expired...')
            return await makeRequest(token.value ?? undefined)
            
        } catch (err: any) {

            console.log('handling error...')

            const status = err?.response?.status || err?.status

            console.log('status:', status)
            console.log('error:', err)

            // Only handle JWT expiry
            if (status === 401) {

                console.log('getting new refresh token...')

                // try refresh
                const newToken = await refreshAccessToken()

                if (!newToken) {
                    console.log('no new token:', newToken)
                    logout()
                    throw err
                }

                // retry original request ONCE
                return await makeRequest(newToken)
            }

            throw err
        }
    }
    console.log('token not expired and all good')

    return { apiFetch }
}