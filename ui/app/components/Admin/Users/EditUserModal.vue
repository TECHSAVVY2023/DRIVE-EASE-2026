<template>
    <Teleport to="body">
        <Transition
            enter-active-class="transition duration-150"
            leave-active-class="transition duration-100"
            enter-from-class="opacity-0"
            leave-to-class="opacity-0"
        >
            <div
                v-if="open && user"
                class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 p-4"
                @click.self="close"
            >
                <div
                    class="flex max-h-[90vh] w-full max-w-2xl flex-col overflow-hidden rounded-2xl border-t-5 border-t-[#C1121F] bg-[#111111] shadow-2xl"
                    role="dialog"
                    aria-modal="true"
                    aria-labelledby="edit-user-title"
                >
                    <header class="flex items-start justify-between border-b border-white/10 px-5 py-5 sm:px-6">
                        <div>
                            <h2 id="edit-user-title" class="text-lg font-extrabold text-white">
                                Edit user
                            </h2>
                            <p class="mt-1 text-xs text-neutral-500">
                                Review and update this user's account details
                            </p>
                        </div>

                        <button
                            type="button"
                            class="mt-0.5 text-white/40 transition-colors hover:text-white"
                            aria-label="Close edit user modal"
                            @click="close"
                        >
                            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" d="M6 6l12 12M18 6 6 18" />
                            </svg>
                        </button>
                    </header>

                    <form class="flex min-h-0 flex-1 flex-col" @submit.prevent="save">
                        <div class="flex-1 overflow-y-auto px-5 py-5 sm:px-6">
                            <div class="mb-6 rounded-xl border border-[#282828] bg-[#171717] p-4">
                                <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                                    <div class="flex min-w-0 items-center gap-3">
                                        <div class="flex h-12 w-12 shrink-0 items-center justify-center overflow-hidden rounded-full bg-[#C1121F] text-sm font-bold text-white">
                                            <img v-if="form.profile_picture" :src="form.profile_picture" alt="User profile picture" class="h-full w-full object-cover">
                                            <span v-else>{{ initials }}</span>
                                        </div>
                                        <div class="min-w-0">
                                            <p class="truncate text-sm font-semibold text-white">{{ fullName || 'Unnamed user' }}</p>
                                            <p class="truncate text-xs text-neutral-500">{{ form.email }}</p>
                                        </div>
                                    </div>
                                    <div v-if="form.profile_picture" class="flex shrink-0 gap-2">
                                        <button type="button" :class="secondaryButtonClass" @click="viewFile(form.profile_picture, 0, 'Profile picture', [form.profile_picture])">View</button>
                                        <button type="button" :class="removalButtonClass" @click="profileRemovalRequested = !profileRemovalRequested">
                                            {{ profileRemovalRequested ? 'Keep picture' : 'Remove' }}
                                        </button>
                                    </div>
                                </div>
                                <div v-if="profileRemovalRequested" class="mt-4 border-t border-white/10 pt-4">
                                    <label for="profile-removal-reason" :class="labelClass">Reason for removing profile picture <span class="text-[#e63946]">*</span></label>
                                    <textarea id="profile-removal-reason" v-model="profileRemovalReason" rows="3" required placeholder="Explain why this profile picture should be removed..." :class="fieldClass" />
                                    <p class="mt-1.5 text-[11px] text-neutral-600">The picture will be removed when you save these changes.</p>
                                </div>
                            </div>

                            <p :class="sectionClass">Personal information</p>
                            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                                <div>
                                    <label for="edit-first-name" :class="labelClass">First name</label>
                                    <input id="edit-first-name" v-model="form.given_name" type="text" :class="fieldClass">
                                </div>
                                <div>
                                    <label for="edit-last-name" :class="labelClass">Last name</label>
                                    <input id="edit-last-name" v-model="form.family_name" type="text" :class="fieldClass">
                                </div>
                                <div>
                                    <label for="edit-email" :class="labelClass">Email address</label>
                                    <input id="edit-email" v-model="form.email" type="email" :class="fieldClass">
                                </div>
                                <div>
                                    <label for="edit-contact" :class="labelClass">Contact number</label>
                                    <input id="edit-contact" v-model="form.contact_number" type="tel" :class="fieldClass">
                                </div>
                                <div class="sm:col-span-2">
                                    <label for="edit-address" :class="labelClass">Address</label>
                                    <textarea id="edit-address" v-model="form.address" rows="3" :class="fieldClass" />
                                </div>
                            </div>

                            <p :class="[sectionClass, 'mt-7']">Identification documents</p>
                            <div class="rounded-xl border border-[#282828] bg-[#171717] p-4">
                                <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                                    <div>
                                        <p class="text-sm font-semibold text-white">Uploaded IDs</p>
                                        <p class="mt-1 text-xs text-neutral-500">Sensitive image or PDF documents uploaded for verification</p>
                                    </div>
                                    <button
                                        v-if="selectedIdFiles.length"
                                        type="button"
                                        :class="secondaryButtonClass"
                                        @click="clearSelectedIdFiles"
                                    >
                                        Clear selection ({{ selectedIdFiles.length }})
                                    </button>
                                </div>

                                    <div v-if="idFiles.length" class="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3">
                                        <div
                                            v-for="(file, index) in idFiles"
                                            :key="`${file}-${index}`"
                                            class="relative overflow-hidden rounded-lg border bg-[#0f0f0f] transition-colors"
                                            :class="isIdFileSelected(file) ? 'border-[#C1121F] ring-1 ring-[#C1121F]' : 'border-[#303030]'"
                                        >
                                            <button
                                                type="button"
                                                class="group relative block aspect-[4/3] w-full overflow-hidden"
                                                :aria-label="`View identification document ${index + 1}`"
                                                @click="viewFile(file, index, 'Identification documents', idFiles)"
                                            >
                                                <img v-if="!isPdfFile(file)" :src="file" :alt="`ID document ${index + 1}`" class="h-full w-full object-cover transition duration-200 group-hover:scale-105 group-hover:opacity-70">
                                                <div v-else class="flex h-full flex-col items-center justify-center gap-2 text-[#e55a64]">
                                                    <svg class="h-9 w-9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M6 2h8l4 4v16H6z"/><path d="M14 2v5h5M8.5 15h7M8.5 18h5"/></svg>
                                                    <span class="text-xs font-semibold">PDF document</span>
                                                </div>
                                                <span class="absolute inset-x-0 bottom-0 truncate bg-black/75 px-2 py-1.5 text-[11px] text-white">{{ fileLabel(file, index) }}</span>
                                            </button>
                                            <button
                                                type="button"
                                                class="absolute right-2 top-2 flex h-7 w-7 items-center justify-center rounded-md border text-white shadow-lg transition-colors"
                                                :class="isIdFileSelected(file) ? 'border-[#C1121F] bg-[#C1121F]' : 'border-white/20 bg-black/70 hover:border-[#C1121F]'"
                                                :aria-label="isIdFileSelected(file) ? `Keep document ${index + 1}` : `Select document ${index + 1} for removal`"
                                                :title="isIdFileSelected(file) ? 'Keep this document' : 'Select for removal'"
                                                @click="toggleIdFileSelection(file)"
                                            >
                                                <svg v-if="isIdFileSelected(file)" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 12 4 4L19 6" stroke-linecap="round" stroke-linejoin="round" /></svg>
                                                <svg v-else class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 5l14 14M19 5 5 19" stroke-linecap="round" /></svg>
                                            </button>
                                        </div>
                                    </div>
                                    <div v-else class="mt-4 rounded-lg border border-dashed border-[#303030] px-4 py-6 text-center text-xs text-neutral-500">
                                        No identification documents uploaded
                                    </div>

                                    <div v-if="selectedIdFiles.length" class="mt-4 border-t border-white/10 pt-4">
                                        <div class="mb-3 flex items-center gap-2 rounded-lg border border-[#5b2429] bg-[#2a1517] px-3 py-2 text-xs text-[#f06a73]">
                                            {{ selectedIdFiles.length }} document{{ selectedIdFiles.length === 1 ? '' : 's' }} selected for removal
                                        </div>
                                        <label for="id-removal-reason" :class="labelClass">Reason for removing selected documents <span class="text-[#e63946]">*</span></label>
                                        <textarea
                                            id="id-removal-reason"
                                            v-model="idRemovalReason"
                                            rows="3"
                                            required
                                            placeholder="Explain why these identification documents should be removed..."
                                            :class="fieldClass"
                                        />
                                        <p class="mt-1.5 text-[11px] text-neutral-600">Only the selected documents will be removed when you save.</p>
                                    </div>
                            </div>

                            <p :class="[sectionClass, 'mt-7']">Account access</p>
                            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                                <div>
                                    <label for="edit-role" :class="labelClass">Role</label>
                                    <div class="relative">
                                        <select id="edit-role" v-model="form.role" disabled :class="[fieldClass, 'cursor-not-allowed appearance-none pr-9 opacity-60']">
                                            <option value="User">User</option>
                                            <option value="Admin">Admin</option>
                                            <option value="Super Admin">Super Admin</option>
                                        </select>
                                        <svg class="pointer-events-none absolute right-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-[#8a8a8a]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <path d="m6 9 6 6 6-6" stroke-linecap="round" stroke-linejoin="round" />
                                        </svg>
                                    </div>
                                </div>
                                <div>
                                    <label for="edit-status" :class="labelClass">Status</label>
                                    <div class="relative">
                                        <select id="edit-status" v-model="form.status" disabled :class="[fieldClass, 'cursor-not-allowed appearance-none pr-9 opacity-60']">
                                            <option value="Active">Active</option>
                                            <option value="Suspended">Suspended</option>
                                        </select>
                                        <svg class="pointer-events-none absolute right-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-[#8a8a8a]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <path d="m6 9 6 6 6-6" stroke-linecap="round" stroke-linejoin="round" />
                                        </svg>
                                    </div>
                                </div>
                            </div>
                            <p class="mt-2 text-[11px] text-neutral-600">Use Assign role or the user table's status action to change account access.</p>

                            <div class="mt-6 grid grid-cols-1 gap-3 text-xs sm:grid-cols-3">
                                <div v-for="detail in accountDetails" :key="detail.label" class="rounded-lg border border-[#282828] bg-[#171717] px-3.5 py-3">
                                    <p class="text-neutral-500">{{ detail.label }}</p>
                                    <p class="mt-1 font-medium text-neutral-200">{{ detail.value }}</p>
                                </div>
                            </div>
                        </div>

                        <footer class="flex justify-end gap-2.5 border-t border-neutral-800 px-5 py-4 sm:px-6">
                            <button
                                type="button"
                                class="rounded-lg border border-[#2a2a2a] px-4 py-2 text-xs text-[#CCCCCC] transition-colors hover:border-white hover:text-white"
                                @click="close"
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                :disabled="!canSave"
                                class="rounded-lg bg-[#C1121F] px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-[#b31a27] disabled:cursor-not-allowed disabled:opacity-50"
                            >
                                Save changes
                            </button>
                        </footer>
                    </form>
                </div>
            </div>
        </Transition>

        <Transition enter-active-class="transition duration-150" leave-active-class="transition duration-100" enter-from-class="opacity-0" leave-to-class="opacity-0">
            <div
                v-if="viewerOpen && activeFile"
                class="fixed inset-0 z-[10000] flex items-center justify-center bg-black/90 p-4 sm:p-8"
                role="dialog"
                aria-modal="true"
                aria-label="Document viewer"
                @click.self="closeViewer"
            >
                <div class="relative flex max-h-full max-w-5xl flex-col items-center">
                    <div class="mb-3 flex w-full items-center justify-between gap-4 text-white">
                        <div>
                            <p class="text-sm font-semibold">{{ viewerTitle }}</p>
                            <p v-if="viewerFiles.length > 1" class="mt-0.5 text-xs text-neutral-400">{{ activeFileIndex + 1 }} of {{ viewerFiles.length }}</p>
                        </div>
                        <button type="button" class="rounded-lg border border-white/15 bg-black/40 p-2 text-white/70 hover:text-white" aria-label="Close image viewer" @click="closeViewer">
                            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" d="M6 6l12 12M18 6 6 18" /></svg>
                        </button>
                    </div>
                    <iframe v-if="isPdfFile(activeFile)" :src="activeFile" title="Selected PDF document" class="h-[75vh] w-[min(90vw,56rem)] rounded-xl bg-white shadow-2xl" />
                    <img v-else :src="activeFile" alt="Selected uploaded document" class="max-h-[78vh] max-w-full rounded-xl object-contain shadow-2xl">
                    <div v-if="viewerFiles.length > 1" class="mt-4 flex gap-2">
                        <button type="button" :disabled="activeFileIndex === 0" :class="viewerButtonClass" @click="activeFileIndex--">Previous</button>
                        <button type="button" :disabled="activeFileIndex === viewerFiles.length - 1" :class="viewerButtonClass" @click="activeFileIndex++">Next</button>
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup lang="ts">
import type { AdminEditUserPayload, User, UserRole } from '~/utils/types/accounts'

