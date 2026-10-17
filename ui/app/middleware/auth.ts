export default defineNuxtRouteMiddleware((to) => {
    if (import.meta.server) return

    // Allow OAuth callback
    if (to.query.token) return

    const { isLoggedIn } = useAuth()

    if (!isLoggedIn.value) {
        return navigateTo('/login')
    }
})