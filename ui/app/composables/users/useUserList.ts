import type { User } from '~/utils/api/api'

const loading = ref(false)

const users = ref<User[]>([])

const count = ref(0)

const nextPage = ref<string | null>(null)
const previousPage = ref<string | null>(null)

const currentPage = ref(1)

const pageSize = 5

// Selected filters
const search = ref("")
const selectedStatus = ref("")
const selectedRole = ref("")

const totalUsers = ref(0)
const activeUsers = ref(0)
const suspendedUsers = ref(0)

export function useUsersList() {
    const { fetchUsersList, fetchUsersStats } = useUsers()

    const totalPages = computed(() =>
        Math.ceil(count.value / pageSize)
    )

    const fetchUsers = async () => {
        loading.value = true

        try {
            const res = await fetchUsersList({
                page: currentPage.value,
                search: search.value,
                status: selectedStatus.value,
                role: selectedRole.value,
            })

            users.value = res.results

            console.log('later users:', users.value)

            count.value = res.count

            nextPage.value = res.next ?? null
            previousPage.value = res.previous ?? null

        } finally {
            loading.value = false
        }
    }

    const fetchStats = async () => {
        const stats = await fetchUsersStats()

        totalUsers.value = stats.total
        activeUsers.value = stats.active
        suspendedUsers.value = stats.suspended
    }

    // Fetch whenever pagination, search, or filters change
    watch(
        [
            currentPage,
            search,
            selectedStatus,
            selectedRole,
        ],
        () => {
            fetchUsers()
        }
    )

    // Reset pagination when filters change
    watch(
        [
            search,
            selectedStatus,
            selectedRole,
        ],
        () => {
            currentPage.value = 1
        }
    )

    const resetFilters = () => {
        search.value = ""
        selectedStatus.value = ""
        selectedRole.value = ""
    }

    return {
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

        totalUsers,
        activeUsers,
        suspendedUsers,
        fetchStats,
    }
}