const open = defineModel<boolean>({ required: true })
const props = defineProps<{ user: User | null }>()
const emit = defineEmits<{
    save: [payload: { userId: number; body: AdminEditUserPayload }]
}>()
const profileRemovalRequested = ref(false)
const profileRemovalReason = ref('')
const selectedIdFiles = ref<string[]>([])
const idRemovalReason = ref('')
const viewerOpen = ref(false)
const viewerFiles = ref<string[]>([])
const activeFileIndex = ref(0)
const viewerTitle = ref('')

const form = reactive({
    given_name: '',
    family_name: '',
    email: '',
    contact_number: '',
    address: '',
    profile_picture: '',
    role: 'User' as UserRole,
    status: 'Active' as User['status'],
})

const fullName = computed(() => `${form.given_name} ${form.family_name}`.trim())
const initials = computed(() => `${form.given_name[0] ?? ''}${form.family_name[0] ?? ''}`.toUpperCase() || 'U')
const idFiles = computed(() => props.user?.id_images?.images ?? [])
const activeFile = computed(() => viewerFiles.value[activeFileIndex.value] ?? '')
const canSave = computed(() => Boolean(
    props.user &&
    form.email.trim() &&
    (!profileRemovalRequested.value || profileRemovalReason.value.trim()) &&
    (!selectedIdFiles.value.length || idRemovalReason.value.trim())
))
const formattedJoinedDate = computed(() => {
    if (!props.user?.date_joined) return '—'
    return new Date(props.user.date_joined).toLocaleDateString('en-US', {
        month: 'short', day: 'numeric', year: 'numeric',
    })
})
const accountDetails = computed(() => [
    { label: 'Joined', value: formattedJoinedDate.value },
    { label: 'Rentals', value: String(props.user?.rentals ?? 0) },
    { label: 'ID documents', value: String(idFiles.value.length) },
])

