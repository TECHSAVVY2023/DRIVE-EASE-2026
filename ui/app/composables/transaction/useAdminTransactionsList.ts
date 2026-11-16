import type { Transaction } from '~/utils/types/booking'

const loading = ref(false)
const error = ref<string | null>(null)

const bookings = ref<Transaction[]>([])

const count = ref(0)

const nextPage = ref<string | null>(null)
const previousPage = ref<string | null>(null)

const currentPage = ref(1)

const total_booking = ref(0)
const pending_approval = ref(0)
const active_rentals = ref(0)
const completed = ref(0)
const cancelled = ref(0)


export function useAdminTransactionsList() {
    const { fetchAdminBookingsList, fetchBookingStats } = useAdminTransactions()

    const search = ref("")
    const selectedStatus = ref("")
    const selectedRentalPeriod = ref("")

    // Keep this aligned with Django's TransactionPagination.page_size.
    const pageSize = 5

    const totalPages = computed(() =>
        Math.max(1, Math.ceil(count.value / pageSize))
    )

    const fetchBookings = async () => {
        loading.value = true
        error.value = null

        try {
            const res = await fetchAdminBookingsList({
                page: currentPage.value,
                search: search.value,
                status: selectedStatus.value,
                rental_period: selectedRentalPeriod.value,
            })

            bookings.value = res.results
            count.value = res.count

            nextPage.value = res.next ?? null
            previousPage.value = res.previous ?? null

        } catch (fetchError: unknown) {
            error.value = fetchError instanceof Error
                ? fetchError.message
                : 'Unable to load bookings.'
        } finally {
            loading.value = false
        }
    }

    const fetchStats = async () => {
        const stats = await fetchBookingStats()

        total_booking.value = stats.total
        pending_approval.value = stats.pending_approval
        active_rentals.value = stats.active_rentals
        completed.value = stats.completed
        cancelled.value = stats.cancelled
    }

    // Fetch when page or filters change
    watch(
        [
            currentPage,
            search,
            selectedStatus,
            selectedRentalPeriod
        ],
        () => {
            fetchBookings()
        }
    )

    onMounted(() => {
        fetchBookings()
    })


    // Reset pagination when filters/search change
    watch(
        [
            search,
            selectedStatus,
            selectedRentalPeriod
        ],
        () => {
            if (currentPage.value !== 1) {
                currentPage.value = 1
            }
        }
    )

    return {
        loading,

        bookings,
        count,

        nextPage,
        previousPage,

        currentPage,
        pageSize,
        totalPages,

        search,
        selectedStatus,
        selectedRentalPeriod,

        fetchBookings,
        fetchStats,

        total_booking,
        pending_approval,
        active_rentals,
        completed,
        cancelled,
    }
}
