export default defineNuxtRouteMiddleware((to) => {
  // Only run on client — localStorage is not available on server
  if (import.meta.server) return

  // Allow access when the Django OAuth callback just redirected here
  // with a token in the URL — onMounted in dashboard will save it
  if (to.query.token) return

  const token = localStorage.getItem('auth_token')
    if (!token) {
      return navigateTo('/login')
    }
})
