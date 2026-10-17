import { ref, watch } from 'vue'

export function useCurrentUser() {
    const { isLoggedIn } = useAuth()
    const { apiFetch } = useApiFetch()

    const user = ref<any>(null)

    watch(
        isLoggedIn,
        async (val) => {
            if (val) {
                user.value = await apiFetch('/auth/me/')
            } else {
                user.value = null
            }
        },
        { immediate: true }
    )

    return {
        user,
    }
}