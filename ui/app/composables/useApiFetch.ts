import { useApiBase } from '~/utils/api/api'

export const useApiFetch = () => {
    const { token, refreshAccessToken, logout } = useAuth()
    const apiBase = useApiBase()

    const apiFetch = async <T>(
        url: string,
        options: any = {}
    ): Promise<T> => {

        console.log('========== API FETCH START ==========')
        console.log('URL:', `${apiBase}${url}`)
        console.log('TOKEN EXISTS:', !!token.value)
        console.log('TOKEN:', token.value)

        const makeRequest = (jwt?: string) => {
            console.log('--- MAKE REQUEST ---')
            console.log('JWT EXISTS:', !!jwt)
            console.log('REQUEST URL:', `${apiBase}${url}`)

            return $fetch<T>(`${apiBase}${url}`, {
                ...options,
                headers: {
                    ...options.headers,
                    ...(jwt
                        ? { Authorization: `Bearer ${jwt}` }
                        : {}),
                },
            })
        }

        try {
            console.log('--- FIRST REQUEST ---')

            const result = await makeRequest(
                token.value ?? undefined
            )

            console.log('--- FIRST REQUEST SUCCESS ---')
            console.log(result)

            return result

        } catch (err: any) {

            console.log('--- REQUEST ERROR ---')

            const status = err?.response?.status || err?.status

            console.log('STATUS:', status)
            console.log('ERROR:', err)

            if (status === 401) {

                console.log('--- TOKEN EXPIRED ---')
                console.log('STARTING REFRESH...')

                const newToken = await refreshAccessToken()

                console.log('REFRESH RESULT:', !!newToken)

                if (!newToken) {
                    console.log('REFRESH FAILED → LOGOUT')

                    logout()
                    throw err
                }

                console.log('--- RETRYING REQUEST ---')

                const result = await makeRequest(newToken)

                console.log('--- RETRY SUCCESS ---')

                return result
            }

            throw err
        }
    }

    return { apiFetch }
}
