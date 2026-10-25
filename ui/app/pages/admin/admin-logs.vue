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

                <section class="overflow-hidden rounded-xl border border-[#232323] bg-[#161616]">
                    <div class="grid gap-3 border-b border-[#252525] p-4 md:grid-cols-[minmax(220px,1fr)_180px_180px]">
                        <label class="relative">
                            <span class="sr-only">Search activity logs</span>
                            <svg class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[#666]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <circle cx="11" cy="11" r="7" /><path stroke-linecap="round" d="m20 20-3.5-3.5" />
                            </svg>
                            <input v-model="search" type="search" placeholder="Search user, action, or details..." class="h-10 w-full rounded-lg border border-[#2b2b2b] bg-[#0f0f0f] pl-10 pr-3 text-sm text-white outline-none placeholder:text-[#5f5f5f] focus:border-[#C1121F]" />
                        </label>

                        <select v-model="selectedAction" class="h-10 rounded-lg border border-[#2b2b2b] bg-[#0f0f0f] px-3 text-sm text-gray-300 outline-none focus:border-[#C1121F]">
                            <option value="all">All actions</option>
                            <option value="create">Created</option>
                            <option value="update">Updated</option>
                            <option value="delete">Deleted</option>
                            <option value="login">Authentication</option>
                        </select>

                        <select v-model="selectedPeriod" class="h-10 rounded-lg border border-[#2b2b2b] bg-[#0f0f0f] px-3 text-sm text-gray-300 outline-none focus:border-[#C1121F]">
                            <option value="all">All time</option>
                            <option value="today">Today</option>
                            <option value="week">Last 7 days</option>
                            <option value="month">Last 30 days</option>
                        </select>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="w-full min-w-[850px]">
                            <thead class="border-b border-[#252525] bg-[#121212] text-left text-[10px] uppercase tracking-[0.12em] text-[#707070]">
                                <tr>
                                    <th class="px-5 py-3 font-semibold">Administrator</th>
                                    <th class="px-5 py-3 font-semibold">Action</th>
                                    <th class="px-5 py-3 font-semibold">Description</th>
                                    <th class="px-5 py-3 font-semibold">IP address</th>
                                    <th class="px-5 py-3 font-semibold">Date & time</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="log in paginatedLogs" :key="log.id" class="border-b border-[#222] last:border-0 hover:bg-white/[0.02]">
                                    <td class="px-5 py-4">
                                        <div class="flex items-center gap-3">
                                            <div class="flex h-9 w-9 items-center justify-center rounded-full bg-[#C1121F] text-xs font-bold">{{ initials(log.actor) }}</div>
                                            <div><p class="text-sm font-semibold">{{ log.actor }}</p><p class="text-[11px] text-[#707070]">{{ log.role }}</p></div>
                                        </div>
                                    </td>
                                    <td class="px-5 py-4"><span class="rounded-full border px-2.5 py-1 text-[10px] font-semibold" :class="actionStyle[log.action]">{{ actionLabel[log.action] }}</span></td>
                                    <td class="max-w-sm px-5 py-4 text-xs leading-5 text-[#b0b0b0]">{{ log.description }}</td>
                                    <td class="px-5 py-4 font-mono text-xs text-[#858585]">{{ log.ipAddress }}</td>
                                    <td class="px-5 py-4"><p class="text-xs text-gray-300">{{ formatDate(log.createdAt) }}</p><p class="mt-1 text-[10px] text-[#666]">{{ formatTime(log.createdAt) }}</p></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div v-if="!filteredLogs.length" class="px-6 py-16 text-center text-sm text-[#777]">No activity logs match your filters.</div>

                    <div class="flex flex-col gap-3 border-t border-[#252525] px-5 py-4 text-xs text-[#777] sm:flex-row sm:items-center sm:justify-between">
                        <span>Showing {{ showingFrom }}–{{ showingTo }} of {{ filteredLogs.length }} logs</span>
                        <div class="flex gap-2">
                            <button type="button" :disabled="page === 1" class="rounded-lg border border-[#303030] px-3 py-2 text-gray-300 disabled:cursor-not-allowed disabled:opacity-40" @click="page--">Previous</button>
                            <button type="button" :disabled="page === totalPages" class="rounded-lg border border-[#303030] px-3 py-2 text-gray-300 disabled:cursor-not-allowed disabled:opacity-40" @click="page++">Next</button>
                        </div>
                    </div>
                </section>
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
const search = ref('')
const selectedAction = ref<LogAction | 'all'>('all')
const selectedPeriod = ref<'all' | 'today' | 'week' | 'month'>('all')
const page = ref(1)
const pageSize = 6

// Replace this array with the result of an activity-log API request later.
const logs = ref<ActivityLog[]>([
    { id: 1, actor: 'Alex Rivera', role: 'Administrator', action: 'update', description: 'Updated booking BKG-71A2 to confirmed.', ipAddress: '192.168.1.24', createdAt: new Date().toISOString() },
    { id: 2, actor: 'Mia Santos', role: 'Administrator', action: 'create', description: 'Added Toyota Vios 2025 to the fleet.', ipAddress: '192.168.1.18', createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString() },
    { id: 3, actor: 'Alex Rivera', role: 'Administrator', action: 'login', description: 'Signed in to the admin portal.', ipAddress: '192.168.1.24', createdAt: new Date(Date.now() - 26 * 60 * 60 * 1000).toISOString() },
    { id: 4, actor: 'Mia Santos', role: 'Administrator', action: 'delete', description: 'Deleted a rejected customer review.', ipAddress: '192.168.1.18', createdAt: new Date(Date.now() - 3 * 86400000).toISOString() },
    { id: 5, actor: 'Alex Rivera', role: 'Administrator', action: 'update', description: 'Changed Ford Raptor availability to maintenance.', ipAddress: '192.168.1.24', createdAt: new Date(Date.now() - 5 * 86400000).toISOString() },
    { id: 6, actor: 'Jamie Cruz', role: 'Support staff', action: 'update', description: 'Approved a five-star customer review.', ipAddress: '192.168.1.31', createdAt: new Date(Date.now() - 9 * 86400000).toISOString() },
    { id: 7, actor: 'Mia Santos', role: 'Administrator', action: 'create', description: 'Created a manual booking for a walk-in customer.', ipAddress: '192.168.1.18', createdAt: new Date(Date.now() - 18 * 86400000).toISOString() },
])

const actionLabel: Record<LogAction, string> = { create: 'Created', update: 'Updated', delete: 'Deleted', login: 'Login' }
const actionStyle: Record<LogAction, string> = {
    create: 'border-emerald-500/20 bg-emerald-500/10 text-emerald-400',
    update: 'border-blue-500/20 bg-blue-500/10 text-blue-400',
    delete: 'border-red-500/20 bg-red-500/10 text-red-400',
    login: 'border-violet-500/20 bg-violet-500/10 text-violet-400',
}

const filteredLogs = computed(() => {
    const query = search.value.trim().toLowerCase()
    const periodDays = { today: 1, week: 7, month: 30 } as const

    return logs.value.filter(log => {
        if (selectedAction.value !== 'all' && log.action !== selectedAction.value) return false
        if (selectedPeriod.value !== 'all' && Date.now() - new Date(log.createdAt).getTime() > periodDays[selectedPeriod.value] * 86400000) return false
        return !query || `${log.actor} ${log.description} ${log.ipAddress}`.toLowerCase().includes(query)
    })
})
const totalPages = computed(() => Math.max(1, Math.ceil(filteredLogs.value.length / pageSize)))
const paginatedLogs = computed(() => filteredLogs.value.slice((page.value - 1) * pageSize, page.value * pageSize))
const showingFrom = computed(() => filteredLogs.value.length ? (page.value - 1) * pageSize + 1 : 0)
const showingTo = computed(() => Math.min(page.value * pageSize, filteredLogs.value.length))
const statCards = computed(() => [
    { label: 'Total activities', value: logs.value.length, icon: '<svg viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h10"/></svg>' },
    { label: 'Changes today', value: logs.value.filter(log => Date.now() - new Date(log.createdAt).getTime() < 86400000).length, icon: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>' },
    { label: 'Administrators', value: new Set(logs.value.map(log => log.actor)).size, icon: '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0116 0"/></svg>' },
])

const initials = (name: string) => name.split(' ').map(part => part[0]).join('').slice(0, 2).toUpperCase()
const formatDate = (value: string) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
const formatTime = (value: string) => new Date(value).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })
const handleOpenSidebar = () => { sidebarOpen.value = true }
const handleCloseSidebar = () => { sidebarOpen.value = false }

watch([search, selectedAction, selectedPeriod], () => { page.value = 1 })
watch(totalPages, value => { if (page.value > value) page.value = value })
onMounted(() => document.documentElement.classList.add('admin-page'))
onBeforeUnmount(() => document.documentElement.classList.remove('admin-page'))
</script>
