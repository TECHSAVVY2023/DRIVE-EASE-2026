<template>
    <div class="bg-[#1a1a1a] border border-[#222] rounded-xl p-5 flex flex-col gap-4">

        <!-- Header -->
        <div class="flex items-start justify-between gap-4">

            <div class="flex items-center gap-3">

                <div class="w-10 h-10 rounded-full bg-[#C1121F] flex-shrink-0 overflow-hidden flex items-center justify-center">
                    <img
                        v-if="review.avatar"
                        :src="review.avatar"
                        :alt="review.name"
                        class="w-full h-full object-cover"
                    />

                    <span v-else class="text-white text-sm font-bold">
                        {{ review.name.charAt(0) }}
                    </span>
                </div>

                <div>
                    <p class="text-white text-sm font-semibold"> {{ review.name }} </p>
                    <p class="text-[#929292] text-xs"> {{ review.date }} </p>
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
                @click="review.helpfulClicked = !review.helpfulClicked"
                class="flex items-center gap-1.5 text-xs transition-colors duration-200"
                :class="
                review.helpfulClicked
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

                Helpful ({{ review.helpfulCount }})

            </button>

        </div>

    </div>
</template>

<script setup lang="ts">
defineProps<{
    review: any
}>()
</script>