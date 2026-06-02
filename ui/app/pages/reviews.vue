<template>
    <MobileDrawer
        :menu-open="menuOpen"
        @close-menu="closeMenu"
    />

    <Navbar
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
            
                <!-- Rating Summary -->
                <div class="bg-[#1a1a1a] border border-[#222] rounded-xl p-5 mb-5">
                    <div class="flex flex-col sm:flex-row gap-6 items-center sm:items-start">
                
                        <!-- Overall Score -->
                        <div class="flex flex-col items-center flex-shrink-0">
                        <span class="text-white text-5xl font-extrabold">{{ overallRating }}</span>
                        <div class="flex gap-0.5 mt-2">
                            <svg v-for="i in 5" :key="i" class="w-5 h-5" :class="i <= Math.round(Number(overallRating)) ? 'text-[#C1121F]' : 'text-[#333]'" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                            </svg>
                        </div>
                        <span class="text-[#929292] text-xs mt-1">{{ reviews.length }} reviews</span>
                        </div>
                
                        <!-- Bar Breakdown -->
                        <div class="flex flex-col gap-2 flex-1 w-full">
                        <div v-for="bar in ratingBreakdown" :key="bar.star" class="flex items-center gap-3">
                            <span class="text-[#929292] text-xs w-4 flex-shrink-0 text-right">{{ bar.star }}</span>
                            <svg class="w-3 h-3 text-[#C1121F] flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                            </svg>
                            <div class="flex-1 h-1.5 bg-[#2a2a2a] rounded-full overflow-hidden">
                            <div
                                class="h-full bg-[#C1121F] rounded-full"
                                :style="{ width: bar.percent + '%' }"
                            ></div>
                            </div>
                            <span class="text-[#929292] text-xs w-10 text-right flex-shrink-0">{{ bar.percent }}%</span>
                        </div>
                        </div>
                
                    </div>
                </div>

                <!-- Filter + Sort Section -->
                <div class="flex flex-col lg:flex-row gap-4 justify-between mb-5">

                    <!-- Rating Filters -->
                    <div class="flex flex-wrap gap-2">
                    <button
                        @click="selectedRating = 0"
                        class="px-4 py-2 rounded-lg border text-sm font-medium transition-colors duration-200"
                        :class="
                            selectedRating === 0
                            ? 'bg-[#C1121F] border-[#C1121F] text-white'
                            : 'bg-[#1a1a1a] border-[#222] text-[#929292] hover:border-[#C1121F]'
                        "
                    >
                        All
                    </button>

                    <button
                        v-for="star in [5,4,3,2,1]"
                        :key="star"
                        @click="selectedRating = star"
                        class="flex items-center gap-1 px-4 py-2 rounded-lg border text-sm font-medium transition-colors duration-200"
                        :class="
                            selectedRating === star
                            ? 'bg-[#C1121F] border-[#C1121F] text-white'
                            : 'bg-[#1a1a1a] border-[#222] text-[#929292] hover:border-[#C1121F]'
                        "
                    >
                        {{ star }}
                        <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                        </svg>
                    </button>
                    </div>

                    <!-- Sort -->
                    <select
                        v-model="sortBy"
                        class="bg-[#1a1a1a] border border-[#222] text-white text-sm rounded-lg px-4 py-2 outline-none hover:border-[#C1121F] transition-colors duration-200"
                        >
                        <option value="newest">Newest</option>
                        <option value="highest">Highest rating</option>
                        <option value="lowest">Lowest rating</option>
                    </select>

                </div>

                <!-- Empty state -->
                <EmptyState
                    v-if="filteredReviews.length === 0"
                    message="No reviews match the selected filters."
                    button-text="Reset filters"
                    @action="
                        selectedRating = 0;
                        sortBy = 'newest';
                    "
                />

                <ReviewCards
                    v-for="(review, i) in visibleReviews"
                    :key="i"
                    :review="review"
                    class="mb-4"
                />
            
                <!-- View more -->
                <div class="flex flex-col items-center gap-2 mt-6">
                    <button
                        v-if="visibleCount < filteredReviews.length"
                        @click="visibleCount += 3"
                        class="flex items-center gap-2 bg-[#C1121F] hover:bg-[#6B0A10] text-white text-sm font-semibold px-8 py-3 rounded-lg transition-colors duration-200"
                    >
                        View more
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                        </svg>
                    </button>
                    <span class="text-[#929292] text-xs">{{ visibleReviews.length }} out of {{ filteredReviews.length }} reviews</span>
                </div>
            
            </div>
        </div>

    </div>

    <Footer />
</template>

<script setup lang="ts">

import { watch } from 'vue'

const { 
    menuOpen,
    toggleMenu,
    closeMenu,
    handleCloseSidebar,
    handleOpenSidebar
 } = useNavbar()

const { reviews } = useReviews()
 
const { filteredReviews, selectedRating, sortBy, visibleCount, visibleReviews} = useReviewsPage()

const overallRating = computed(() => {
    if (!reviews.value.length) return 0

    const sum = reviews.value.reduce((acc, r) => acc + r.rating, 0)
    return (sum / reviews.value.length).toFixed(1)
})

const ratingBreakdown = computed(() => {
    const total = reviews.value.length

    return [5,4,3,2,1].map(star => {
        const count = reviews.value.filter(r => r.rating === star).length

        return {
            star,
            percent: total ? (count / total) * 100 : 0
        }
    })
})


watch([selectedRating, sortBy], () => {
    visibleCount.value = 3
})

</script>
