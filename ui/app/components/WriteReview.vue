<template>
    <Transition name="fade">
        <div
            ref="modalRef"
            v-if="modelValue"
            class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 p-4"
            @click.self="$emit('update:modelValue', false)"
        >
            <div 
                class="
                    bg-[#111111] border-t-[#C1121F] border-t-5 rounded-xl 
                    w-full h-[90%] max-w-md font-[poppins] flex flex-col
                "
            >
                <!-- Header -->
                <div class="flex items-center justify-between p-6 border-b border-[#2A2A2A]">

                    <div>
                        <h2 class="text-white font-extrabold text-lg">Write a Review</h2>
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
                    <div v-if="existingImages.length" class="flex flex-col gap-2 mb-2">
                        <div
                            v-for="(url, index) in existingImages"
                            :key="'existing-' + index"
                            class="flex items-center justify-between bg-[#0f0f0f] border border-white/10 hover:border-[#c1121f] rounded-lg px-3 py-2 transition-colors"
                        >
                            <div class="flex items-center gap-3">
                                
                                <div class="w-8 h-8 flex items-center justify-center bg-[#1a1a1a] rounded">
                                    <svg class="w-4 h-4 text-[#c1121f]" fill="currentColor" viewBox="0 0 24 24">
                                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                    </svg>
                                </div>

                                <a
                                    :href="url"
                                    target="_blank"
                                    class="text-white text-xs hover:text-[#c1121f] transition-colors"
                                >
                                    View ID {{ index + 1 }}
                                </a>

                            </div>

                            <button
                                @click="removeExisting(index, url)"
                                class="text-white/40 hover:text-red-500"
                            >
                                ✕
                            </button>

                        </div>
                    </div>

                    <!-- Uploaded Files -->
                    <div v-if="uploadedImages.length" class="flex flex-col gap-2 mb-3">
                        <div
                            v-for="(file, index) in uploadedImages"
                            :key="index"
                            class="flex items-center justify-between bg-[#121212] border border-[#333] rounded-lg px-3 py-2"
                        >
                            <div class="flex items-center gap-3">

                                <div class="w-8 h-8 flex shrink-0 items-center justify-center bg-[#1a1a1a] rounded">
                                    <svg
                                        class="w-4 h-4 text-[#C1121F]"
                                        fill="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path d="M19 3H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V5a2 2 0 00-2-2zm0 16H5V5h14v14zm-4-7-2.5 3.01L11 13l-3 4h8z"/>
                                    </svg>
                                </div>

                                <div>
                                    <p class="text-white text-xs font-medium">
                                        {{ file.name }}
                                    </p>

                                    <p class="text-gray-500 text-[10px]">
                                        {{ (file.size / 1024).toFixed(1) }} KB
                                    </p>
                                </div>

                            </div>

                            <button
                                @click="removeImage(index)"
                                class="text-gray-500 hover:text-red-500 transition"
                            >
                                ✕
                            </button>
                        </div>
                    </div>

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
                        @click="submitReview"
                        class="w-full bg-[#C1121F] hover:bg-red-700 text-white text-sm font-bold py-3 rounded-lg transition-colors duration-200"
                    >
                        Submit Review
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
import type { Review, ReviewForm } from '~/utils/api/api'

import { ref } from "vue"
const { $swal } = useNuxtApp()

const props = defineProps<{
    carId: string
    modelValue: boolean
    myReview?: Review | null
}>()

const emit = defineEmits([
    "update:modelValue",
    "submit"
])

// For the modal
watch(
    () => props.modelValue,
    (open) => {
        if (!import.meta.client) return

        document.documentElement.style.overflow =
            open ? 'hidden' : ''
    },
    { immediate: true }
)

const modalRef = ref<HTMLElement | null>(null)
const hoverRating = ref(0)

const form = reactive<ReviewForm>({
    rating: 0,
    review: "",
    images: [],
})

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

const { createReview } = useReviews()

const submitReview = async () => {
    if (form.rating < 1 || form.rating > 5) {
        $swal.fire({
            target: modalRef.value,
            icon: 'error',
            title: 'Error',
            text: 'Please select a rating.',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff',
            customClass: {
                popup: 'swal-over-modal'
            }
        })
        return
    }

    $swal.fire({
        title: 'Saving changes...',
        text: 'Please wait.',
        background: '#1a1a1a',
        color: '#ffffff',
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => {
            $swal.showLoading()
        }
    })

    try {
        await createReview(props.carId, {
            rating: form.rating,
            review: form.review,
            images: uploadedImages.value,
        })

        Object.assign(form, {
            rating: 0,
            review: "",
            images: [],
        })

        uploadedImages.value = []

        $swal.close()

        await $swal.fire({
            icon: 'success',
            title: 'Success',
            text: 'Review submitted successfully.',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff'
        })

        emit("update:modelValue", false)
        window.location.reload()
    } catch (error) {
        console.error(error)
    }
}

const imageInput = ref<HTMLInputElement | null>(null)
const uploadedImages = ref<File[]>([])
const existingImages = ref<string[]>([])

const triggerUpload = () => {
    imageInput.value?.click()
}

const addFiles = (files: File[]) => {
    const remaining = 5 - uploadedImages.value.length

    uploadedImages.value.push(
        ...files
            .filter(file => file.type.startsWith("image/"))
            .slice(0, remaining)
    )
}

const handleImageChange = (event: Event) => {
    const input = event.target as HTMLInputElement

    if (!input.files) return

    addFiles(Array.from(input.files))

    input.value = ""
}

const handleDrop = (event: DragEvent) => {
    if (!event.dataTransfer) return

    addFiles(Array.from(event.dataTransfer.files))
}

const removeImage = (index: number) => {
    uploadedImages.value.splice(index, 1)
}

const removeExisting = (index: number, url: string) => {
    existingImages.value.splice(index, 1)
}
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