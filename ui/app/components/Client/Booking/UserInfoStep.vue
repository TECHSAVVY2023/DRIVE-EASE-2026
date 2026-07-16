<script setup lang="ts">
defineProps<{
    form: {
        firstName: string
        lastName: string
        address: string
        contact: string
    }
    uploadedImages: string[]
}>()

defineEmits<{
    (e: 'trigger-upload'): void
    (e: 'drop', event: DragEvent): void
    (e: 'file-change', event: Event): void
    (e: 'remove-image', index: number): void
}>()

const fileInput = ref<HTMLInputElement | null>(null)
</script>

<template>
    <div class="flex flex-col gap-4">

        <!-- First + Last name -->
        <div class="grid grid-cols-2 gap-3">
            <div class="flex flex-col gap-1.5">
                <label class="text-gray-400 text-xs">First name</label>

                <input
                    :value="form.firstName"
                    @input="form.firstName = ($event.target as HTMLInputElement).value"
                    type="text"
                    class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm placeholder-[#444] focus:outline-none focus:border-[#C1121F] transition-colors duration-200"
                />
            </div>

            <div class="flex flex-col gap-1.5">
                <label class="text-gray-400 text-xs">Last name</label>

                <input
                    :value="form.lastName"
                    @input="form.lastName = ($event.target as HTMLInputElement).value"
                    type="text"
                    class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm placeholder-[#444] focus:outline-none focus:border-[#C1121F] transition-colors duration-200"
                />
            </div>
        </div>

        <!-- Address -->
        <div class="flex flex-col gap-1.5">
            <label class="text-gray-400 text-xs">Address</label>

            <input
                :value="form.address"
                @input="form.address = ($event.target as HTMLInputElement).value"
                type="text"
                class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm placeholder-[#444] focus:outline-none focus:border-[#C1121F] transition-colors duration-200"
            />
        </div>

        <!-- Contact -->
        <div class="flex flex-col gap-1.5">
            <label class="text-gray-400 text-xs">Contact number</label>

            <input
                :value="form.contact"
                @input="form.contact = ($event.target as HTMLInputElement).value"
                type="tel"
                class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm placeholder-[#444] focus:outline-none focus:border-[#C1121F] transition-colors duration-200"
            />
        </div>

        <!-- Upload -->
        <div class="flex flex-col gap-1.5">
            <label class="text-gray-400 text-xs">
                Upload image of two valid IDs
            </label>

            <p class="text-gray-500 text-[10px]">
                Valid ID that are accepted: national ID, driver license ID, passport.
            </p>

            <div
                class="border-2 border-dashed border-[#C1121F]/40 hover:border-[#C1121F] rounded-xl h-24 flex items-center justify-center cursor-pointer transition-colors duration-200"
                @click="$emit('trigger-upload')"
                @dragover.prevent
                @drop.prevent="$emit('drop', $event)"
            >
                <p class="text-gray-500 text-xs text-center px-4">
                    Click to upload image or drag and drop
                </p>
            </div>

            <input
                ref="fileInput"
                type="file"
                accept="image/*"
                multiple
                class="hidden"
                @change="$emit('file-change', $event)"
            />
        </div>

        <!-- Previews -->
        <div v-if="uploadedImages.length" class="flex flex-col gap-1.5">
            <label class="text-gray-400 text-xs">
                Uploaded images
            </label>

            <div class="flex gap-2 flex-wrap">
                <div
                    v-for="(img, i) in uploadedImages"
                    :key="i"
                    class="relative w-16 h-12 rounded-lg overflow-hidden border border-[#2a2a2a] flex-shrink-0"
                >
                    <img
                        :src="img"
                        alt="Uploaded ID"
                        class="w-full h-full object-cover"
                    />

                    <button
                        @click="$emit('remove-image', i)"
                        class="absolute top-0.5 right-0.5 w-4 h-4 bg-black/70 rounded-full flex items-center justify-center"
                    >
                        <svg
                            class="w-2.5 h-2.5 text-white"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M6 18L18 6M6 6l12 12"
                            />
                        </svg>
                    </button>
                </div>
            </div>
        </div>

    </div>
</template>