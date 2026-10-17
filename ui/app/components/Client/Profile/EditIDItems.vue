<template>
    <div class="flex flex-col gap-1.5">
        <label class="text-[#9E9E9E] text-xs">
            Upload your valid IDs
        </label>

        <p class="text-[#6E6E6E] text-[10px]">
            Valid ID that are accepted: national ID, driver license ID, passport.
        </p>

        <!-- Existing IDs -->
        <div
            v-if="props.existingIdImages.length"
            class="flex flex-col gap-2"
        >
            <div
                v-for="(url, index) in props.existingIdImages"
                :key="'existing-' + index"
                class="flex items-center justify-between bg-[#0f0f0f] border border-white/10 hover:border-[#c1121f] rounded-lg px-3 py-2 transition-colors"
            >
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 flex items-center justify-center bg-[#1a1a1a] rounded"
                    >
                        <svg
                            class="w-4 h-4 text-[#c1121f]"
                            fill="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
                            />
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
                    type="button"
                    @click="emit('removeExisting', index, url)"
                    class="text-white/40 hover:text-red-500"
                >
                    ✕
                </button>
            </div>
        </div>

        <!-- Uploaded ID Files -->
        <div
            v-if="props.uploadedIdFiles.length"
            class="flex flex-col gap-2 mt-2 mb-2"
        >
            <div
                v-for="(file, index) in props.uploadedIdFiles"
                :key="index"
                class="flex items-center justify-between bg-[#0f0f0f] border border-white/10 rounded-lg px-3 py-2"
            >
                <div class="flex items-center gap-3">
                    <div
                        class="w-8 h-8 flex flex-shrink-0 items-center justify-center bg-[#1a1a1a] rounded"
                    >
                        <svg
                            class="w-4 h-4 text-[#c1121f]"
                            fill="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
                            />
                        </svg>
                    </div>

                    <div class="flex flex-col">
                        <p class="text-white text-xs font-medium">
                            {{ file.name }}
                        </p>

                        <p class="text-white/40 text-[10px]">
                            {{
                                file.size >= 1024 * 1024
                                    ? `${(file.size / (1024 * 1024)).toFixed(1)} MB`
                                    : `${(file.size / 1024).toFixed(1)} KB`
                            }}
                        </p>
                    </div>
                </div>

                <button
                    type="button"
                    @click="emit('removeFile', index)"
                    class="text-white/40 hover:text-red-500 transition-colors"
                >
                    ✕
                </button>
            </div>
        </div>

        <!-- Drop Zone -->
        <div
            v-if="
                props.uploadedIdFiles.length < 5 &&
                props.existingIdImages.length < 5
            "
            class="border-2 border-dashed border-[#C1121F]/40 hover:border-[#C1121F] rounded-xl h-24 flex flex-col items-center justify-center cursor-pointer transition-colors duration-200"
            @click="triggerIdUpload"
            @dragover.prevent
            @drop.prevent="handleIdDrop"
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
                Click or drag and drop to upload ID'
            </p>
        </div>

        <input
            ref="idInput"
            type="file"
            accept="image/*,.pdf"
            multiple
            class="hidden"
            @change="handleIdChange"
        />
    </div>
</template>

<script setup lang="ts">
const props = defineProps<{
    existingIdImages: string[]
    uploadedIdFiles: File[]
}>()

const emit = defineEmits<{
    removeExisting: [index: number, url: string]
    removeFile: [index: number]
    change: [event: Event]
    drop: [event: DragEvent]
}>()

const idInput = ref<HTMLInputElement | null>(null)

const triggerIdUpload = () => {
    idInput.value?.click()
}

const handleIdChange = (event: Event) => {
    emit('change', event)
}

const handleIdDrop = (event: DragEvent) => {
    emit('drop', event)
}
</script>