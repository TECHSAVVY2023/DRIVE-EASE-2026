<template>
    <Teleport to="body">
        <Transition
            enter-active-class="transition duration-150"
            leave-active-class="transition duration-100"
            enter-from-class="opacity-0"
            leave-to-class="opacity-0"
        >
            <div
                v-if="open"
                class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 p-4"
                @click.self="close"
            >

                <div 
                    class="
                        bg-[#111111] border-t-[#C1121F] border-t-5 rounded-xl 
                        w-full h-[90%] max-w-md font-[poppins] flex flex-col
                    "
                    @click.stop
                    role="dialog"
                    aria-modal="true"
                >

                    <!-- Header -->
                    <div class="flex items-center justify-between p-6 border-b border-[#2A2A2A]">
                        <div>
                            <h2 class="text-white font-extrabold text-lg">Write a review</h2>
                            <p class="text-[#929292] text-xs mt-0.5">Share your experience with this vehicle.</p>
                        </div>

                        <button 
                            @click="close" 
                            class="text-white/40 hover:text-white transition-colors"
                        >
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    <!-- Rating -->
                    <div class="flex flex-col justify-center items-center py-5 border-b border-[#2A2A2A]">

                        <div class="flex gap-2">
                            <button
                                v-for="star in 5"
                                :key="star"
                                @click="form.rating = star"
                                @mouseenter="hoverRating = star"
                                @mouseleave="hoverRating = 0"
                                class="transition-transform duration-150 hover:scale-110"
                            >

                                <svg 
                                    class="w-8 h-8 transition-colors duration-150" 
                                    :class="
                                        star <= (hoverRating || form.rating)
                                            ? 'text-[#C1121F]'
                                            : 'text-[#333]'
                                    "
                                    fill="currentColor" 
                                    viewBox="0 0 24 24"
                                >
                                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                                </svg>

                            </button>
                        </div>

                        <label class="block text-xs text-[#929292] mt-4"> Click or tap to leave a rating </label>  

                    </div>

                    <!-- Body -->
                    <div class="p-6 overflow-y-auto">

                        <!-- Review -->
                        <div class="mb-6">
                            <label class="block text-sm font-medium text-[#929292] mb-2"> Your review </label>

                            <textarea
                                v-model="form.text"
                                rows="6"
                                placeholder="Tell others about your experience..."
                                class="
                                    w-full rounded-lg
                                    px-4 py-3 text-white resize-none
                                    placeholder:text-sm bg-[#0f0f0f] border border-[#2a2a2a]"
                            />

                        </div>

                        <ClientReviewsWriteImageUploader
                            v-model:images="form.images"
                        />

                    </div>

                    <!-- Footer -->
                    <div class="flex flex-col gap-2 my-4 mx-6">
                        <button
                            class="w-full bg-[#C1121F] hover:bg-red-700 text-white text-sm font-bold py-3 rounded-lg transition-colors duration-200"
                            @click="save"
                        >
                            Submit Review
                        </button>

                        <button
                            class="w-full border border-[#2a2a2a] hover:border-white text-white text-sm font-semibold py-3 rounded-lg transition-colors duration-200"
                            @click="close"
                        >
                            Cancel
                        </button>
                    </div>

                </div>
            </div>

        </Transition>
    </Teleport>
</template>

<script setup lang="ts">
import type { Review } from '~/utils/api/api'

const emit = defineEmits<{
    submit: [review: Review]
}>()

const open = defineModel<boolean>({ required: true })

const form = ref<Review>(blank())

const hoverRating = ref(0)

function blank(): Review {
    return {
        id: 0,
        car: '',
        user: {
            id: 0,
            first_name: '',
            last_name: '',
            profile_picture: null,
        },
        rating: 0,
        text: '',
        created_at: '',
        status: 'pending',
        images: [],
        helpful_count: 0,
    }
}

function save() {
    const review = toRaw(form.value)

    emit('submit', {
        ...review,
        images: review.images.map(image => ({ ...image })),
    })
}

function close() {
    open.value = false
}

watch(
    () => open.value,
    (open) => {
        if (!import.meta.client) return

        document.documentElement.style.overflow =
            open ? 'hidden' : ''
    },
    { immediate: true }
)

const fieldClass = 'w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3.5 py-2.5 text-[13px] text-[#e4e4e4] outline-none transition-colors placeholder:text-neutral-600 hover:border-[#3a3a3a] focus:border-[#C1121F]'
</script>
