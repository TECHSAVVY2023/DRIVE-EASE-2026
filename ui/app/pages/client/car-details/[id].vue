<template>
    <ClientBookingModal
        v-model="showBookingModal"
        :car="car"
        :user="user"
        :reservation-mode="reservationMode"
    />

    <MobileDrawer
        :menu-open="menuOpen"
        @close-menu="closeMenu"
    />
    
    <Navbar
        :user="user"
        :is-logged-in="isLoggedIn"
        :auth-ready="authReady"
        :menu-open="menuOpen"
        @toggle-menu="toggleMenu"
        @open-sidebar="handleOpenSidebar" 
        @close-sidebar="handleCloseSidebar"
    />

    <div class="charcoal-blueprint-surface min-h-screen w-full font-[poppins]">

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

                <ClientReviewsCarDetails
                    :car="car"
                    :avg-rating="avgRating"
                    :total-reviews="totalReviews"
                    :availability-alert-subscribed="availabilityAlertSubscribed"
                    :availability-alert-loading="availabilityAlertLoading"
                    @book="openBooking(false)"
                    @reserve="openBooking(true)"
                    @notify-available="handleNotifyWhenAvailable"
                />

                <ClientReviewsOwnersNote
                    :note="car.note"
                />

                <!-- Header -->
                <div class="smoked-charcoal-panel font-[poppins] p-6 rounded-xl w-full">
                    <div class="flex justify-between items-center mb-5">

                        <h2 class="text-white font-extrabold text-lg">Customer reviews</h2>

                        <button v-if="isLoggedIn && !myReview"
                            class="bg-[#C1121F] hover:bg-[#9B0E18] transition-colors duration-200 text-white text-xs px-4 py-2 rounded-lg flex items-center gap-2"
                            @click="showWriteReviewModal = true"
                        >

                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                class="w-5 h-5"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                stroke-width="2"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5M16.5 3.5a2.121 2.121 0 113 3L12 14l-4 1 1-4 7.5-7.5z"
                                />
                            </svg>
                            Write a Review

                        </button>

                        <ClientReviewsWriteModal
                            v-model="showWriteReviewModal"
                            @submit="handleCreateReview"
                        />

                        <ClientReviewsEditModal
                            v-if="myReview"
                            v-model="showEditReviewModal"
                            :my-review="myReview"
                            :existing-images="existingImages"
                            @submit="handleEditReview"
                            @update:existing-images="handleExistingImagesUpdate"
                        />

                    </div>

                    <ClientReviewsSummary
                        :avg-rating="avgRating"
                        :total-reviews="totalReviews"
                        :formatted-rating-breakdown="formattedRatingBreakdown"
                    />

                    <ClientReviewsCarFilterSort 
                        :selected-rating="selectedRating"
                        :sort-by="sortBy"
                        @update:selected-rating="selectedRating = $event"
                        @update:sortBy="sortBy = $event"
                    />

                    <ClientReviewsCards
                        v-if="myReview"
                        :review="myReview"
                        :car-id="carId"
                        :is-my-review="true"
                        class="mb-4"
                        @edit="handleEdit"
                        @delete="reviewState.deleteReview(myReview.review_reference, carId)"
                    />

                    <ClientReviewsCards
                        v-for="(review, i) in reviews"
                        :key="review.id"
                        :review="review"
                        :car-id="carId"
                        class="mb-4"
                    />

                    <!-- Empty state -->
                    <ClientCommonEmptyState
                        v-if="reviews.length === 0"
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
                        :total-reviews="filteredTotalReviews"
                        @load-more="loadMore"
                    />
                </div>

                <SimilarCars :car-reference="car.car_reference" />
            
            </div>

        </div>
        
    </div>

    <Footer />
    
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Review } from '~/utils/api/api'

const route = useRoute()
const router = useRouter()

const { init, isLoggedIn, authReady } = useAuth()
const { apiFetch } = useApiFetch()
const { handleSubmitReview } = useReviewsWrite()
const {
    handleSubmitEditReview,
    existingImages,
    prepareEditReview,
    resetEditReview,
} = useReviewsEdit()

