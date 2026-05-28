export const useReviewsPage = () => {
    const { reviews } = useReviews()

    const visibleCount = ref<number>(3)

    const selectedRating = ref<number>(0)

    const sortBy = ref<'newest' | 'highest' | 'lowest'>('newest')

    const filteredReviews = computed(() => {
        let filtered = [...reviews.value]

        if (selectedRating.value !== 0) {
            filtered = filtered.filter(
                review => review.rating === selectedRating.value
            )
        }

        if (sortBy.value === 'newest') {
            filtered.sort(
                (a, b) =>
                    new Date(b.date).getTime() -
                    new Date(a.date).getTime()
            )
        }

        if (sortBy.value === 'highest') {
            filtered.sort((a, b) => b.rating - a.rating)
        }

        if (sortBy.value === 'lowest') {
            filtered.sort((a, b) => a.rating - b.rating)
        }

        return filtered
    })

    const visibleReviews = computed(() =>
        filteredReviews.value.slice(0, visibleCount.value)
    )
    
    return {
        visibleCount,
        selectedRating,
        sortBy,
        filteredReviews,
        visibleReviews
    }
}