<template>
    <div
        v-bind="$attrs"
        class="border rounded-xl p-5 flex flex-col gap-4"
        :class="
            isMyReview
                ? 'border-[#C1121F] bg-white/[0.025]'
                : 'border-white/[0.08] bg-white/[0.025]'
        "
    >
        <div v-if="isMyReview" class="flex items-center justify-between gap-4">

            <div class="text-white bg-[#c1121f] px-7 py-1 rounded-4xl h-fit flex items-center">
                <p class="text-sm">Your review</p>
            </div>

            <div class="flex gap-2">

                <!-- Edit Button -->
                <button
                    @click="$emit('edit')"
                    class="
                        cursor-pointer flex items-center gap-2 
                        border border-[#3D3D3D] text-[#929292] hover:text-white hover:border-white
                        px-3 py-2 rounded-lg transition-colors
                    "
                >
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

                    <span class="text-xs">Edit</span>
                </button>

                <!-- Delete Button -->
                <button
                    @click="$emit('delete')"
                    class="
                        cursor-pointer flex items-center gap-2 
                        border border-[#3D3D3D] text-[#929292] hover:text-[#c1121f] hover:border-[#c1121f]
                        px-4 rounded-lg transition-colors
                    "
                >
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

                    <span class="text-xs">Delete</span>
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

        <!-- Image gallery -->
        <div
            v-if="reviewImages.length"
            class="grid gap-1.5 overflow-hidden rounded-xl bg-[#111]"
            :class="reviewImages.length === 1
                ? 'w-full max-w-sm grid-cols-1'
                : 'h-44 w-full grid-cols-2 sm:h-56 sm:grid-cols-4'"
        >
            <button
                v-for="(image, index) in reviewImages"
                :key="`${image}-${index}`"
                type="button"
                class="group relative min-h-0 overflow-hidden bg-[#111] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-[#C1121F]"
                :class="galleryItemClass(index)"
                :aria-label="`View review image ${index + 1} of ${reviewImages.length}`"
                @click="openViewer(index)"
            >
                <img
                    :src="image"
                    :alt="`Review image ${index + 1}`"
                    class="transition duration-300 group-hover:scale-105 group-hover:brightness-75"
                    :class="reviewImages.length === 1
                        ? 'block h-auto w-full object-contain'
                        : 'h-full w-full object-cover'"
                    loading="lazy"
                />

                <span class="absolute inset-0 flex items-center justify-center bg-black/0 opacity-0 transition group-hover:bg-black/20 group-hover:opacity-100">
                    <svg class="h-7 w-7 text-white drop-shadow" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m15 15 6 6m-11-4a7 7 0 1 1 0-14 7 7 0 0 1 0 14Z" />
                    </svg>
                </span>
            </button>
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

    <ClientReviewsImageViewer
        v-model="viewerOpen"
        :images="reviewImages"
        :initial-index="activeImageIndex"
    />

</template>

<script setup lang="ts">
import type { Review, Review1 } from '~/utils/api/api'

defineOptions({ inheritAttrs: false })

const { apiFetch } = useApiFetch()

const props = defineProps<{
    review: any
    carId?: string | null
    myReview?: Review1 | null
    isMyReview?: boolean
}>()

const emit = defineEmits<{
    (e: 'edit'): void
    (e: 'delete'): void
}>()

const viewerOpen = ref(false)
const activeImageIndex = ref(0)

const reviewImages = computed<string[]>(() =>
    (props.review.images || [])
        .map((image: string | { url?: string }) =>
            typeof image === 'string' ? image : image.url
        )
        .filter((image: string | undefined): image is string => Boolean(image))
        .slice(0, 5)
)

const galleryItemClass = (index: number) => {
    const count = reviewImages.value.length

    if (count === 1) return ''
    if (count === 2) return 'sm:col-span-2'
    if (count === 3 && index === 0) return 'row-span-2 sm:col-span-2'
    if (count >= 4 && index === 0) return 'row-span-2 sm:col-span-2'
    if (count === 4 && index === 3) return 'col-span-2'

    return ''
}

const openViewer = (index: number) => {
    activeImageIndex.value = index
    viewerOpen.value = true
}

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
