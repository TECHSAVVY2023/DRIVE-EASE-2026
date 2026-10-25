const removeLegacyOAuthTokensFromUrl = () => {
    const url = new URL(window.location.href)

    if (!url.searchParams.has('access')
        && !url.searchParams.has('refresh')
        && !url.hash.startsWith('#access=')) return

    url.searchParams.delete('access')
    url.searchParams.delete('refresh')
    url.hash = ''

    window.history.replaceState(window.history.state, '', url.toString())
}

export default defineNuxtPlugin(async () => {
    const { init } = useAuth()

    removeLegacyOAuthTokensFromUrl()
    await init()
})
