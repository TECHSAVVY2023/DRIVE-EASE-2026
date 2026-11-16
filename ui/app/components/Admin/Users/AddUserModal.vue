<template>
    <Teleport to="body">
        <Transition
            enter-active-class="transition duration-150"
            leave-active-class="transition duration-100"
            enter-from-class="opacity-0"
            leave-to-class="opacity-0"
        >
            <div
                v-if="open"
                class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 p-4"
                @click.self="close"
            >
                <div
                    class="max-h-[90vh] w-full max-w-xl overflow-y-auto rounded-2xl border-t-5 border-t-[#C1121F] bg-[#111111]"
                    role="dialog"
                    aria-modal="true"
                    aria-labelledby="add-user-title"
                >
                    <header class="flex items-start justify-between border-b border-white/10 px-6 py-5">
                        <div>
                            <h2 id="add-user-title" class="text-lg font-extrabold text-white">
                                Add user
                            </h2>
                            <p class="mt-1 text-xs text-[#929292]">
                                Create an account that the user can access through Google login
                            </p>
                        </div>

                        <button
                            type="button"
                            class="mt-0.5 text-white/40 transition-colors hover:text-white"
                            aria-label="Close modal"
                            @click="close"
                        >
                            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" d="M6 6l12 12M18 6 6 18" />
                            </svg>
                        </button>
                    </header>

                    <form @submit.prevent="save">
                        <div class="grid gap-4 px-6 py-5 sm:grid-cols-2">
                            <div>
                                <label for="new-user-first-name" :class="labelClass">First name</label>
                                <input id="new-user-first-name" v-model.trim="form.given_name" :class="fieldClass" required>
                            </div>

                            <div>
                                <label for="new-user-last-name" :class="labelClass">Last name</label>
                                <input id="new-user-last-name" v-model.trim="form.family_name" :class="fieldClass" required>
                            </div>

                            <div class="sm:col-span-2">
                                <label for="new-user-email" :class="labelClass">Google email</label>
                                <input id="new-user-email" v-model.trim="form.email" type="email" :class="fieldClass" required>
                                <p class="mt-1.5 text-[10px] leading-4 text-[#777]">
                                    This must match the Google account the user will use to sign in.
                                </p>
                            </div>

                            <div>
                                <label for="new-user-contact" :class="labelClass">Contact number</label>
                                <input id="new-user-contact" v-model.trim="form.contact_number" type="tel" :class="fieldClass">
                            </div>

                            <div>
                                <label for="new-user-role" :class="labelClass">Role</label>
                                <div class="relative">
                                    <select id="new-user-role" v-model="form.role" :class="`${fieldClass} appearance-none pr-9`" required>
                                        <option value="Customer">Customer</option>
                                        <option v-if="props.canManageRoles" value="Admin">Admin</option>
                                        <option v-if="props.canManageRoles" value="Super Admin">Super Admin</option>
                                    </select>
                                    <svg class="pointer-events-none absolute right-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-[#8a8a8a]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="m6 9 6 6 6-6" />
                                    </svg>
                                </div>
                            </div>

                            <div class="sm:col-span-2">
                                <label for="new-user-address" :class="labelClass">Address</label>
                                <textarea id="new-user-address" v-model.trim="form.address" rows="3" :class="`${fieldClass} resize-none`" />
                            </div>

                            <div class="sm:col-span-2">
                                <div class="mb-2">
                                    <label :class="labelClass">Valid IDs</label>
                                    <p class="text-[10px] leading-4 text-[#777]">
                                        Upload two valid IDs, with a maximum of five files. JPG, JPEG, PNG, and PDF files up to 50 MB are accepted.
                                    </p>
                                </div>

                                <div v-if="uploadedIdFiles.length" class="mb-3 space-y-2">
                                    <div
                                        v-for="(file, index) in uploadedIdFiles"
                                        :key="`${file.name}-${file.lastModified}`"
                                        class="flex items-center justify-between rounded-lg border border-white/10 bg-[#0f0f0f] px-3 py-2"
                                    >
                                        <div class="flex min-w-0 items-center gap-3">
                                            <div class="flex h-8 w-8 shrink-0 items-center justify-center rounded bg-[#1a1a1a] text-[#C1121F]">
                                                <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
                                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                                                </svg>
                                            </div>
                                            <div class="min-w-0">
                                                <p class="truncate text-xs font-medium text-white">{{ file.name }}</p>
                                                <p class="text-[10px] text-white/40">{{ formatFileSize(file.size) }}</p>
                                            </div>
                                        </div>
                                        <button type="button" class="ml-3 text-white/40 transition hover:text-red-500" aria-label="Remove ID file" @click="removeIdFile(index)">
                                            ×
                                        </button>
                                    </div>
                                </div>

                                <div
                                    v-if="uploadedIdFiles.length < 5"
                                    class="flex h-24 cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-[#C1121F]/40 transition-colors hover:border-[#C1121F]"
                                    @click="triggerIdUpload"
                                    @dragover.prevent
                                    @drop.prevent="handleAdminIdDrop"
                                >
                                    <svg class="mb-2 h-6 w-6 text-[#9E9E9E]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 16.5V4.5m0 0L7.5 9m4.5-4.5L16.5 9M3 16.5v1.125A2.625 2.625 0 0 0 5.625 20.25h12.75A2.625 2.625 0 0 0 21 17.625V16.5" />
                                    </svg>
                                    <p class="px-4 text-center text-xs text-[#9E9E9E]">
                                        Click or drag and drop ID documents ({{ uploadedIdFiles.length }}/5)
                                    </p>
                                </div>

                                <input
                                    ref="idInput"
                                    type="file"
                                    accept="image/jpeg,image/png,.jpg,.jpeg,.png,.pdf,application/pdf"
                                    multiple
                                    class="hidden"
                                    @change="handleAdminIdChange"
                                >
                            </div>

                            <div class="sm:col-span-2 rounded-xl border border-[#2a2a2a] bg-[#0f0f0f] p-4">
                                <p class="text-xs font-semibold text-white">Google authentication only</p>
                                <p class="mt-1 text-[11px] leading-5 text-[#858585]">
                                    No password will be created. The user signs in with the Google account matching the email above.
                                </p>
                            </div>
                        </div>

                        <footer class="flex justify-end gap-2.5 border-t border-neutral-800 px-5 py-4">
                            <button type="button" class="rounded-lg border border-[#2a2a2a] px-4 py-2 text-xs text-[#CCCCCC] transition-colors hover:border-white hover:text-white" @click="close">
                                Cancel
                            </button>
                            <button type="submit" :disabled="!canSave" class="rounded-lg bg-[#C1121F] px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-[#9B0E18] disabled:cursor-not-allowed disabled:opacity-50">
                                Add user
                            </button>
                        </footer>
                    </form>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup lang="ts">
