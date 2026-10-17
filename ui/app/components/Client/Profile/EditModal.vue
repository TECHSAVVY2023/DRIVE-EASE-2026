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
                    <ClientProfileEditAvatar
                        :user="user"
                        :profile-preview="profilePreview"
                        @change="handleProfileChange"
                    />

                    <!-- Personal Information -->
                    <div class="scroll-container flex flex-col gap-3 py-2 px-5 overflow-y-auto h-[80%]">

                        <!-- Personal Info Component -->
                        <ClientProfileEditPersonalInfo 
                            :form="form" 
                        />

                        <ClientProfileEditIDItems
                            :existing-id-images="existingIdImages"
                            :uploaded-id-files="uploadedIdFiles"
                            @remove-existing="removeExistingId"
                            @remove-file="removeIdFile"
                            @change="handleIdChange"
                            @drop="handleIdDrop"
                        />

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
import type { User, UpdateProfilePayload } from '~/utils/api/api'
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

const resetForm = () => {
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
}

const loadUser = (user: User) => {
    Object.assign(form, {
        given_name: user.given_name,
        family_name: user.family_name,
        email: user.email,
        contact_number: user.contact_number,
        address: user.address,
        id_images: user.id_images || []
    })

    const images = user.id_images?.images || []

    existingIdImages.value = [...images]
    originalIdImages.value = [...images]
    uploadedIdFiles.value = []
}

watch(
    () => props.modelValue,
    (open) => {
        if (!open) { resetForm(); return }

        if (props.user) { loadUser(props.user) }
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

const { profilePreview, uploadedIdFiles, removeIdFile, removeExistingId, uploadProfilePicture, uploadIdFiles,
    idInput, existingIdImages, originalIdImages, triggerIdUpload, handleProfileChange, profileImage,
    handleIdChange, handleIdDrop, validateFile } = useProfileUploads()

watch(
    () => props.user,
    (user) => {
        if (!user) return

        const images = user.id_images?.images || []

        originalIdImages.value = [...images]
        existingIdImages.value = [...images]

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

        if (totalIdImages > 5) {
            await $swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'You can upload a maximum of 5 files.',
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

        // Show loading immediately
        $swal.fire({
            title: 'Saving changes...',
            text: 'Please wait.',
            background: '#1a1a1a',
            color: '#ffffff',
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                $swal.showLoading()
            }
        })

        let newProfileImage = null

        if (profileImage.value) {
            newProfileImage = await uploadProfilePicture()

            if (newProfileImage === false) {
                $swal.close()
                return
            }
        }

        const newIdUrls = await uploadIdFiles()

        const idUrls: string[] = [
            ...existingIdImages.value,
            ...newIdUrls
        ]

        const body: UpdateProfilePayload = {
            ...form,
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