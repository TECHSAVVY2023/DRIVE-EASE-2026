import type { Transaction } from '~/utils/api/api'

const loading = ref(false)

const transactions = ref<Transaction[]>([])

const count = ref(0)

const nextPage = ref<string | null>(null)
const previousPage = ref<string | null>(null)

const currentPage = ref(1)

export function useTransactionsList() {
    const { fetchTransactionsList } = useTransactions()

    const activeTab = ref("all")
    const sortBy = ref("newest")

    const pageSize = 9

    const totalPages = computed(() =>
        Math.max(1, Math.ceil(count.value / pageSize))
    )

    const tabs = [
        { label: "All", value: "all" },
        { label: "Pending", value: "pending_approval" },
        { label: "Completed", value: "completed" },
        { label: "Cancelled", value: "cancelled" },
    ]

    const sortOptions = [
        { label: "Newest first", value: "newest" },
        { label: "Oldest first", value: "oldest" },
        { label: "Highest amount", value: "highest" },
        { label: "Lowest amount", value: "lowest" },
    ]

    const fetchTransactions = async () => {
        loading.value = true

        try {
            const res = await fetchTransactionsList({
                page: currentPage.value,
                status: activeTab.value,
                sort: sortBy.value,
            })

            console.log("Transactions:", res.results)

            transactions.value = res.results

            count.value = res.count

            nextPage.value = res.next ?? null
            previousPage.value = res.previous ?? null

        } finally {
            loading.value = false
        }
    }

    // Fetch when page, status, or sort changes
    watch(
        [currentPage, activeTab, sortBy],
        () => {
            fetchTransactions()
        },
        { immediate: true }
    )

    // Reset pagination when changing filters/sort
    watch(
        [activeTab, sortBy],
        () => {
            if (currentPage.value !== 1) {
                currentPage.value = 1
            }
        }
    )

    return {
        loading,

        transactions,
        count,

        nextPage,
        previousPage,

        currentPage,
        totalPages,

        activeTab,
        sortBy,

        tabs,
        sortOptions,

        fetchTransactions,
    }
}