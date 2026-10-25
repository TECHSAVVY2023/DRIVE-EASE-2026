const protectedClientPaths = [
    '/client/notifications',
    '/client/profile',
    '/client/transaction',
]

export default defineNuxtRouteMiddleware(async (to) => {
    if (import.meta.server) return

    const needsAuthentication = to.path.startsWith('/admin/')
        || protectedClientPaths.some(path => to.path.startsWith(path))

    if (!needsAuthentication) return

    const { init, isLoggedIn } = useAuth()
    await init()

    if (!isLoggedIn.value) {
        return navigateTo({
            path: '/client/login',
            query: { redirect: to.fullPath },
        })
    }
})
