<template>
    <p class="mb-1.5 text-[12px] font-bold text-white">
        Photos
    </p>

    <p class="mb-2 text-[11px] text-[#929292]">
        Upload a photo and click a photo to set it as the thumbnail
    </p>

    <div class="mb-1.5 flex flex-wrap gap-2.5">

        <!-- Uploaded images -->
        <div
            v-for="image in images"
            :key="image.url"
            class="relative size-[66px] w-[88px] shrink-0 rounded-lg border"
            :class="
                thumbnailUrl === image.url
                    ? 'border-[1.5px] border-red-600'
                    : 'border-neutral-700'
            "
        >
            <button
                type="button"
                class="size-full focus:outline-none focus-visible:ring-2 focus-visible:ring-red-600"
                @click="setThumbnail(image.url)"
            >
                <img
                    :src="image.url"
                    alt=""
                    class="size-full object-cover"
                />
            </button>

            <!-- Thumbnail label -->
            <span
                v-if="thumbnailUrl === image.url"
                class="
                    pointer-events-none absolute inset-x-0 bottom-0 
                    bg-[#c1121f] py-0.5 text-center text-[9px] text-white
                "
            >
                Thumbnail
            </span>

            <!-- Remove -->
            <button
                type="button"
                class="absolute -right-1.5 -top-1.5 flex size-[18px] items-center justify-center rounded-full border border-neutral-700 bg-neutral-950 text-neutral-400 hover:text-white"
                aria-label="Remove photo"
                @click="removeImage(image.url)"
            >
                <span class="relative block size-2.5">
                    <span
                        class="absolute left-1/2 top-1/2 h-px w-3 -translate-x-1/2 -translate-y-1/2 rotate-45 bg-current"
                    ></span>
                    <span
                        class="absolute left-1/2 top-1/2 h-px w-3 -translate-x-1/2 -translate-y-1/2 -rotate-45 bg-current"
                    ></span>
                </span>
            </button>
        </div>

        <!-- Add button -->
        <button
            type="button"
            class="flex size-[66px] w-[88px] shrink-0 flex-col items-center justify-center gap-0.5 rounded-lg border border-dashed border-neutral-700 bg-neutral-900 text-neutral-500 hover:border-neutral-600 hover:text-neutral-300"
            @click="fileInput?.click()"
        >
            <span class="relative block size-4">
                <span
                    class="absolute left-1/2 top-1/2 h-[1.5px] w-4 -translate-x-1/2 -translate-y-1/2 bg-current"
                ></span>
                <span
                    class="absolute left-1/2 top-1/2 h-4 w-[1.5px] -translate-x-1/2 -translate-y-1/2 bg-current"
                ></span>
            </span>

            <span class="text-[10px]">Add</span>
        </button>

        <!-- Hidden file input -->
        <input
            ref="fileInput"
            type="file"
            accept="image/png,image/jpeg"
            multiple
            class="hidden"
            @change="handleImageChange"
        />
    </div>

    <p class="mb-5 text-[10px] text-neutral-500">
        PNG or JPG, up to 5MB each
    </p>
</template>

<script setup lang="ts">
import type { Car, CarForm, VehicleImage } from '~/utils/api/api'
const { $swal } = useNuxtApp()

const props = defineProps<{
    images: VehicleImage[]
    thumbnailUrl: string | null
}>()

const emit = defineEmits<{
    'update:images': [images: VehicleImage[]]
    'update:thumbnailUrl': [url: string | null]
}>()

const fileInput = ref<HTMLInputElement | null>(null)

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
    const remaining = 5 - props.images.length
    const validFiles: File[] = []

    for (const file of files) {
        if (validFiles.length >= remaining) break

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

    if (!props.thumbnailUrl && newImages.length > 0) {
        emit('update:thumbnailUrl', newImages[0].url)
    }
}

const handleImageChange = async (event: Event) => {
    const input = event.target as HTMLInputElement

    if (!input.files) return

    await addFiles(Array.from(input.files))

    input.value = ""
}

function removeImage(id: string) {
    const target = props.images.find(image => image.url === id)

    if (target?.file) {
        URL.revokeObjectURL(target.url)
    }
    
    const images = props.images.filter(image => image.url !== id)

    emit('update:images', images)

    if (props.thumbnailUrl === id) {
        emit('update:thumbnailUrl', images[0]?.url ?? null)
    }
}

function setThumbnail(url: string) {
    emit('update:thumbnailUrl', url)
}
</script>
