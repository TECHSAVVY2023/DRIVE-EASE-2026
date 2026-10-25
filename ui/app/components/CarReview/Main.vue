<template>
    <!-- Header -->
    <div class="bg-[#1B1B1B] font-[poppins] p-6 rounded-xl w-full">
        <div class="flex justify-between items-center mb-5">
            <h2 class="text-white font-extrabold text-lg">Customer reviews</h2>

            <CarReviewWriteButton 
                :is-logged-in="isLoggedIn" 
                @click="OpenWriteReviewModal = true" 
            />

            <CarReviewWriteReviewModal 
                v-model="OpenWriteReviewModal" 
                @submit="handleReviewSubmit"
                :review-state="reviewState"
            />

        </div>
        
        <CarReviewRetingSummary 
            :avg-rating="avgRating"
            :total-reviews="totalReviews"
            :formatted-rating-breakdown="formattedRatingBreakdown"
        />

        <CarReviewFilterSort
            :selected-rating="selectedRating"
            :sort-by="sortBy"
            @update:selected-rating="selectedRating = $event"
            @update:sortBy="sortBy = $event"
        />

        <CarReviewCards
            v-if="myReview"
            :review="myReview"
            :car-id="carId"
            class="mb-4"
            @click="OpenEditReviewModal = true" 
        />

        <CarReviewWriteReviewModal 
            v-model="OpenEditReviewModal" 
            :my-review="myReview"
            @submit="handleReviewSubmit"
            :review-state="reviewState"
        />        

        <CarReviewCards
            v-for="(review, i) in reviews"
            :key="i"
            :review="review"
            :car-id="carId"
            class="mb-4"
        />

        <!-- Empty state -->
        <CommonEmptyState
            v-if="reviews.length === 0 && !myReview"
            message="No reviews match the selected filters."
            button-text="Reset filters"
            @action="
                selectedRating = 0;
                sortBy = 'highest';
            "
        />

        <!-- View more -->
        <div class="flex flex-col items-center gap-2 mt-6">

            <button
                v-if="nextPage"
                @click="loadMore"
                class="flex items-center gap-2 bg-[#C1121F] hover:bg-[#9B0E18] text-white text-sm font-semibold px-8 py-3 rounded-lg transition-colors duration-200"
            >
                View more
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
            </button>

            <span class="text-[#929292] text-xs">{{ displayedReviews }} out of {{ totalReviews }} reviews</span>
        </div>

    </div>
</template>

<script setup lang="ts">

const loading = ref(false)
const OpenWriteReviewModal = ref(false)
const OpenEditReviewModal = ref(false)

const { $swal } = useNuxtApp()
const { isLoggedIn } = useAuth()
const { fetchCarReviews } = useReviews()
const { apiFetch } = useApiFetch()

const props = defineProps<{
    carId: string
    isLoggedIn: boolean 
}>()

const { formattedRatingBreakdown, displayedReviews, totalReviews, 
        avgRating, reviews, myReview, nextPage, previousPage, sortBy, setRating,
        selectedRating, ratingBreakdown } = useCarReview()

const reviewState = useWriteReview()

const fetchReviews = async (page: number) => {
    loading.value = true

    try {
        const res = await fetchCarReviews(props.carId, {
            page: page,
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

        myReview.value = res.my_review
        totalReviews.value = res.total_reviews

        avgRating.value = res.avg_rating
        ratingBreakdown.value = res.rating_breakdown

    } finally {
        loading.value = false
    }
}

const loadMore = async () => {
    if (!nextPage.value || loading.value) return

    const url = new URL(nextPage.value)
    const page = Number(url.searchParams.get("page"))
    console.log("page", page);

    fetchReviews(page)
}

const handleReviewSubmit = async () => {
    if(OpenEditReviewModal.value){

        const removedImages = reviewState.originalImages.value.filter(
            (url) => !reviewState.existingImages.value.includes(url)
        )

       for (const file of reviewState.uploadedImages.value) {
            if (!(await reviewState.validateFile(file))) {
                return
            }
        }

        $swal.fire({
            title: 'Saving changes...',
            text: 'Please wait.',
            background: '#1a1a1a',
            color: '#ffffff',
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => {
                $swal.showLoading()
            }
        })

        try {

        const newImagesUrls = await reviewState.uploadFiles()

        const imageUrls: string[] = [
            ...reviewState.existingImages.value,
            ...newImagesUrls
        ]

        const body: any = {
            rating: reviewState.form.rating,
            review: reviewState.form.review,
            images: imageUrls
        }

        if (removedImages.length > 0) {
            body.deleted_images = removedImages
        }

        $swal.close()

        const res = await apiFetch<{ message: string }>(`/reviews/cars/${props.carId}/edit/${myReview.value?.id}/`, {
            method: 'PATCH',
            body
        })

        await nextTick()
        await new Promise(resolve => requestAnimationFrame(resolve))

        await $swal.fire({
            icon: 'success',
            title: 'Success',
            text: 'Review updated successfully.',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
            allowOutsideClick: false,
            allowEscapeKey: false,
            scrollbarPadding: false
        })
        
        OpenEditReviewModal.value = false
        } catch (err) {
            $swal.close()

            await $swal.fire({
                icon: "error",
                title: "Update failed",
                text: "Something went wrong while updating your review."
            })

            throw err
        }

        window.location.reload()
    } else {
        console.log("Add review");
        await $swal.fire({
            icon: 'success',
            title: 'Success',
            text: 'Review added successfully.',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
            allowOutsideClick: false,
            allowEscapeKey: false,
            scrollbarPadding: false
        })

        OpenWriteReviewModal.value = false
    }
}

onMounted(() => {
    fetchReviews(1)
})

watch([selectedRating, sortBy], () => {
    reviews.value = []
    nextPage.value = null
    previousPage.value = null

    fetchReviews(1)
})
</script>
