<template>
    <div class="flex h-screen overflow-hidden bg-[#0D0D0D] font-[poppins] text-white">
        <AdminCommonSidebarNav :sidebar-open="sidebarOpen" @close-sidebar="sidebarOpen = false" />

        <div class="flex min-w-0 flex-1 flex-col overflow-hidden">
            <AdminCommonTopbarNav
                :user="user"
                :is-logged-in="isLoggedIn"
                title="Activity Logs"
                @open-sidebar="handleOpenSidebar"
                @close-sidebar="handleCloseSidebar"
            />

            <main class="flex-1 overflow-y-auto px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
                <div class="mb-6 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
                    <div>
                        <h1 class="text-[22px] font-extrabold">Activity logs</h1>
                        <p class="mt-1 text-[13px] text-[#8a8a8a]">Track important administrative actions across the system</p>
                    </div>

                    <button type="button" class="flex items-center justify-center gap-2 rounded-lg border border-[#303030] bg-[#181818] px-4 py-2.5 text-xs font-semibold text-gray-300 transition hover:border-[#C1121F] hover:text-white">
                        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v12m0 0 4-4m-4 4-4-4M5 21h14" />
                        </svg>
                        Export logs
                    </button>
                </div>

                <AdminCommonStatsCards :cards="statCards" />

                <AdminLogsTable 
                    :logs="logs"
                    :search="search"
                    :current-page="currentPage"
                    :count="count"
                    :page-size="pageSize"
                    :total-pages="totalPages"
                    :next-page="nextPage"
                    :previous-page="previousPage"
                    :selected-action="selectedAction"
                    :selected-sort="selectedSort"
                    @update:search="search = $event"
                    @update:page="currentPage = $event"
                    @update:selected-action="selectedAction = $event"
                    @update:selected-sort="selectedSort = $event"
                />

            </main>
        </div>
    </div>
</template>

<script setup lang="ts">
type LogAction = 'create' | 'update' | 'delete' | 'login'
type ActivityLog = { id: number; actor: string; role: string; action: LogAction; description: string; ipAddress: string; createdAt: string }

const { isLoggedIn } = useAuth()
const { user } = useCurrentUser()
const sidebarOpen = ref(false)

const { logs, count, nextPage, previousPage, currentPage, pageSize, totalPages,
    search, selectedAction, selectedSort } = useLogsList()

const actionLabel: Record<LogAction, string> = { create: 'Created', update: 'Updated', delete: 'Deleted', login: 'Login' }
const actionStyle: Record<LogAction, string> = {
    create: 'border-emerald-500/20 bg-emerald-500/10 text-emerald-400',
    update: 'border-blue-500/20 bg-blue-500/10 text-blue-400',
    delete: 'border-red-500/20 bg-red-500/10 text-red-400',
    login: 'border-violet-500/20 bg-violet-500/10 text-violet-400',
}

const statCards = computed(() => [
    { label: 'Total activities', value: logs.value.length, icon: '<svg viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h10"/></svg>' },
    { label: 'Changes today', value: logs.value.filter(log => Date.now() - new Date(log.created_at).getTime() < 86400000).length, icon: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>' },
    { label: 'Administrators', value: new Set(logs.value.map(log => log.admin_name)).size, icon: '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0116 0"/></svg>' },
])

const initials = (name: string) => name.split(' ').map(part => part[0]).join('').slice(0, 2).toUpperCase()
const formatDate = (value: string) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
const formatTime = (value: string) => new Date(value).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })
const handleOpenSidebar = () => { sidebarOpen.value = true }
const handleCloseSidebar = () => { sidebarOpen.value = false }

onMounted(() => document.documentElement.classList.add('admin-page'))
onBeforeUnmount(() => document.documentElement.classList.remove('admin-page'))
</script>
