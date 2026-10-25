import type { Review, Review1 } from '~/utils/api/api'

export const useReviewsLists = () => {
    const { fetchCarReviews, fetchAllReviews } = useReviews()
    const loading = ref(false)

    const totalReviews = ref(0)
    const filteredTotalReviews = ref(0)
    const avgRating = ref(0)
    const selectedRating = ref<number>(0)
    const ratingBreakdown = ref<Record<number, number>>({})

    const reviews = ref<Review[]>([])
    const myReview = ref<Review1 | null>(null)

    const nextPage = ref<string | null>(null)
    const previousPage = ref<string | null>(null)
    const activeCarId = ref<string | undefined>()
    const sortBy = ref<'newest' | 'oldest' | 'highest' | 'lowest'>('highest')

    const setRating = (star: number) => {
        selectedRating.value = star
    }
    
    const formattedRatingBreakdown = computed(() => {
        const total = totalReviews.value

        return [5, 4, 3, 2, 1].map((star) => ({
            star,
            percent: total > 0
                ? ((ratingBreakdown.value[star] ?? 0) / total) * 100
                : 0,
        }))
    })

    // The pinned user's review is rendered separately, so this counter should
    // only represent reviews loaded through the paginated results list.
    const displayedReviews = computed(() => reviews.value.length)

    const withoutMyReview = (items: Review[]) => {
        if (!myReview.value) return items

        return items.filter(
            review => String(review.id) !== String(myReview.value?.id)
        )
    }

    const fetchReviews = async (page: number, carId?: string) => {
        loading.value = true
        activeCarId.value = carId

        if (page === 1) {
            filteredTotalReviews.value = 0
        }

        try {
            if (carId) {
                const res = await fetchCarReviews(carId, {
                    page,
                    rating: selectedRating.value,
                    sort: sortBy.value
                })

                myReview.value = res.my_review

                const otherReviews = withoutMyReview(res.results)

                if (page === 1) {
                    reviews.value = otherReviews
                } else {
                    const loadedIds = new Set(reviews.value.map(review => String(review.id)))
                    reviews.value.push(
                        ...otherReviews.filter(review => !loadedIds.has(String(review.id)))
                    )
                }

                nextPage.value = res.next ?? null
                previousPage.value = res.previous ?? null
                totalReviews.value = res.total_reviews
                filteredTotalReviews.value = res.count
                avgRating.value = res.avg_rating
                ratingBreakdown.value = res.rating_breakdown
            } else {
                const res = await fetchAllReviews({
                    page,
                    rating: selectedRating.value,
                    sort: sortBy.value
                })

                if (page === 1) {
                    reviews.value = res.results
                } else {
                    reviews.value.push(...res.results)
                }

                nextPage.value = res.next ?? null
                previousPage.value = res.previous ?? null
                totalReviews.value = res.total_reviews
                filteredTotalReviews.value = res.count
                avgRating.value = res.avg_rating
                ratingBreakdown.value = res.rating_breakdown
            }
        } finally {
            loading.value = false
        }
    }
        
    const loadMore = async () => {
        if (!nextPage.value || loading.value) return

        const url = new URL(nextPage.value)
        const page1 = Number(url.searchParams.get("page"))

        await fetchReviews(page1, activeCarId.value)
    }

    return {
        formattedRatingBreakdown,
        displayedReviews,
        totalReviews,
        filteredTotalReviews,
        avgRating,
        ratingBreakdown,
        reviews,
        myReview,
        nextPage,
        previousPage,
        sortBy,
        setRating,
        selectedRating,
        fetchReviews,
        loadMore,
    }
}
