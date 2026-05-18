import { ref } from 'vue'

export const useAdminDashboard = () => {
    const sidebarOpen = ref<boolean>(false)

    const handleCloseSidebar = (): void => {
        sidebarOpen.value = false
    }

    const handleOpenSidebar = (): void => {
        sidebarOpen.value = true
    }

    type FleetItem = {
        label: string
        value: number
        max: number
    }

    const fleet = ref<FleetItem[]>([
        { label: 'Economy', value: 8, max: 10 },
        { label: 'Economy', value: 6, max: 10 },
        { label: 'Economy', value: 9, max: 10 },
        { label: 'Economy', value: 5, max: 10 },
    ])

    return {
        sidebarOpen,
        handleCloseSidebar,
        handleOpenSidebar,
        fleet,
    }
}