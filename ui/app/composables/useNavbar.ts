export const useNavbar = () => {
    const menuOpen = ref(false)

    const toggleMenu = () => {
        menuOpen.value = !menuOpen.value
    }

    const closeMenu = () => {
        menuOpen.value = false
    }

    const sidebarOpen = ref<boolean>(false)

    const handleCloseSidebar = (): void => {
        sidebarOpen.value = false
    }

    const handleOpenSidebar = (): void => {
        sidebarOpen.value = true
    }

    const route = useRoute()
    const { setAuth } = useAuth()

    if (route.query.token) {
        setAuth(route.query.token as string)
    }

    return {
        menuOpen,
        toggleMenu,
        closeMenu,
        sidebarOpen,
        handleCloseSidebar,
        handleOpenSidebar
    }
}