watch(
    () => props.user,
    user => {
        if (!user) return
        Object.assign(form, {
            given_name: user.given_name,
            family_name: user.family_name,
            email: user.email,
            contact_number: user.contact_number,
            address: user.address,
            profile_picture: user.profile_picture ?? '',
            role: user.role,
            status: user.status,
        })
        profileRemovalRequested.value = false
        profileRemovalReason.value = ''
        selectedIdFiles.value = []
        idRemovalReason.value = ''
        closeViewer()
    },
    { immediate: true },
)

function close() {
    closeViewer()
    open.value = false
}

function save() {
    if (!props.user || !canSave.value) return

    const body: AdminEditUserPayload = {
        given_name: form.given_name.trim(),
        family_name: form.family_name.trim(),
        email: form.email.trim(),
        contact_number: form.contact_number.trim(),
        address: form.address.trim(),
    }

    if (profileRemovalRequested.value) {
        body.remove_profile_picture = true
        body.profile_removal_reason = profileRemovalReason.value.trim()
    }

    if (selectedIdFiles.value.length) {
        body.remove_id_images = [...selectedIdFiles.value]
        body.id_removal_reason = idRemovalReason.value.trim()
    }

    emit('save', { userId: props.user.id, body })
}

function viewFile(file: string, index: number, title: string, files: string[]) {
    viewerFiles.value = [...files]
    activeFileIndex.value = index
    viewerTitle.value = title
    viewerOpen.value = true
}