const showWriteReviewModal = ref(false)

const { $swal } = useNuxtApp()

const { user } = useCurrentUser()

const carId = computed(() => String(route.params.id))
const reviewState = useWriteReview()

const { formattedRatingBreakdown, displayedReviews, totalReviews,
        filteredTotalReviews,
        avgRating, reviews, myReview, nextPage, sortBy,
        selectedRating, fetchReviews, loadMore } = useReviewsLists()

function handleExistingImagesUpdate(images: string[]) {
    existingImages.value = images
}

const { car, getCar } = useCarDetail()
const {
    subscribed: availabilityAlertSubscribed,
    loading: availabilityAlertLoading,
    getAlertStatus,
    subscribe: subscribeToAvailability,
    reset: resetAvailabilityAlert,
} = useCarAvailabilityAlert()

const reservationMode = ref(false)

const handleNotifyWhenAvailable = async () => {
    if (!user.value) {
        const result = await $swal.fire({
            icon: 'warning',
            title: 'Login Required',
            text: 'Log in so we know where to send your availability notification.',
            showCancelButton: true,
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
            confirmButtonText: 'Login',
        })

        if (result.isConfirmed) {
            await router.push('/client/login')
        }
        return
    }

    try {
        const message = await subscribeToAvailability(carId.value)
        await $swal.fire({
            icon: 'success',
            title: 'Alert Set',
            text: message,
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
        })
    } catch (error: any) {
        await $swal.fire({
            icon: 'error',
            title: 'Could Not Set Alert',
            text: error?.data?.message ?? 'Please try again.',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
        })
    }
}

const openBooking = async (reserveInAdvance = false) => {
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

    reservationMode.value = reserveInAdvance
    showBookingModal.value = true
}

const showEditReviewModal = ref(false)

const handleEdit = () => {
    showEditReviewModal.value = true
}

async function refreshReviews() {
    reviews.value = []
    nextPage.value = null
    await fetchReviews(1, carId.value)
}

async function handleCreateReview(form: Review) {
    const result = await handleSubmitReview(form, carId.value)

    if (!result.success) return

    showWriteReviewModal.value = false
    await refreshReviews()
}

async function handleEditReview(form: Review) {
    const result = await handleSubmitEditReview(form, carId.value)

    if (!result.success) return

    showEditReviewModal.value = false
    resetEditReview()
    await refreshReviews()
}

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
} = useNavbar()

const showBookingModal = ref(false)

watch(
    [authReady, isLoggedIn],
    async ([ready, loggedIn]) => {
        if (!ready) return

        if (!loggedIn) {
            myReview.value = null
            resetAvailabilityAlert()
        } else if (car.value) {
            await getAlertStatus(carId.value)
        }
    },
    { immediate: true }
)

onMounted(async () => {
    await init()
    if (!authReady.value) return

    await getCar(carId.value)
    await fetchReviews(1, carId.value)

    if (isLoggedIn.value) {
        await getAlertStatus(carId.value)
    }

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
        const bookingReference = String(route.query.booking_reference || '')

        if (bookingReference) {
            try {
                await apiFetch('/payments/cancel-paymongo-payment/', {
                    method: 'POST',
                    body: { booking_reference: bookingReference },
                })
                await getCar(carId.value, { force: true })
            } catch (error) {
                console.error('Could not cancel the payment session.', error)
            }
        }

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

    fetchReviews(1, carId.value)
})

watch(carId, async (nextCarId, previousCarId) => {
    if (!authReady.value || nextCarId === previousCarId) return

    reviews.value = []
    myReview.value = null
    nextPage.value = null
    resetAvailabilityAlert()

    await getCar(nextCarId)
    await fetchReviews(1, nextCarId)

    if (isLoggedIn.value) {
        await getAlertStatus(nextCarId)
    }

    if (import.meta.client) {
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }
})

watch(showEditReviewModal, (isOpen) => {
    if (isOpen && myReview.value) {
        prepareEditReview(myReview.value)
    }
})
</script>
