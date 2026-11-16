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

    const { init, isLoggedIn, authFailureReason } = useAuth()
    await init()

    if (!isLoggedIn.value) {
        return navigateTo({
            path: '/client/login',
            query: {
                redirect: to.fullPath,
                ...(authFailureReason.value
                    ? { error: authFailureReason.value }
                    : {}),
            },
        })
    }

    if (to.path.startsWith('/admin/')) {
        try {
            const { fetchUser } = useCurrentUser()
            const currentUser = await fetchUser()

            if (!currentUser || currentUser.role === 'Customer') {
                return navigateTo('/')
            }
        } catch {
            return navigateTo('/client/login')
        }
    }
})
