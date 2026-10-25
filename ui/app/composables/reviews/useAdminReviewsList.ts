import type { AdminReview, AdminReviewsResponse, AdminReviewStats } from '~/utils/api/api'

const loading = ref(false)

const reviews = ref<AdminReview[]>([])

const count = ref(0)
const stats = ref<AdminReviewStats>({
    total: 0,
    average_rating: 0,
    pending: 0,
    approved: 0,
})

const nextPage = ref<string | null>(null)
const previousPage = ref<string | null>(null)

const currentPage = ref(1)

export function useAdminReviewsList() {
    const { fetchAdminReviews } = useAdminReview()

    const search = ref('')
    const selectedStatus = ref('all')
    const selectedRating = ref('all')

    const pageSize = 5

    const totalPages = computed(() =>
        Math.ceil(count.value / pageSize)
    )

    const fetchReviews = async (force = false) => {
        loading.value = true

        try {
            const res: AdminReviewsResponse = await fetchAdminReviews({
                page: currentPage.value,
                search: search.value,
                status: selectedStatus.value,
                rating: selectedRating.value === 'all'
                    ? undefined
                    : Number(selectedRating.value),
                force,
            })

            reviews.value = res.results
            count.value = res.count
            stats.value = res.stats

            nextPage.value = res.next ?? null
            previousPage.value = res.previous ?? null
        } finally {
            loading.value = false
        }
    }

    // Fetch when page, search, or filters change
    watch(
        [
            currentPage,
            search,
            selectedStatus,
            selectedRating,
        ],
        () => {
            fetchReviews()
        },
        { immediate: true }
    )

    // Reset pagination when search or filters change
    watch(
        [
            search,
            selectedStatus,
            selectedRating,
        ],
        () => {
            if (currentPage.value !== 1) {
                currentPage.value = 1
            }
        }
    )

    return {
        loading,

        reviews,
        count,
        stats,

        nextPage,
        previousPage,

        currentPage,
        pageSize,
        totalPages,

        search,
        selectedStatus,
        selectedRating,

        fetchReviews,
    }
}
