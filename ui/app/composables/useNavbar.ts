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

    return {
        menuOpen,
        toggleMenu,
        closeMenu,
        sidebarOpen,
        handleCloseSidebar,
        handleOpenSidebar
    }
}