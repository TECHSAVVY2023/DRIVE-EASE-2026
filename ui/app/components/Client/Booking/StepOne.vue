<template>
    <div class="flex flex-col gap-4">
        
        <div 
            v-if="!user.family_name"
            class="flex flex-col gap-1.5"
        >
            <label class="text-white text-sm">Last name</label>
            <input
                v-model="form.lastName"
                type="text"
                class="smoked-control rounded-lg px-3 py-2.5 text-white text-sm"
            />
        </div>

        <!-- Address -->
        <div 
            v-if="!user.address"
            class="flex flex-col gap-1.5"
        >
            <label class="text-white text-sm">Address</label>
            <input
                required
                v-model="form.address"
                type="text"
                class="smoked-control rounded-lg px-3 py-2.5 text-white text-sm"
            />
        </div>

        <!-- Contact number -->
        <div 
            v-if="!user.contact_number"
            class="flex flex-col gap-1.5"
        >
            <label class="text-white text-sm">Contact number</label>
            <input
                required
                v-model="form.contact"
                type="tel"
                class="smoked-control rounded-lg px-3 py-2.5 text-white text-sm"
            />
        </div>

        <!-- Upload -->
        <div class="flex flex-col gap-1.5 pt-2">
            <label class="text-white text-sm">
                Upload image of two valid IDs
            </label>

            <div class="flex flex-col gap-1 pb-3">
                <p class="text-[#929292] text-xs">
                    • JPG or PNG, max 5MB per file
                </p>
                <p class="text-[#929292] text-xs">
                    • Make sure all text is clear and readable
                </p>
                <p class="text-[#929292] text-xs">
                    • Accepted: national ID, driver's license, or passport
                </p>
                <p class="text-[#929292] text-xs">
                    • Upload both front sides in a single image, or add them one at a time
                </p>
            </div>

            <ClientCommonExistingIDImagesList 
                :images="existingIdImages"
                @remove-existing-id="(index, url) => $emit('remove-existing-id', index, url)"
            />

            <ClientCommonUploadedIDImagesList
                :images="uploadedIdFiles"
                @remove-uploaded-id="(index) => $emit('remove-uploaded-id', index)"
            />

            <!-- Drop zone -->
            <div v-if="uploadedIdFiles.length < 6 && existingIdImages.length < 6 && uploadedIdFiles.length + existingIdImages.length < 6"
                class="border-2 border-dashed border-[#C1121F]/40 hover:border-[#C1121F] rounded-xl h-24 flex flex-col items-center justify-center cursor-pointer transition-colors duration-200"
                @click="triggerIdUpload"
                @dragover.prevent
                @drop.prevent="event => $emit('drop', event)"
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

                <p class="text-[#9E9E9E] text-xs text-center px-4">
                    Click or drag and drop to upload image of your ID
                </p>
            </div>

            <input
                ref="idInput"
                type="file"
                accept="image/*"
                multiple
                class="hidden"
                @change="event => $emit('file-change', event)"
            />
        </div>

    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
    form: any
    user: any
    existingIdImages: string[]
    uploadedIdFiles: File[]
}>()

const { idInput, triggerIdUpload } = useProfileUploads()

defineEmits<{
    (e: 'trigger-upload'): void
    (e: 'file-change', event: Event): void
    (e: 'drop', event: DragEvent): void
    (e: 'remove-uploaded-id', index: number): void
    (e: 'remove-existing-id', index: number, url: string): void
}>()

</script>
