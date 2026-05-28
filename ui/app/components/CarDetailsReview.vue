<template>
    <div class="bg-[#1B1B1B] font-[poppins] p-6 rounded-xl">
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
                    <span class="text-[#929292] text-xs w-10 text-right flex-shrink-0">{{ bar.percent.toFixed(0) }}%</span>
                </div>
                </div>
        
            </div>
        </div>

        <ReviewCards
            v-for="(review, i) in filteredReviews"
            :key="i"
            :review="review"
            :car-id="carId"
            class="mb-4"
        />

        <!-- View more -->
        <div class="flex flex-col items-center gap-2 mt-6">
            <button
                v-if="filteredReviews.length > 4 && visibleCount < filteredReviews.length"
                @click="visibleCount += 3"
                class="flex items-center gap-2 bg-[#C1121F] hover:bg-[#6B0A10] text-white text-sm font-semibold px-8 py-3 rounded-lg transition-colors duration-200"
            >
                View more
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
            </button>
            <span class="text-[#929292] text-xs">{{ filteredReviews.length }} out of {{ reviews.filter(review => review.car_id === props.carId).length }} reviews</span>
        </div>
    
    </div>
</template>
 
<script setup lang="ts">

const { reviews } = useReviews()

const props = defineProps<{
    carId?: number
}>()
 
const visibleCount = ref<number>(3)
 
const filteredReviews = computed(() =>
    reviews.value.filter(
        review => review.car_id === props.carId
    )
)

const overallRating = computed(() => {
    if (!filteredReviews.value.length) return 0

    const sum = filteredReviews.value.reduce((acc, r) => acc + r.rating, 0)
    return (sum / filteredReviews.value.length).toFixed(1)
})

const ratingBreakdown = computed(() => {
    const total = filteredReviews.value.length

    const countByStar = [5,4,3,2,1].map(star => {
        const count = filteredReviews.value.filter(r => r.rating === star).length

        return {
            star,
            percent: total ? (count / total) * 100 : 0
        }
    })

    return countByStar
})

</script>