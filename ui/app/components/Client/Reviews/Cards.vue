<template>
    <div
        class="border rounded-xl p-5 flex flex-col gap-4"
        :class="
            review.is_mine
                ? 'border-[#C1121F] bg-[#212121]'
                : 'border-[#222] bg-[#1a1a1a]'
        "
    >
        <div v-if="review.is_mine" class="flex items-center justify-between gap-4">

            <div class="text-white bg-[#c1121f] px-7 py-1 rounded-4xl h-fit flex items-center">
                <p class="text-sm">Your review</p>
            </div>

            <div class="flex gap-2">
                <button
                    @click="$emit('click')"
                    class="cursor-pointer flex items-center gap-2 border border-[#929292] text-[#929292] hover:bg-[#2B2B2B] hover:text-white px-4 py-2 rounded-lg transition-colors"
                >
                    <!-- Edit Icon -->
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="w-4 h-4"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M16.862 3.487a2.1 2.1 0 113.03 2.91L8.5 17.79l-4 1 1-4L16.862 3.487z"
                        />
                    </svg>

                    <span class="text-sm font-semibold">Edit</span>
                </button>

                <button
                    @click="$emit('delete')"
                    class="cursor-pointer flex items-center gap-2 border hover:bg-[#2E1618] border-[#C1121F] text-[#C1121F] hover:text-[#D92331] px-4 rounded-lg transition-colors"
                >
                    <!-- Trash Icon -->
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="w-4 h-4"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5-3h4m-7 3h10M10 11v6m4-6v6"
                        />
                    </svg>

                    <span class="text-sm font-semibold">Delete</span>
                </button>
            </div>
        </div>

        <!-- Header -->
        <div class="flex items-start justify-between gap-4">

            <div class="flex items-center gap-3">

                <div class="w-10 h-10 rounded-full bg-[#C1121F] flex-shrink-0 overflow-hidden flex items-center justify-center">
                    
                    <img
                        v-if="review.user.profile_picture"
                        :src="review.user.profile_picture"
                        :alt="review.user.first_name + ' ' + review.user.last_name"
                        class="w-full h-full object-cover"
                    />

                    <svg v-else class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                    </svg>

                </div>

                <div>
                    <p class="text-white text-sm font-semibold"> {{ review.user.first_name }} {{ review.user.last_name }} </p>
                    <p class="text-[#929292] text-xs"> {{ formatDate(review.created_at) }} </p>
                </div>

            </div>

            <!-- Stars -->
            <div class="flex gap-0.5 flex-shrink-0">
                
                <svg
                    v-for="s in 5"
                    :key="s"
                    class="w-4 h-4"
                    :class="s <= review.rating ? 'text-[#C1121F]' : 'text-[#333]'"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                </svg>

            </div>

        </div>

        <!-- Review text -->
        <p class="text-white text-sm leading-relaxed">
            {{ review.text }}
        </p>

        <!-- Images -->
        <div
            v-if="review.images && review.images.length"
            class="flex gap-2 flex-wrap"
        >
            <div
                v-for="(img, j) in review.images"
                :key="j"
                class="w-16 h-12 rounded-lg bg-[#111] border border-[#2a2a2a] overflow-hidden flex-shrink-0"
            >
                <img
                :src="img"
                :alt="'Review image ' + (Number(j) + 1)"
                class="w-full h-full object-cover"
                />
            </div>
        </div>

        <!-- Helpful -->
        <div class="flex justify-end">

            <button
                 @click="toggleHelpful(review)"
                class="flex items-center gap-1.5 text-xs transition-colors duration-200"
                :class="
                review.helpful
                    ? 'text-[#C1121F]'
                    : 'text-gray-400 hover:text-[#C1121F]'
                "
            >

                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5"
                />
                </svg>

                Helpful ({{ review.helpful_count }})

            </button>

        </div>

    </div>
</template>

<script setup lang="ts">
import type { Review } from '~/utils/api/api'

const { apiFetch } = useApiFetch()

defineProps<{
    review: any
    carId?: string | null
    myReview?: Review | null
}>()

defineEmits<{
    click: []
    delete: []
}>()

const formatDate = (date: string) =>
    new Date(date).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
    })

type HelpfulResponse = {
    helpful: boolean
    helpful_count: number
}

async function toggleHelpful(review: any) {
    try {
        const res = await apiFetch<HelpfulResponse>(
            `/reviews/${review.id}/helpful/`,
            {
                method: "POST"
            }
        )

        review.helpful = res.helpful
        review.helpful_count = res.helpful_count

    } catch (error) {
        console.error("Failed to toggle helpful:", error)
    }
}

</script>