function isPdfFile(file: string) {
    const cleanFile = file.split(/[?#]/)[0]?.toLowerCase() ?? ''
    return cleanFile.endsWith('.pdf') || file.toLowerCase().startsWith('data:application/pdf')
}

function fileLabel(file: string, index: number) {
    if (isPdfFile(file)) return `PDF document ${index + 1}`
    return `Image document ${index + 1}`
}

function isIdFileSelected(file: string) {
    return selectedIdFiles.value.includes(file)
}

function toggleIdFileSelection(file: string) {
    if (isIdFileSelected(file)) {
        selectedIdFiles.value = selectedIdFiles.value.filter(selectedFile => selectedFile !== file)
        if (!selectedIdFiles.value.length) idRemovalReason.value = ''
        return
    }

    selectedIdFiles.value = [...selectedIdFiles.value, file]
}

function clearSelectedIdFiles() {
    selectedIdFiles.value = []
    idRemovalReason.value = ''
}

function closeViewer() {
    viewerOpen.value = false
    viewerFiles.value = []
    activeFileIndex.value = 0
}

const labelClass = 'mb-1.5 block text-xs text-neutral-400'
const sectionClass = 'mb-3 text-xs font-semibold uppercase tracking-[0.12em] text-neutral-500'
const fieldClass = 'w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3.5 py-2.5 text-[13px] text-[#e4e4e4] outline-none transition-colors placeholder:text-neutral-600 hover:border-[#3a3a3a] focus:border-[#C1121F]'
const secondaryButtonClass = 'rounded-lg border border-[#343434] px-3 py-2 text-xs text-neutral-300 transition-colors hover:border-neutral-500 hover:text-white'
const removalButtonClass = 'rounded-lg border border-[#5b2429] bg-[#2a1517] px-3 py-2 text-xs text-[#f06a73] transition-colors hover:border-[#C1121F] hover:text-white'
const viewerButtonClass = 'rounded-lg border border-white/15 bg-white/10 px-4 py-2 text-xs text-white transition-colors hover:bg-white/15 disabled:cursor-not-allowed disabled:opacity-30'
</script>
