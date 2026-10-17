<template>
    <div class="flex h-screen bg-[#0D0D0D] font-[poppins] overflow-hidden text-white">

        <!-- Sidebar -->
        <AdminCommonSidebarNav
            :sidebarOpen="sidebarOpen" 
            @close-sidebar="sidebarOpen = false" 
        />

        <div class="flex-1 flex flex-col overflow-hidden">

            <AdminCommonTopbarNav
                :user="user"
                @open-sidebar="handleOpenSidebar"
                @close-sidebar="handleCloseSidebar"
                title="Users"
                :isLoggedIn="isLoggedIn"
                :subtitle="currentDate"
            />

            <!-- Main -->
            <main class="flex-1 overflow-y-auto px-8 py-8">
                <div class="flex justify-between items-end mb-[22px]">
                    <div>
                        <h2 class="text-[22px] font-extrabold">Users</h2>
                        <div class="text-[#8a8a8a] text-[13px] mt-1">Manage customer and staff accounts</div>
                    </div>
                    <button class="bg-[#c81e2c] hover:bg-[#b31a27] text-white font-bold text-sm px-5 py-[11px] rounded-lg">
                        + Add user
                    </button>
                </div>

                <!-- Stat cards -->
                <AdminCommonStatsCards :cards="statCards"/>

                <!-- Table card -->
                <AdminUsersTable
                    :users="users"
                    :search="search"
                    :current-page="currentPage"
                    :count="count"
                    :page-size="pageSize"
                    :total-pages="totalPages"
                    :next-page="nextPage"
                    :previous-page="previousPage"
                    :selected-role="selectedRole"
                    :selected-status="selectedStatus"
                    @update:search="search = $event"
                    @update:page="currentPage = $event"
                    @update:selected-role="selectedRole = $event"
                    @update:selected-status="selectedStatus = $event"
                    @edit="handleEdit"
                    @secondary-action="handleSecondaryAction"
                />

            </main>

    </div>

    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { User } from '~/utils/api/api'

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

const sidebarOpen = ref<boolean>(false)

const handleCloseSidebar = (): void => {
    sidebarOpen.value = false
}

const handleOpenSidebar = (): void => {
    sidebarOpen.value = true
}

const handleAddUser = () => {
    // Open add-user modal
}

const handleEdit = (user: User) => {
    // Open edit-user modal
    console.log('Edit user:', user)
}

const handleSecondaryAction = (user: User) => {
    if (user.status === 'Active') {
        console.log('Suspend user:', user)
    } else {
        console.log('Activate user:', user)
    }
}

const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
})

const { 
        loading,
        users,
        count,
        nextPage,
        previousPage,
        currentPage,
        pageSize,

        search,
        selectedStatus,
        selectedRole,

        fetchUsers,
        totalPages,
        resetFilters,

        fetchStats,
        totalUsers,
        activeUsers,
        suspendedUsers,
} = useUsersList()

const statCards = computed(() => [
    {
        label: 'Total users',
        value: totalUsers.value,
        icon: `<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.5 2.7-6 6-6s6 2.5 6 6"/><circle cx="17.5" cy="9" r="2.4"/><path d="M15.8 14.3c2.3.4 4.2 2.5 4.2 5.2"/></svg>`
    },
    {
        label: 'Active',
        value: activeUsers.value,
        icon: `<svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>`
    },
    {
        label: 'Suspended',
        value: suspendedUsers.value,
        icon: `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M6.5 6.5l11 11"/></svg>`
    }
])

console.log(totalUsers.value, activeUsers.value, suspendedUsers.value);

onMounted(async () => {
    await Promise.all([
        fetchUsers(),
        fetchStats(),
    ])
})

onMounted(() => {
    document.documentElement.classList.add('admin-page')
})

onBeforeUnmount(() => {
    document.documentElement.classList.remove('admin-page')
})

</script>