<template>
    <!-- Rating Summary -->
    <div class="bg-[#1a1a1a] border border-[#222] rounded-xl p-5 mb-5">
        <div class="flex flex-col sm:flex-row gap-6 items-center sm:items-start">
    
            <!-- Overall Score -->
            <div class="flex flex-col items-center flex-shrink-0">
            <span class="text-white text-5xl font-extrabold">{{ avgRating.toFixed(1) }}</span>
            
            <div class="flex gap-0.5 mt-2">
                <svg v-for="i in 5" :key="i" class="w-5 h-5" :class="i <= Math.round(avgRating) ? 'text-[#C1121F]' : 'text-[#333]'" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
            </div>

            <span class="text-[#929292] text-xs mt-1">{{ totalReviews }} reviews</span>
            </div>

            <!-- Bar Breakdown -->
            <div class="flex flex-col gap-2 flex-1 w-full">
                <div v-for="bar in formattedRatingBreakdown" :key="bar.star" class="flex items-center gap-3">
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
</template>

<script setup lang="ts">
defineProps<{
    avgRating: number
    totalReviews: number
    formattedRatingBreakdown: Array<{
        star: number
        percent: number
    }>
}>()
</script>