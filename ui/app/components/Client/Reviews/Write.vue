<template>
    <Transition name="fade">
        <div
            ref="modalRef"
            v-if="modelValue"
            class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 p-4"
            @click="$emit('update:modelValue', false)"
        >

            <div 
                class="
                    bg-[#111111] border-t-[#C1121F] border-t-5 rounded-xl 
                    w-full h-[90%] max-w-md font-[poppins] flex flex-col
                "
                @click.stop
            >

                <!-- Header -->
                <div class="flex items-center justify-between p-6 border-b border-[#2A2A2A]">

                    <div v-if="props.mode === 'create'">
                        <h2 class="text-white font-extrabold text-lg">Write a review</h2>
                        <p class="text-[#929292] text-xs mt-1">Share your experience with this vehicle.</p>
                    </div>

                    <div v-if="props.mode === 'edit'">
                        <h2 class="text-white font-extrabold text-lg">Edit your review</h2>
                        <p class="text-[#929292] text-xs mt-1">Share your experience with this vehicle.</p>
                    </div>

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
                            v-model="form.review"
                            rows="6"
                            placeholder="Tell others about your experience..."
                            class="
                                w-full rounded-lg bg-[#121212] border border-[#333] 
                                px-4 py-3 text-white resize-none focus:border-[#C1121F] focus:outline-none
                                placeholder:text-sm"
                        />

                    </div>

                    <div>
                        <label class="block text-sm font-medium text-[#929292] mb-2">
                            Upload Photos (Optional)
                        </label>

                        <!-- Existing IDs from DB -->
                        <ClientCommonExistingImageList
                            v-if="props.mode === 'edit'"
                            :images="existingImages"
                            @remove="removeExistingImage"
                        />

                        <ClientCommonUploadedImagesList
                            :images="uploadedImages"
                            @remove="removeUploadedImage"
                        />
                        
                        <!-- Upload Area -->
                        <div
                            v-if="uploadedImages.length + existingImages.length < 5"
                            class="border-2 border-dashed border-[#C1121F]/40 hover:border-[#C1121F] rounded-xl h-24 flex flex-col items-center justify-center cursor-pointer transition"
                            @click="triggerUpload"
                            @dragover.prevent
                            @drop.prevent="handleDrop"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke-width="1.5"
                                stroke="#9E9E9E"
                                class="w-6 h-6 mb-2"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    d="M12 16.5V4.5m0 0L7.5 9m4.5-4.5L16.5 9M3 16.5v1.125A2.625 2.625 0 005.625 20.25h12.75A2.625 2.625 0 0021 17.625V16.5"
                                />
                            </svg>

                            <p class="text-[#9E9E9E] text-xs">
                                Click or drag images here
                            </p>
                        </div>

                        <input
                            ref="imageInput"
                            type="file"
                            accept="image/*"
                            multiple
                            class="hidden"
                            @change="handleImageChange"
                        />
                    </div>

                </div>

                <!-- Footer -->
                <div class="flex flex-col gap-2 my-4 mx-6">
                    <button
                        v-if="props.mode === 'create'"
                        @click="emit('submit')"
                        class="w-full bg-[#C1121F] hover:bg-red-700 text-white text-sm font-bold py-3 rounded-lg transition-colors duration-200"
                    >
                        Submit Review
                    </button>

                    <button
                        v-if="props.mode === 'edit'"
                        @click="emit('submit')"
                        class="w-full bg-[#C1121F] hover:bg-red-700 text-white text-sm font-bold py-3 rounded-lg transition-colors duration-200"
                    >
                        Update Review
                    </button>

                    <button
                        @click="$emit('update:modelValue', false)"
                        class="w-full border border-[#2a2a2a] hover:border-white text-white text-sm font-semibold py-3 rounded-lg transition-colors duration-200"
                    >
                        Cancel
                    </button>
                </div>

            </div>
        </div>

    </Transition>
</template>

<script setup lang="ts">
import type { Review } from '~/utils/api/api'

interface Props {
    modelValue: boolean
    mode?: 'create' | 'edit'
    myReview?: Review | null
    reviewState: ReturnType<typeof useWriteReview>
}

const props = withDefaults(defineProps<Props>(), {
    mode: 'create',
})

const emit = defineEmits<{
    (e: "update:modelValue", value: boolean): void
    (e: "submit"): void
    (e: "close"): void
}>()

const { form, hoverRating, uploadedImages,
        existingImages, imageInput, triggerUpload, 
        addFiles, handleImageChange, handleDrop, 
        removeUploadedImage, removeExistingImage, 
        originalImages, deletedImages 
} = props.reviewState

watch(() => props.modelValue, (v) => {
    console.log("modelValue:", v)
})

watch(
    () => props.myReview,
    (review) => {
        if (!review) return

        const images = review.images || []

        originalImages.value = [...images]
        console.log('original images', originalImages.value)
        existingImages.value = [...images]
        console.log('existing images', existingImages.value)

    },
    { immediate: true }
)

//Populate the modal
watch(
    () => props.modelValue,
    (open) => {
        if (open) {
            if (props.myReview) {
                form.rating = props.myReview.rating
                form.review = props.myReview.text

                existingImages.value = [...props.myReview.images]
            } else {
                form.rating = 0
                form.review = ""
                form.images = []
                uploadedImages.value = []
            }

            return
        }

        form.rating = 0
        form.review = ""
        form.images = []
        uploadedImages.value = []
    }
)

//Make the modal empty after user cancels to write a review
watch(
    () => props.modelValue,
    (open) => {
        if (!open) {

            Object.assign(form, {
                rating: 0,
                review: '',
                images: []
            })

            uploadedImages.value = []

            return
        }

    }
)
    
// For the modal
watch(
    () => props.modelValue,
    (open) => {
        if (!import.meta.client) return

        document.documentElement.style.overflow = open ? "hidden" : ""
    },
    { immediate: true }
)

</script>

<style scoped>
    .fade-enter-active,
    .fade-leave-active {
    transition: opacity .2s ease;
    }

    .fade-enter-from,
    .fade-leave-to {
    opacity: 0;
    }
</style>