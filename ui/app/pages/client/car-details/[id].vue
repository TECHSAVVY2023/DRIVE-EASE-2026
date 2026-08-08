<template>
    <ClientBookingModal
        v-model="showBookingModal"
        :car="car"
        :user="user"
    />

    <MobileDrawer
        :menu-open="menuOpen"
        @close-menu="closeMenu"
    />
    
    <Navbar
        :user="user"
        :isLoggedIn="isLoggedIn"
        :menu-open="menuOpen"
        @toggle-menu="toggleMenu"
        @open-sidebar="handleOpenSidebar" 
        @close-sidebar="handleCloseSidebar"
    />

    <div class="min-h-screen w-full bg-[#121212] font-[poppins]">

        <Banner 
            subtitle="More info about the car"
            title="Car Details"
            :breadcrumbs="[
                { label: 'Home', to: '/' },
                { label: 'Fleet', to: '/client/fleet' },
                { label: 'Car Details' }
            ]"
        />

        <div class="flex justify-center items-center">
            <div v-if="car" class="max-w-5xl w-full h-fit flex justify-center items-center flex-col gap-6 px-4 py-8">

                <CarDetails 
                    :car="car"
                    :avg-rating="avgRating"
                    :total-reviews="totalReviews"
                    @book="openBooking"
                    @reserve="showBookingModal = true"
                />
        
                <OwnerNote
                    :note="car.note" 
                />

                <!-- Header -->
                <div class="bg-[#1B1B1B] font-[poppins] p-6 rounded-xl w-full">
                    <div class="flex justify-between items-center mb-5">

                        <h2 class="text-white font-extrabold text-lg">Customer reviews</h2>

                        <CarReviewWriteButton 
                            v-if="!myReview"
                            :is-logged-in="isLoggedIn" 
                            @click="OpenWriteReviewModal = true" 
                        />

                        <ClientReviewsWrite
                            v-model="OpenWriteReviewModal"
                            mode="create" 
                            @submit="handleReviewSubmit"
                            :review-state="reviewState"
                        />

                    </div>

                    <ClientReviewsSummary
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

                    <ClientReviewsCards
                        v-if="myReview"
                        :review="myReview"
                        :car-id="carId"
                        class="mb-4"
                        @click="OpenEditReviewModal = true" 
                        @delete="reviewState.deleteReview(Number(myReview.id), carId)"
                    />

                    <ClientReviewsWrite 
                        v-model="OpenEditReviewModal"
                        mode="edit" 
                        :my-review="myReview"
                        @submit="handleReviewSubmit"
                        :review-state="reviewState"
                    />        

                    <ClientReviewsCards
                        v-for="(review, i) in reviews"
                        :key="i"
                        :review="review"
                        :car-id="carId"
                        class="mb-4"
                    />

                    <!-- Empty state -->
                    <ClientCommonEmptyState
                        v-if="reviews.length === 0 && !myReview"
                        message="No reviews match the selected filters."
                        button-text="Reset filters"
                        @action="
                            selectedRating = 0;
                            sortBy = 'highest';
                        "
                    />

                    <ClientCommonViewMoreButton
                        :nextPage="nextPage || ''"
                        :displayed-reviews="displayedReviews"
                        :total-reviews="totalReviews"
                        @load-more="loadMore"
                    />
                </div>

                <SimilarCars />
            
            </div>

        </div>
        
    </div>

    <Footer />
    
</template>

<script setup lang="ts">
import { ref } from 'vue'

const route = useRoute()
const router = useRouter()

const { isLoggedIn } = useAuth()
const { apiFetch } = useApiFetch()

const loading = ref(false)
const OpenWriteReviewModal = ref(false)
const OpenEditReviewModal = ref(false)

const { $swal } = useNuxtApp()
const { fetchCarReviews } = useReviews()

const user = ref<any>(null)

const carId = route.params.id as string

const { formattedRatingBreakdown, displayedReviews, totalReviews, 
        avgRating, reviews, myReview, nextPage, previousPage, sortBy, setRating,
        selectedRating, ratingBreakdown, fetchReviews, loadMore } = useCarReview({ carId })

const { car, getCar } = useCarDetail()

const reviewState = useWriteReview({ carId })

const hasUserReviewed = computed(() => {
    if (!isLoggedIn.value || !user.value) return false

    return reviews.value.some(
        review => review.user.id === user.value.id
    )
})

const openBooking = async () => {
    if (!user.value) {
        const result = await $swal.fire({
            icon: 'warning',
            title: 'Login Required',
            text: 'You need to log in before booking a vehicle.',
            showCancelButton: true,
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
            confirmButtonText: 'Login',
        })

        if (result.isConfirmed) {
            router.push('/client/login')
        }

        return
    }

    showBookingModal.value = true
}

const handleReviewSubmit = async () => {
    if(OpenEditReviewModal.value){

        const removedImages = reviewState.originalImages.value.filter(
            (url) => reviewState.existingImages.value.includes(url)
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

        console.log('new images urls:', newImagesUrls)

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

        const res = await apiFetch<{ message: string }>(`/reviews/cars/${carId}/edit/${myReview.value?.id}/`, {
            method: 'PATCH',
            body
        })

        $swal.close()

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

        if (reviewState.uploadedImages.value.length > 0) {
            for (const file of reviewState.uploadedImages.value) {
                if (!(await reviewState.validateFile(file))) {
                    return
                }
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

        const ImagesUrls = await reviewState.uploadFiles()

        console.log('Imageurls:', ImagesUrls)

        let body: any = {}
        
        if (ImagesUrls.length > 0) {
            console.log('there is an image')
            body = {
                rating: reviewState.form.rating,
                review: reviewState.form.review,
                images: ImagesUrls
            }
        } else {
            console.log('there is no image')
            body = {
                rating: reviewState.form.rating,
                review: reviewState.form.review
            }
        }

        console.log(body)

        const res = await apiFetch<{ message: string }>(`/reviews/cars/${carId}/create/`, {
            method: 'POST',
            body
        })

        $swal.close()

        await nextTick()
        await new Promise(resolve => requestAnimationFrame(resolve))

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

        window.location.reload()
    }
}

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

const showBookingModal = ref(false)

watch(isLoggedIn, async (val) => {
    if (val) {
        user.value = await apiFetch('/auth/me/')
    } else {
        user.value = null
    }
}, { immediate: true })

onMounted(async () => {
    const id = String(route.params.id)
    await getCar(id)
    await fetchReviews(1)

    if (route.query.payment === 'success') {
        $swal.fire({
        icon: 'success',
        title: 'Payment Successful',
        text: 'Your booking has been submitted successfully.',
        confirmButtonColor: '#C1121F',
        background: '#1a1a1a',
        color: '#ffffff'
        })

        // Remove the query parameter
        navigateTo(`/client/car-details/${route.params.id}`, {
            replace: true
        })
    }

    if (route.query.payment === 'cancelled') {
        await $swal.fire({
        icon: 'info',
        title: 'Payment Cancelled',
        text: 'Your payment was cancelled. No charges were made.',
        confirmButtonColor: '#C1121F',
        background: '#1a1a1a',
        color: '#ffffff'
        })

        router.replace({
            path: route.path,
            query: {}
        })
    }
})

watch([selectedRating, sortBy], () => {
    reviews.value = []
    nextPage.value = null
    previousPage.value = null

    fetchReviews(1)
})
</script>