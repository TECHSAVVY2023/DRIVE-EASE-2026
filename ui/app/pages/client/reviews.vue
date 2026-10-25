<template>
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

    <div class="min-h-screen bg-[#121212] font-[poppins]">

        <Banner 
            subtitle="See what others think"
            title="Customer Reviews"
            :breadcrumbs="[
                { label: 'Home', to: '/' },
                { label: 'Reviews' }
            ]"
        />

        <div class="py-10 px-10">
            <div class="bg-[#1B1B1B] p-6 rounded-xl">
                <h2 class="text-white font-extrabold text-lg mb-5">Customer reviews</h2>

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
                    v-for="(review, i) in reviews"
                    :key="i"
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
                    :total-reviews="totalReviews"
                    @load-more="loadMore"
                />
        
            </div>
        </div>

    </div>

    <Footer />
</template>

<script setup lang="ts">
import { watch } from 'vue'

const route = useRoute()

const { isLoggedIn, authReady } = useAuth()
const { user } = useCurrentUser()

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
 } = useNavbar()

const { formattedRatingBreakdown, displayedReviews, totalReviews, 
        avgRating, reviews, myReview, nextPage, previousPage, sortBy, setRating,
        selectedRating, ratingBreakdown, fetchReviews, loadMore } = useCarReview()

const carId = route.params.id as string

onMounted(() => {
    fetchReviews(1)
})

watch([selectedRating, sortBy], () => {
    fetchReviews(1)
})

</script>