import type { AdminCreateUserFormPayload } from '~/utils/types/accounts'

const open = defineModel<boolean>({ required: true })
const props = defineProps<{
    canManageRoles: boolean
}>()
const emit = defineEmits<{
    save: [payload: { body: AdminCreateUserFormPayload; idFiles: File[] }]
}>()

const emptyForm = (): AdminCreateUserFormPayload => ({
    given_name: '',
    family_name: '',
    email: '',
    contact_number: '',
    address: '',
    role: 'Customer',
})
const form = reactive<AdminCreateUserFormPayload>(emptyForm())
const {
    uploadedIdFiles,
    idInput,
    triggerIdUpload,
    handleIdChange,
    handleIdDrop,
    removeIdFile,
} = useProfileUploads()
const canSave = computed(() =>
    Boolean(
        form.given_name.trim()
        && form.family_name.trim()
        && form.email.trim()
        && uploadedIdFiles.value.length <= 5
    )
)

watch(open, isOpen => {
    if (isOpen) {
        Object.assign(form, emptyForm())
        uploadedIdFiles.value = []
    }
})

const limitIdFiles = () => {
    uploadedIdFiles.value = uploadedIdFiles.value.slice(0, 5)
}

const handleAdminIdChange = (event: Event) => {
    handleIdChange(event)
    limitIdFiles()
}

const handleAdminIdDrop = (event: DragEvent) => {
    handleIdDrop(event)
    limitIdFiles()
}

const formatFileSize = (bytes: number) =>
    bytes >= 1024 * 1024
        ? `${(bytes / (1024 * 1024)).toFixed(1)} MB`
        : `${Math.max(1, Math.round(bytes / 1024))} KB`

const close = () => {
    open.value = false
}

const save = () => {
    if (!canSave.value) return
    emit('save', {
        body: { ...form, email: form.email.trim().toLowerCase() },
        idFiles: [...uploadedIdFiles.value],
    })
}

const labelClass = 'mb-1.5 block text-xs text-neutral-400'
const fieldClass = 'w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3.5 py-2.5 text-[13px] text-[#c8c8c8] outline-none transition-colors placeholder:text-[#555] hover:border-[#C1121F] focus:border-[#C1121F]'
</script>
