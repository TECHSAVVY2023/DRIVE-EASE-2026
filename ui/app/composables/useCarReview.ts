import type { Review, ReviewForm, CarReviewsResponse } from '~/utils/api/api'

export function useWriteReview(props: { carId: string , myReview?: Review | null}) {
    const { apiFetch } = useApiFetch()
    const { $swal } = useNuxtApp()

    const form = reactive<ReviewForm>({
        rating: 0,
        review: "",
        images: [],
    })

    const hoverRating = ref(0)
    
    const uploadedImages = ref<File[]>([])
    const existingImages = ref<string[]>([])
    const originalImages = ref<string[]>([])
    const deletedImages = ref<string[]>([])

    const imageInput = ref<HTMLInputElement | null>(null)

    const OpenWriteReviewModal = ref(false)
    const OpenEditReviewModal = ref(false)

    const triggerUpload = () => {
        imageInput.value?.click()
    }

    const addFiles = (files: File[]) => {

        const remaining = 5 - uploadedImages.value.length

        uploadedImages.value.push(
            ...files
                .filter(file => file.type.startsWith("image/"))
                .slice(0, remaining)
        )
    }

    const handleImageChange = (event: Event) => {
        const input = event.target as HTMLInputElement

        if (!input.files) return

        addFiles(Array.from(input.files))

        input.value = ""
    }

    const handleDrop = (event: DragEvent) => {
        if (!event.dataTransfer) return

        addFiles(Array.from(event.dataTransfer.files))
    }

    const validateFile = async (file: File): Promise<boolean> => {
        const MAX_FILE_SIZE = 50 * 1024 * 1024
        const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']

        const extension = file.name.split('.').pop()?.toLowerCase()

        if (!extension || !ALLOWED_EXTENSIONS.includes(extension)) {
            $swal.close()
            await $swal.fire({
                icon: 'error',
                title: 'Invalid File',
                text: 'Only JPG and PNG images are allowed.',
                confirmButtonText: 'OK',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff'
            })
            return false
        }

        console.log('file size:', file.size)

        if (file.size > MAX_FILE_SIZE) {
            $swal.close()
            await $swal.fire({
                icon: 'error',
                title: 'File Too Large',
                text: 'Image size must not exceed 50 MB.',
                confirmButtonText: 'OK',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff'
            })
            return false
        }

        return true
    }

    const removeUploadedImage = (index: number) => {
        uploadedImages.value.splice(index, 1)
    }

    const removeExistingImage = (index: number, url: string) => {
        existingImages.value.splice(index, 1)
    }

    const uploadFiles = async () => {
        return await Promise.all(
            uploadedImages.value.map(async (file) => {
                const fd = new FormData()
                fd.append('file', file)

                const res = await apiFetch<{ url: string }>('/uploads/', {
                    method: 'POST',
                    body: fd
                })

                return res.url
            })
        )
    }

    const deleteReview = async (reviewId: number, carId: string) => {
        const result = await $swal.fire({
            title: 'Delete review?',
            text: 'This action cannot be undone.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
            confirmButtonText: 'Yes, delete it',
            cancelButtonText: 'Cancel',
        })

        if (!result.isConfirmed) return

        await apiFetch(`/reviews/cars/${carId}/delete/${reviewId}/`, {
            method: 'DELETE'
        })

        await $swal.fire({
            title: 'Deleted!',
            text: 'Your review has been deleted.',
            icon: 'success',
            timer: 1500,
            background: '#1a1a1a',
            color: '#ffffff',
            showConfirmButton: false,
        })

        window.location.reload()
    }

    return {
        form,
        hoverRating,
        uploadedImages,
        existingImages,
        imageInput,
        triggerUpload,
        addFiles,
        handleImageChange,
        handleDrop,
        removeUploadedImage,
        removeExistingImage,
        validateFile,
        originalImages,
        deletedImages,
        uploadFiles,
        deleteReview
    }
}

export function useCarReview(props?: { carId?: string }) {

    const { fetchCarReviews, fetchAllReviews } = useReviews()
    const loading = ref(false)

    const totalReviews = ref(0)
    const avgRating = ref(0)
    const selectedRating = ref<number>(0)
    const ratingBreakdown = ref<Record<number, number>>({})

    const reviews = ref<Review[]>([])
    const myReview = ref<Review | null>(null)

    const nextPage = ref<string | null>(null)
    const previousPage = ref<string | null>(null)
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

    const displayedReviews = computed(() => {
        return reviews.value.length + (myReview.value ? 1 : 0)
    })

    const fetchReviews = async (page: number) => {
        loading.value = true

        try {
            const res = props?.carId
                ? await fetchCarReviews(props.carId, {
                    page,
                    rating: selectedRating.value,
                    sort: sortBy.value
                })
                : await fetchAllReviews({
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
                avgRating.value = res.avg_rating
                ratingBreakdown.value = res.rating_breakdown

                if (props?.carId) {
                    myReview.value = (res as CarReviewsResponse).my_review
                }
        } finally {
            loading.value = false
        }
    }
    
    const loadMore = async () => {
        if (!nextPage.value || loading.value) return

        const url = new URL(nextPage.value)
        const page1 = Number(url.searchParams.get("page"))

        fetchReviews(page1)
    }

    return {
        formattedRatingBreakdown,
        displayedReviews,
        totalReviews,
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
