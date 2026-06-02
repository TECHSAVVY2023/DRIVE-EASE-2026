<template>
    <MobileDrawer
      :menu-open="menuOpen"
      @close-menu="closeMenu"
   />
   
   <Navbar
      :menu-open="menuOpen"
      @toggle-menu="toggleMenu"
      @open-sidebar="handleOpenSidebar" 
      @close-sidebar="handleCloseSidebar"
   />

    <div class="min-h-screen bg-[#0D0D0D] font-[poppins]">

        <Banner 
            subtitle="View transactions"
            title="My Transactions"
            :breadcrumbs="[
                { label: 'Home', to: '/' },
                { label: 'Transactions' }
            ]"
        />

        <div class="max-w-2xl mx-auto px-4 py-8 flex flex-col gap-5">

            <!-- Stat Cards -->
            <div class="grid grid-cols-3 gap-3">
                <div
                v-for="stat in stats"
                :key="stat.label"
                class="bg-[#1a1a1a] border-t-6 border-[#C1121F] rounded-xl p-4 flex flex-col gap-1"
                >
                <span class="text-gray-400 text-xs">{{ stat.label }}</span>
                <span class="text-white text-2xl font-extrabold">{{ stat.value }}</span>
                </div>
            </div>

            <!-- Transactions Table Card -->
            <div class="bg-[#1a1a1a] border border-[#222] rounded-xl overflow-hidden flex flex-col gap-4">

                <!-- Header -->
                <div class="px-5 pt-5">
                <h2 class="text-white font-extrabold text-base">All transactions</h2>
                </div>

                <!-- Filters + Sort -->
                <div class="px-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <!-- Tabs -->
                <div class="flex flex-wrap gap-2">
                    <button
                    v-for="tab in tabs"
                    :key="tab"
                    @click="activeTab = tab; currentPage = 1"
                    class="text-xs px-3 py-1.5 rounded-full border transition-colors duration-200 font-medium"
                    :class="activeTab === tab
                        ? 'bg-[#C1121F] border-[#C1121F] text-white'
                        : 'border-[#2a2a2a] text-gray-400 hover:border-white hover:text-white'"
                    >
                    {{ tab }}
                    </button>
                </div>

                <!-- Sort -->
                <div class="relative">
                    <select
                    v-model="sortBy"
                    class="bg-[#111] border border-[#2a2a2a] text-white text-xs px-4 py-2 pr-8 rounded-lg appearance-none focus:outline-none focus:border-[#C1121F] cursor-pointer transition-colors duration-200"
                    >
                    <option value="newest">Newest first</option>
                    <option value="oldest">Oldest first</option>
                    <option value="highest">Highest amount</option>
                    <option value="lowest">Lowest amount</option>
                    </select>
                    <svg class="w-4 h-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                </div>
                </div>

                <!-- Table -->
                <div class="overflow-x-auto">
                <table class="w-full text-sm">
                    <thead>
                    <tr class="border-b border-[#222]">
                        <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">Vehicle</th>
                        <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">Transaction</th>
                        <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">Amount</th>
                        <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">Method</th>
                        <th class="text-left text-gray-500 text-xs font-medium px-5 py-3">Status</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-if="paginatedTransactions.length === 0">
                        <td colspan="5" class="text-center text-gray-500 text-sm py-12">
                        No transactions found.
                        </td>
                    </tr>
                    <tr
                        v-for="(txn, i) in paginatedTransactions"
                        :key="i"
                        class="border-b border-[#1f1f1f] hover:bg-[#222] transition-colors duration-150"
                    >
                        <!-- Vehicle -->
                        <td class="px-5 py-4">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-8 bg-[#111] rounded-lg overflow-hidden flex-shrink-0">
                            <img :src="txn.vehicleImage" :alt="txn.vehicleName" class="w-full h-full object-cover" @error="(e) => (e.target as HTMLImageElement).style.display = 'none'" />
                            </div>
                            <span class="text-white text-xs font-medium whitespace-nowrap">{{ txn.vehicleName }}</span>
                        </div>
                        </td>

                        <!-- Transaction -->
                        <td class="px-5 py-4">
                        <p class="text-gray-400 text-xs">{{ txn.date }}</p>
                        <p class="text-gray-500 text-[10px] font-mono mt-0.5">{{ txn.txnId }}</p>
                        </td>

                        <!-- Amount -->
                        <td class="px-5 py-4 text-white text-xs font-semibold">{{ txn.amount }}</td>

                        <!-- Method -->
                        <td class="px-5 py-4 text-gray-300 text-xs">{{ txn.method }}</td>

                        <!-- Status -->
                        <td class="px-5 py-4">
                        <span
                            class="text-xs font-semibold px-2.5 py-1 rounded-full"
                            :class="statusClass(txn.status)"
                        >
                            {{ txn.status }}
                        </span>
                        </td>
                    </tr>
                    </tbody>
                </table>
                </div>

                <!-- Pagination -->
                <div class="flex items-center justify-center gap-2 px-5 pb-5">
                <button
                    @click="currentPage--"
                    :disabled="currentPage === 1"
                    class="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs border border-[#2a2a2a] text-gray-400 hover:border-white hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors duration-200"
                >
                    <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
                    Previous
                </button>

                <template v-for="p in totalPages" :key="p">
                    <button
                    @click="currentPage = p"
                    class="w-8 h-8 rounded-lg text-xs font-semibold transition-colors duration-200"
                    :class="currentPage === p ? 'bg-[#C1121F] text-white' : 'border border-[#2a2a2a] text-gray-400 hover:border-white hover:text-white'"
                    >
                    {{ p }}
                    </button>
                </template>

                <button
                    @click="currentPage++"
                    :disabled="currentPage === totalPages"
                    class="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs border border-[#2a2a2a] text-gray-400 hover:border-white hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors duration-200"
                >
                    Next
                    <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                </button>
                </div>

            </div>

        </div>

    </div>

    <Footer />

</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const route = useRoute()
const { setAuth } = useAuth()

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

if (route.query.token) {
    await setAuth(route.query.token as string)
}

type TabType = 'All' | 'Paid' | 'Pending' | 'Refunded'
type StatusType = 'Done' | 'Pending' | 'Refunded' | 'Failed'

interface Stat {
    label: string
    value: string | number
}

interface Transaction {
    vehicleName: string
    vehicleImage: string
    date: string
    txnId: string
    amount: string
    method: string
    status: StatusType
}

const activeTab = ref<TabType>('All')
const sortBy = ref<string>('newest')
const currentPage = ref<number>(1)
const perPage = 5

const tabs: TabType[] = ['All', 'Paid', 'Pending', 'Refunded']

const transactions: Transaction[] = [
    { vehicleName: 'Toyota Wigo', vehicleImage: '', date: 'May 20, 2025', txnId: '#TXN-20250520-001', amount: '₱800', method: 'Gcash', status: 'Done' },
    { vehicleName: 'Toyota Vios', vehicleImage: '', date: 'April 15, 2025', txnId: '#TXN-20250415-002', amount: '₱1,800', method: 'Cash', status: 'Done' },
    { vehicleName: 'Toyota Innova', vehicleImage: '', date: 'March 10, 2025', txnId: '#TXN-20250310-003', amount: '₱2,500', method: 'Maya', status: 'Pending' },
    { vehicleName: 'Toyota Fortuner', vehicleImage: '', date: 'February 5, 2025', txnId: '#TXN-20250205-004', amount: '₱3,500', method: 'Gcash', status: 'Refunded' },
    { vehicleName: 'Toyota Camry', vehicleImage: '', date: 'January 22, 2025', txnId: '#TXN-20250122-005', amount: '₱4,000', method: 'Cash', status: 'Done' },
    { vehicleName: 'Toyota Rush', vehicleImage: '', date: 'January 10, 2025', txnId: '#TXN-20250110-006', amount: '₱2,200', method: 'Maya', status: 'Failed' },
    { vehicleName: 'Toyota Hiace', vehicleImage: '', date: 'December 1, 2024', txnId: '#TXN-20241201-007', amount: '₱4,700', method: 'Gcash', status: 'Done' },
]

const stats: Stat[] = [
    { label: 'Total spent', value: 20 },
    { label: 'Last transaction', value: 20 },
    { label: 'Total transactions', value: transactions.length },
]

function statusClass(status: StatusType): string {
    const map: Record<StatusType, string> = {
        Done: 'bg-green-500/10 text-green-400',
        Pending: 'bg-yellow-500/10 text-yellow-400',
        Refunded: 'bg-blue-500/10 text-blue-400',
        Failed: 'bg-red-500/10 text-red-400',
    }
    return map[status] ?? ''
}

const filteredTransactions = computed<Transaction[]>(() => {
    let result = [...transactions]

    if (activeTab.value === 'Paid') result = result.filter(t => t.status === 'Done')
    if (activeTab.value === 'Pending') result = result.filter(t => t.status === 'Pending')
    if (activeTab.value === 'Refunded') result = result.filter(t => t.status === 'Refunded')

    if (sortBy.value === 'oldest') result.reverse()
    if (sortBy.value === 'highest') result.sort((a, b) => parseInt(b.amount.replace(/\D/g, '')) - parseInt(a.amount.replace(/\D/g, '')))
    if (sortBy.value === 'lowest') result.sort((a, b) => parseInt(a.amount.replace(/\D/g, '')) - parseInt(b.amount.replace(/\D/g, '')))

    return result   
})

const totalPages = computed<number>(() => Math.max(1, Math.ceil(filteredTransactions.value.length / perPage)))

const paginatedTransactions = computed<Transaction[]>(() => {
    const start = (currentPage.value - 1) * perPage
    return filteredTransactions.value.slice(start, start + perPage)
})
</script>