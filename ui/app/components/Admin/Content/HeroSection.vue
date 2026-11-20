<template>
    <ContentSection
        title="Hero section"
        description="Manage the main message, call to action, and featured car image"
    >
        <div class="grid gap-4 sm:grid-cols-2">
            <div>
                <label for="home-heading1" :class="labelClass">Main heading1</label>
                <input
                    id="home-heading1"
                    v-model="props.form.hero_heading1"
                    :class="fieldClass"
                />
            </div>

            <div>
                <label for="home-heading2" :class="labelClass">Main heading2</label>
                <input
                    id="home-heading2"
                    v-model="props.form.hero_heading2"
                    :class="fieldClass"
                />
            </div>

            <div class="sm:col-span-2">
                <label for="home-description" :class="labelClass">Tagline</label>
                <input
                    id="home-description"
                    v-model="props.form.hero_tagline"
                    :class="fieldClass"
                />
            </div>

            <div class="border-t border-[#262626] pt-4 sm:col-span-2">
                <label :class="labelClass">Main car image</label>

                <div class="flex flex-col gap-4 rounded-lg border border-[#2a2a2a] bg-[#101010] p-4 sm:flex-row sm:items-center sm:justify-between">
                    <div class="flex min-w-0 items-center gap-3">
                        <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[#222] text-[#C1121F]">
                            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="3" y="3" width="18" height="18" rx="2" />
                                <circle cx="8.5" cy="8.5" r="1.5" />
                                <path d="m21 15-5-5L5 21" />
                            </svg>
                        </div>

                        <div class="min-w-0">
                            <p class="truncate text-[11px] font-medium text-[#d0d0d0]">
                                {{ currentImageName }} 
                            </p>
                            <p class="mt-0.5 text-[9px] text-[#666]">PNG required</p>
                        </div>

                    </div>

                    <div class="min-w-0 flex-1 sm:max-w-md">
                        <p class="text-[10px] leading-4 text-[#888]">
                            Recommended: <span class="font-semibold text-[#bbb]">1536 × 1024 px</span>
                            transparent PNG. Keep the full car visible; other sizes may appear smaller or softer.
                        </p>
                    </div>

                    <button
                        type="button"
                        :class="secondaryButtonClass"
                        @click="fileInput?.click()"
                    >
                        Replace image
                    </button>

                    <input
                        ref="fileInput"
                        type="file"
                        accept="image/png"
                        class="hidden"
                        @change="handleImageChange"
                    />
                </div>
            </div>
        </div>
    </ContentSection>
</template>

<script setup lang="ts">
import type { HomepageContent } from '~/utils/types/content'

const props = defineProps<{
    form: HomepageContent
}>()

const emit = defineEmits<{
    'update:newImageFile': [file: File]
}>()

const { $swal } = useNuxtApp()

const fileInput = ref<HTMLInputElement | null>(null)

const handleImageChange = async (event: Event) => {
    const input = event.target as HTMLInputElement

    if (!input.files) return

    await addFiles(Array.from(input.files))

    input.value = ""
}

const addFiles = async (files: File[]) => {
    const file = files[0]

    if (!file) return

    if (!(await validateFile(file))) return

    const newImage = URL.createObjectURL(file)

    props.form.hero_image = newImage
    emit('update:newImageFile', file)
}

const validateFile = async (file: File): Promise<boolean> => {
    const MAX_FILE_SIZE = 50 * 1024 * 1024

    const extension = file.name.split('.').pop()?.toLowerCase()

    if (extension !== 'png' || file.type !== 'image/png') {
        $swal.close()

        await $swal.fire({
            icon: 'error',
            title: 'Invalid File',
            text: 'Only PNG images are allowed.',
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

const currentImageName = computed(() => {
    if (!props.form.hero_image) return 'No image uploaded'

    const imageUrl = props.form.hero_image

    try {
        const fileName = decodeURIComponent(
            new URL(imageUrl).pathname.split('/').pop() || 'Current image'
        )

        const lastDotIndex = fileName.lastIndexOf('.')

        if (lastDotIndex === -1) {
            return fileName.length > 25
                ? `${fileName.slice(0, 22)}...`
                : fileName
        }

        const name = fileName.slice(0, lastDotIndex)
        const extension = fileName.slice(lastDotIndex)

        return name.length > 25
            ? `${name.slice(0, 22)}...${extension}`
            : fileName
    } catch {
        const fileName = imageUrl.split('/').pop() || 'Current image'

        return fileName.length > 25
            ? `${fileName.slice(0, 22)}...`
            : fileName
    }
})

const fieldClass = `
    w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f]
    px-3.5 py-2.5 text-[13px] text-[#d4d4d4]
    outline-none transition-colors placeholder:text-[#555]
    focus:border-[#C1121F]
`
const labelClass = 'mb-1.5 block text-[11px] text-neutral-400'
const secondaryButtonClass = `
    shrink-0 rounded-lg border border-[#343434] bg-[#1b1b1b]
    px-3 py-2 text-[10px] font-semibold text-[#bbb]
    transition hover:border-[#C1121F] hover:text-white
`

</script>
