<template>
    <Teleport to="body">
        <Transition
        enter-active-class="transition-opacity duration-200"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-200"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
        >
            <div
                v-if="modelValue"
                class="fixed inset-0 z-999 bg-black/70 px-auto overflow-y-hidden"
                @click.self="$emit('update:modelValue', false)"
            >
                <div class="h-full flex items-center justify-center">

                    <div
                        v-if="modelValue"
                        class="
                            bg-[#111111] border-t-[#C1121F] border-t-5 rounded-xl 
                            w-full h-[90%] max-w-md font-[poppins] flex flex-col
                        "
                    >

                    <!-- Header -->
                    <div class="flex items-start justify-between px-6 pt-5 pb-4 border-b border-white/10">

                        <div>
                            <h2 class="text-white font-semibold text-base font-[Poppins]">Edit profile</h2>
                            <p class="text-[#929292] text-xs mt-0.5">Update your personal information</p>
                        </div>

                        <button 
                            @click="closeModal" 
                            class="text-white/40 hover:text-white transition-colors mt-0.5"
                        >
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>

                    </div>

                    <!-- Avatar row -->
                    <div class="flex items-center px-5 py-4 gap-4">
                        <div class="w-14 h-14 rounded-full overflow-hidden flex-shrink-0">
                            <img
                                v-if="profilePreview"
                                :src="profilePreview"
                                alt="Profile"
                                class="w-full h-full object-cover"
                            />

                            <img
                                v-else
                                :src="`${user?.profile_picture}`"
                                alt="Profile"
                                class="w-full h-full object-cover"
                            />
                        </div>
                        
                        <div>
                            <p class="text-white font-medium text-sm font-[Poppins]">{{ user?.given_name }} {{ user?.family_name }}</p>
                            <p class="text-[#929292] text-xs">Member since {{ user?.date_created ? new Date(user.date_created).getFullYear() : '' }}</p>
                        </div>

                        <button
                            @click="triggerProfileUpload"
                            class="ml-auto text-white/60 border border-white/20 hover:border-white/40 hover:text-white text-xs px-3 py-1.5 rounded transition-colors">
                            Change photo
                        </button>

                        <input
                            ref="profileInput"
                            type="file"
                            accept="image/*"
                            class="hidden"
                            @change="handleProfileChange"
                        />
                    </div>

                    <!-- Personal Information -->
                    <div class="scroll-container flex flex-col gap-3 py-2 px-5 overflow-y-auto h-[80%]">

                        <div>
                            <div class="grid grid-cols-2 gap-3">
                                    <div>
                                    <label class="text-[#9E9E9E] text-[10px] uppercase tracking-wider block mb-1">First Name</label>
                                    <input
                                        type="text"
                                        v-model="form.given_name"
                                        class="
                                            w-full bg-[#111] border border-white/10 rounded 
                                            px-3 py-2 text-white text-sm 
                                            focus:outline-none focus:border-[#C1121F] 
                                            transition-colors"
                                    />
                                    </div>
                                    <div>
                                    <label class="text-[#9E9E9E] text-[10px] uppercase tracking-wider block mb-1">Last Name</label>
                                    <input
                                        type="text"
                                        v-model="form.family_name"
                                        class="
                                            w-full bg-[#111] border border-white/10 rounded 
                                            px-3 py-2 text-white text-sm 
                                            focus:outline-none focus:border-[#C1121F] 
                                            transition-colors"
                                    />
                                    </div>
                            </div>
                        </div>

                        <div>
                            <label class="text-[#9E9E9E] text-[10px] uppercase tracking-wider block mb-1">Email Address</label>
                            <input
                                type="email"
                                readonly
                                v-model="form.email"
                                class="
                                    w-full bg-[#111] border border-white/10 rounded 
                                    px-3 py-2 text-[#ABABAB] text-sm 
                                    focus:outline-none focus:border-[#C1121F] 
                                    transition-colors"
                            />
                        </div>

                        <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label class="text-[#9E9E9E] text-[10px] uppercase tracking-wider block mb-1">Contact Number</label>
                            <input
                                type="text"
                                v-model="form.contact_number"
                                class="
                                    w-full bg-[#111] border border-white/10 rounded 
                                    px-3 py-2 text-white text-sm 
                                    focus:outline-none focus:border-[#C1121F] 
                                    transition-colors"
                            />
                        </div>
                        <div>
                            <label class="text-[#9E9E9E] text-[10px] uppercase tracking-wider block mb-1">Address</label>
                            <input
                            type="text"
                            v-model="form.address"
                            class="
                                w-full bg-[#111] border border-white/10 rounded 
                                px-3 py-2 text-white text-sm 
                                focus:outline-none focus:border-[#C1121F] 
                                transition-colors"
                            />
                        </div>
                        </div>

                        <!-- Upload ID -->
                        <div class="flex flex-col gap-1.5">
                            <label class="text-[#9E9E9E] text-xs">Upload your valid IDs</label>
                            <p class="text-[#6E6E6E] text-[10px]">Valid ID that are accepted: national ID, driver license ID, passport.</p>

                            <!-- Existing IDs from DB -->
                            <div v-if="existingIdImages.length" class="flex flex-col gap-2">
                                <div
                                    v-for="(url, index) in existingIdImages"
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
                                        @click="removeExistingId(index, url)"
                                        class="text-white/40 hover:text-red-500"
                                    >
                                        ✕
                                    </button>

                                </div>
                            </div>

                            <!-- Uploaded ID Files List -->
                            <div v-if="uploadedIdFiles.length" class="flex flex-col gap-2 mt-2 mb-2">
                                <div
                                    v-for="(file, index) in uploadedIdFiles"
                                    :key="index"
                                    class="flex items-center justify-between bg-[#0f0f0f] border border-white/10 rounded-lg px-3 py-2"
                                >
                                    <!-- Left: file info -->
                                    <div class="flex items-center gap-3">
                                        
                                        <!-- File icon -->
                                        <div class="w-8 h-8 flex items-center justify-center bg-[#1a1a1a] rounded">
                                            <svg class="w-4 h-4 text-[#c1121f]" fill="currentColor" viewBox="0 0 24 24">
                                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                            </svg>
                                        </div>

                                        <!-- File details -->
                                        <div class="flex flex-col">
                                            <p class="text-white text-xs font-medium">
                                                {{ file.name }}
                                            </p>
                                            <p class="text-white/40 text-[10px]">
                                                {{ file.size }} KB
                                            </p>
                                        </div>

                                    </div>

                                    <!-- Remove button -->
                                    <button
                                        @click="removeIdFile(index)"
                                        class="text-white/40 hover:text-red-500 transition-colors"
                                    >
                                        ✕
                                    </button>
                                </div>

                            </div>

                            <!-- Drop zone -->
                            <div v-if="uploadedIdFiles.length < 2 && existingIdImages.length < 2"
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
                                    {{
                                        uploadedIdFiles.length === 0 || uploadedIdFiles.length === 1
                                            ? 'Click or drag and drop to upload image of the first ID'
                                            : 'Click or drag and drop to upload image of the second ID'
                                    }}
                                </p>
                            </div>

                            <input
                                ref="idInput"
                                type="file"
                                accept="image/*"
                                multiple
                                class="hidden"
                                @change="handleIdChange"
                            />

                        </div>

                        <!-- Delete account -->
                        <div class="flex items-center justify-between bg-[#111] border border-white/10 rounded px-4 py-3">
                        <div>
                            <p class="text-white text-sm">Delete account</p>
                            <p class="text-white/40 text-xs mt-0.5">This action is permanent and cannot be undone</p>
                        </div>
                        <button class="border border-[#C1121F] text-[#C1121F] hover:bg-[#C1121F] hover:text-white text-xs px-3 py-1.5 rounded transition-colors ml-4 flex-shrink-0">
                            Delete account
                        </button>
                        </div>

                    </div>

                    <!-- Footer -->
                    <div class="flex items-center justify-between px-6 py-4 border-t border-white/10">
                        <p class="text-white/30 text-xs">Changes are saved immediately</p>
                        <div class="flex items-center gap-2">
                        <button 
                            @click="closeModal" 
                            class="text-white/60 hover:text-white text-xs px-4 py-2 transition-colors"
                        >
                            Cancel
                        </button>
                        <button 
                            @click="saveChanges"
                            class="bg-[#C1121F] hover:bg-[#a00f1a] text-white text-xs px-5 py-2 rounded transition-colors font-medium"
                        >
                            Save changes
                        </button>
                        </div>
                    </div>

                    </div>

                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup lang="ts">
import type { User } from '~/utils/api/api'
const { apiFetch } = useApiFetch()
const { $swal } = useNuxtApp()

const props = defineProps<{
    modelValue: boolean
    user: User | null
}>()

const form = reactive({
    given_name: '',
    family_name: '',
    email: '',
    contact_number: '',
    address: '',
    id_images: []
})

watch(
    () => props.modelValue,
    (open) => {
        if (!open) {
            // RESET EVERYTHING HERE
            uploadedIdFiles.value = []
            existingIdImages.value = []
            originalIdImages.value = []

            Object.assign(form, {
                given_name: '',
                family_name: '',
                email: '',
                contact_number: '',
                address: '',
                id_images: []
            })

            return
        }

        if (!props.user) return

        Object.assign(form, {
            given_name: props.user.given_name,
            family_name: props.user.family_name,
            email: props.user.email,
            contact_number: props.user.contact_number,
            address: props.user.address,
            id_images: props.user.id_images || []
        })

        const images = props.user.id_images?.images || []

        existingIdImages.value = [...images]
        originalIdImages.value = [...images]

        // IMPORTANT: reset uploaded files too when opening
        uploadedIdFiles.value = []
    }
)

watch(
    () => props.modelValue,
    (open) => {
        if (!import.meta.client) return

        document.documentElement.style.overflow =
            open ? 'hidden' : ''
    },
    { immediate: true }
)

const closeModal = () => {
    if (import.meta.client) {
        document.documentElement.style.overflow = 'hidden'
    }

    emit('update:modelValue', false)
}

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'updated'): void
}>()

const {
    profilePreview,
    uploadedIdFiles,
    removeIdFile,
    removeExistingId,
    uploadProfilePicture,
    uploadIdFiles,

    profileInput,
    idInput,
    existingIdImages,
    originalIdImages,

    triggerProfileUpload,
    triggerIdUpload,

    handleProfileChange,
    handleIdChange,
    handleIdDrop,

    validateFile
} = useProfileUploads()

watch(
    () => props.user,
    (user) => {
        if (!user) return

        const images = user.id_images?.images || []

        originalIdImages.value = [...images]
        console.log('original images', originalIdImages.value)
        existingIdImages.value = [...images]
        console.log('existing images', existingIdImages.value)

    },
    { immediate: true }
)

const saveChanges = async () => {
    try {
        const removedImages = originalIdImages.value.filter(
            (url) => !existingIdImages.value.includes(url)
        )

        // Validate total ID images first
        const totalIdImages =
            existingIdImages.value.length +
            uploadedIdFiles.value.length

        if (totalIdImages !== 2) {
            await $swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'You must have exactly 2 ID images.',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff'
            })
            return
        }

        // Validate files before showing loading state
        for (const file of uploadedIdFiles.value) {
            if (!(await validateFile(file))) {
                return
            }
        }

        let newProfileImage = null

        if (profileInput.value) {
            newProfileImage = await uploadProfilePicture()

            if (newProfileImage === false) {
                $swal.close()
                return
            }
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

        const newIdUrls = await uploadIdFiles()

        const idUrls: string[] = [
            ...existingIdImages.value,
            ...newIdUrls
        ]

        const body: any = {
            given_name: form.given_name,
            family_name: form.family_name,
            email: form.email,
            contact_number: form.contact_number,
            address: form.address,
            id_images: {
                images: idUrls
            }
        }

        if (newProfileImage) {
            body.profile_picture = newProfileImage
        }

        if (removedImages.length > 0) {
            body.deleted_images = removedImages
        }

        const res = await apiFetch<{ message: string }>('/auth/me/', {
            method: 'PATCH',
            body
        })

        $swal.close()

        await $swal.fire({
            icon: 'success',
            title: 'Success',
            text: res.message,
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff'
        })

        emit('update:modelValue', false)
        emit('updated')
    } catch (error) {
        $swal.close()

        await $swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to save changes.',
            confirmButtonColor: '#C1121F',
            background: '#1a1a1a',
            color: '#ffffff'
        })
    }
}

</script>