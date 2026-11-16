<template>

    <AdminUsersAddUserModal
        v-model="addUserModalOpen"
        :can-manage-roles="isSuperAdmin"
        @save="handleCreateUser"
    />

    <AdminUsersEditUserModal
        v-model="editModalOpen"
        :user="selectedEditUser"
        :can-manage-roles="isSuperAdmin"
        @save="handleEditUser"
    />

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

                    <button
                        type="button"
                        class="rounded-lg bg-[#c81e2c] px-5 py-[11px] text-sm font-bold text-white hover:bg-[#b31a27]"
                        @click="addUserModalOpen = true"
                    >
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
                    :can-manage-staff="isSuperAdmin"
                    @update:search="search = $event"
                    @update:page="currentPage = $event"
                    @update:selected-role="selectedRole = $event"
                    @update:selected-status="selectedStatus = $event"
                    @edit="handleEdit"
                    @secondary-action="handleSecondaryAction"
                    @delete="handleDelete"
                />

            </main>

    </div>

    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { AdminCreateUserFormPayload, AdminEditUserPayload, User } from '~/utils/types/accounts'

const { isLoggedIn } = useAuth()
const { user } = useCurrentUser()
const isSuperAdmin = computed(() => user.value?.role === 'Super Admin')

const sidebarOpen = ref<boolean>(false)

const handleCloseSidebar = (): void => {
    sidebarOpen.value = false
}

const handleOpenSidebar = (): void => {
    sidebarOpen.value = true
}

const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
})

const { loading, users, count, nextPage, previousPage, currentPage,
        pageSize, search, selectedStatus, selectedRole, fetchUsers, totalPages,
        resetFilters, fetchStats, totalUsers, activeUsers, suspendedUsers,
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

const addUserModalOpen = ref(false)
const editModalOpen = ref(false)
const selectedEditUser = ref<User | null>(null)

const handleEdit = (account: User) => {
    selectedEditUser.value = account
    editModalOpen.value = true
}

const {
    handleCreateUser: createUser,
    handleDeleteUser: deleteUser,
    handleEditUser: editUser,
    handleUpdateUserStatus: updateUserStatus,
} = useUserAdminEdit()

const refreshUsers = async () => {
    await Promise.all([fetchUsers(true), fetchStats()])
}

const handleSecondaryAction = async (account: User) => {
    const result = await updateUserStatus(
        account.user_reference,
        account.status !== 'Active',
    )
    if (result.success) await refreshUsers()
}

const handleDelete = async (account: User) => {
    const userLabel = `${account.given_name} ${account.family_name}`.trim() || account.email
    const result = await deleteUser(account.user_reference, userLabel)
    if (result.success) await refreshUsers()
}

const handleCreateUser = async ({
    body,
    idFiles,
}: {
    body: AdminCreateUserFormPayload
    idFiles: File[]
}) => {
    const result = await createUser(body, idFiles)

    if (!result.success) return

    addUserModalOpen.value = false

    await Promise.all([
        fetchUsers(true),
        fetchStats(),
    ])
}

const handleEditUser = async ({userReference, body}: { userReference: string, body: AdminEditUserPayload }) => {
    const result = await editUser(userReference, body)

    if (!result.success) return

    editModalOpen.value = false
    selectedEditUser.value = null

    await Promise.all([
        fetchUsers(true),
        fetchStats(),
    ])
}

watch(editModalOpen, isOpen => {
    if (!isOpen) selectedEditUser.value = null
})

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
