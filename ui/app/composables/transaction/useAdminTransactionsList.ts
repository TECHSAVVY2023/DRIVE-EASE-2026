import type { Transaction } from '~/utils/types/booking'

const loading = ref(false)

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
    const selectedPayment = ref("")

    const pageSize = 9

    const totalPages = computed(() =>
        Math.max(1, Math.ceil(count.value / pageSize))
    )

    const fetchBookings = async () => {
        loading.value = true

        try {
            const isOverdueFilter = selectedStatus.value === 'overdue'

            const res = await fetchAdminBookingsList({
                page: currentPage.value,
                search: search.value,
                status: isOverdueFilter ? '' : selectedStatus.value,
                payment_status: selectedPayment.value,
            })

            let results = res.results

            if (isOverdueFilter) {
                results = results.filter(booking =>
                    ['confirmed', 'picked_up'].includes(booking.status) &&
                    new Date(booking.return_date) < new Date()
                )
            }

            bookings.value = results
            count.value = isOverdueFilter
                ? results.length
                : res.count

            nextPage.value = res.next ?? null
            previousPage.value = res.previous ?? null

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
            selectedPayment
        ],
        () => {
            fetchBookings()
        },
        { immediate: true }
    )

    // Reset pagination when filters/search change
    watch(
        [
            search,
            selectedStatus,
            selectedPayment
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
        selectedPayment,

        fetchBookings,
        fetchStats,

        total_booking,
        pending_approval,
        active_rentals,
        completed,
        cancelled,
    }
}
