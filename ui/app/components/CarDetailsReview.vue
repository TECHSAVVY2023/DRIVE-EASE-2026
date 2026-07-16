<template>

    <div class="bg-[#1B1B1B] font-[poppins] p-6 rounded-xl w-full">
        <div class="flex justify-between items-center mb-5">
            <h2 class="text-white font-extrabold text-lg">Customer reviews</h2>

            <button v-if="isLoggedIn"
                class="bg-[#C1121F] hover:bg-[#9B0E18] transition-colors duration-200 text-white text-xs px-4 py-2 rounded-lg flex items-center gap-2"
                @click="reviewModalOpen = true"
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

        </div>
    
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
                      @click="setRating(star)"
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
                  <option value="oldest">Oldest</option>
                  <option value="highest">Highest Likes</option>
                  <option value="lowest">Lowest Likes</option>
              </select>

          </div>

        <ReviewCards
            v-for="(review, i) in reviews"
            :key="i"
            :review="review"
            :car-id="carId"
            class="mb-4"
        />

        <!-- Empty state -->
        <EmptyState
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
import type { Review } from '~/utils/api/api'

const props = defineProps<{
    carId: string
    isLoggedIn: boolean 
}>()

const emit = defineEmits<{
    (e: "submit"): void
}>()

const reviewModalOpen = ref(false)


const selectedRating = ref<number>(0)

const setRating = (star: number) => {
    selectedRating.value = star
}

const reviews = ref<Review[]>([])
const myReview = ref<Review | null>(null)

const totalReviews = ref(0)
const avgRating = ref(0)
const ratingBreakdown = ref<Record<number, number>>({})

const nextPage = ref<string | null>(null)
const previousPage = ref<string | null>(null)
const sortBy = ref<'newest' | 'oldest' | 'highest' | 'lowest'>('highest')

const loading = ref(false)

const { fetchCarReviews } = useReviews()

// load initial reviews
onMounted(() => {
    fetchReviews(1)
})

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

const loadMore = async () => {
    if (!nextPage.value || loading.value) return

    const url = new URL(nextPage.value)
    const page = Number(url.searchParams.get("page"))
    console.log("page", page);

    fetchReviews(page)
}

const fetchReviews = async (page: number) => {
    loading.value = true

    try {
        console.log("before fetchAllReviews")

        const res = await fetchCarReviews(props.carId, {
            page: page,
            rating: selectedRating.value,
            sort: sortBy.value
        })

        console.log("after fetchAllReviews", res)

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

watch([selectedRating, sortBy], () => {
    reviews.value = []
    nextPage.value = null
    previousPage.value = null

    fetchReviews(1)
})

</script>