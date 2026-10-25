<template>
    <label class="block text-sm font-medium text-[#929292] mb-2">
        Upload Photos (Optional)
    </label>

    <ClientCommonExistingImageList
        :images="existingImages || []"
        @remove="removeExistingImage"
    />

    <div v-if="images.length" class="flex flex-col gap-2 mb-3">
        <div
            v-for="(image, index) in images"
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
                        <path d="M19 3H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V5a2 2 0 00-2-2zm0 16H5V5h14v14zm-4-7-2.5 3.01L11 13l-1.5-2-3 4h8z"/>
                    </svg>
                </div>

                <div>
                    <p class="text-white text-xs font-medium">
                        {{ image.file?.name ?? image.url.split('/').pop() ?? 'Uploaded image' }}
                    </p>

                    <p class="text-gray-500 text-[10px]">
                        <template v-if="image.file">
                            {{ (image.file.size / 1024).toFixed(1) }} KB
                        </template>
                        <template v-else>
                            Existing image
                        </template>
                    </p>
                </div>
            </div>

            <button
                type="button"
                @click="removeImage(image.url)"
                class="text-gray-500 hover:text-red-500 transition"
                aria-label="Remove image"
            >
                ✕
            </button>

        </div>

    </div>

    <div
        class="border-2 border-dashed border-[#C1121F]/40 hover:border-[#C1121F] rounded-xl h-24 flex flex-col items-center justify-center cursor-pointer transition"
        @click="fileInput?.click()"
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
        ref="fileInput"
        type="file"
        accept="image/*"
        multiple
        class="hidden"
        @change="handleImageChange"
    />
</template>

<script setup lang="ts">
import type { ReviewImage } from '~/utils/api/api'
const { $swal } = useNuxtApp()

const props = defineProps<{
    images: ReviewImage[]
    existingImages?: string[]
}>()

const emit = defineEmits<{
    'update:images': [images: ReviewImage[]]
    'update:existingImages': [images: string[]]
}>()

const localExistingImages = ref<string[]>([
    ...(props.existingImages || [])
])

watch(
    () => props.existingImages,
    (images) => {
        localExistingImages.value = [...(images || [])]
    },
    { deep: true }
)

const removeExistingImage = (index: number, url: string) => {
    console.log('Removing image:', { index, url })
    console.log('Before removal:', localExistingImages.value)

    localExistingImages.value = localExistingImages.value.filter(
        image => image !== url
    )

    console.log('After removal:', localExistingImages.value)

    emit('update:existingImages', [...localExistingImages.value])
}

const fileInput = ref<HTMLInputElement | null>(null)

const handleImageChange = async (event: Event) => {
    const input = event.target as HTMLInputElement

    if (!input.files) return

    await addFiles(Array.from(input.files))

    input.value = ""
}

const validateFile = async (file: File): Promise<boolean> => {
    const MAX_FILE_SIZE = 50 * 1024 * 1024
    const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']

    const extension = file.name.split('.').pop()?.toLowerCase()

    if (!extension || !ALLOWED_EXTENSIONS.includes(extension)) {
        $swal.close()

        await $swal.fire({
            icon: 'error',
            title: 'Invalid File',
            text: 'Only JPG and PNG images are allowed.',
            confirmButtonText: 'OK',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff'
        })

        return false
    }

    if (file.size > MAX_FILE_SIZE) {
        $swal.close()

        await $swal.fire({
            icon: 'error',
            title: 'File Too Large',
            text: 'Image size must not exceed 50 MB.',
            confirmButtonText: 'OK',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff'
        })

        return false
    }

    return true
}

const addFiles = async (files: File[]) => {
    const totalImages =
        props.images.length + (props.existingImages?.length || 0)

    const remaining = Math.max(0, 5 - totalImages)

    if (remaining === 0) {
        await $swal.fire({
            icon: 'error',
            title: 'Image Limit Reached',
            text: 'You can only upload up to 5 images.',
            confirmButtonText: 'OK',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff'
        })
        return
    }

    const acceptedFiles = files.slice(0, remaining)
    const validFiles: File[] = []

    for (const file of acceptedFiles) {
        if (await validateFile(file)) {
            validFiles.push(file)
        }
    }

    const newImages = validFiles.map(file => ({
        url: URL.createObjectURL(file),
        file,
    }))

    emit('update:images', [
        ...props.images,
        ...newImages,
    ])

    if (files.length > remaining) {
        await $swal.fire({
            icon: 'warning',
            title: 'Image Limit Reached',
            text: `Only ${remaining} more image(s) can be added.`,
            confirmButtonText: 'OK',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff'
        })
    }
}

function removeImage(id: string) {
    const target = props.images.find(image => image.url === id)

    if (target?.file) {
        URL.revokeObjectURL(target.url)
    }
    
    const images = props.images.filter(image => image.url !== id)
    emit('update:images', images)
}

const handleDrop = (event: DragEvent) => {
    if (!event.dataTransfer) return

    addFiles(Array.from(event.dataTransfer.files))
}

</script>
