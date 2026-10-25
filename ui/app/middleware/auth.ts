export default defineNuxtRouteMiddleware(async (to) => {
    if (import.meta.server) return

    const { init, isLoggedIn } = useAuth()
    await init()

    if (!isLoggedIn.value) {
        return navigateTo({
            path: '/client/login',
            query: { redirect: to.fullPath },
        })
    }
})
