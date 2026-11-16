<template>
    <div class="space-y-7">
        <ContentSection title="Who we are" description="Company introduction, image, and summary statistics">
            <div class="space-y-4">
                <AdminContentFieldInput id="about-wwr-heading" v-model="form.wwr_heading" label="Section heading" />
                <div>
                    <label for="about-wwr-description" :class="labelClass">Introduction</label>
                    <textarea id="about-wwr-description" v-model="form.wwr_description" rows="5" :class="textareaClass" />
                </div>
                <div class="border-t border-[#262626] pt-4">
                    <label :class="labelClass">Section image</label>

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
                                <p class="mt-0.5 text-[9px] text-[#666]">PNG, JPG, or JPEG</p>
                            </div>
                        </div>

                        <div class="min-w-0 flex-1 sm:max-w-md">
                            <p class="text-[10px] leading-4 text-[#888]">
                                Upload a PNG, JPG, or JPEG image up to 50 MB. Any image dimensions are accepted.
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
                            accept="image/png,image/jpeg,.jpg,.jpeg"
                            class="hidden"
                            @change="handleImageChange"
                        />
                    </div>
                </div>

                <AdminContentEditorList title="Statistics" add-label="+ Add statistic" @add="addStat">
                    <div v-for="(stat, index) in form.wwr_stats" :key="stat.id || `new-${index}`" :class="cardClass">
                        <div class="grid gap-3 sm:grid-cols-2">
                            <AdminContentFieldInput :id="`about-stat-value-${index}`" v-model="stat.value" label="Value" />
                            <AdminContentFieldInput :id="`about-stat-label-${index}`" v-model="stat.stat" label="Label" />
                        </div>
                        <AdminContentRemoveButton @click="form.wwr_stats.splice(index, 1)" />
                    </div>
                </AdminContentEditorList>
            </div>
        </ContentSection>

        <div class="grid gap-7 xl:grid-cols-2">
            <ContentSection title="Our mission" description="Mission statement shown on the About page">
                <AdminContentFieldInput id="mission-heading" v-model="form.mission_heading" label="Heading" />
                <textarea v-model="form.mission_description" rows="5" :class="`${textareaClass} mt-3`" aria-label="Mission statement" />
            </ContentSection>
            <ContentSection title="Our vision" description="Vision statement shown on the About page">
                <AdminContentFieldInput id="vision-heading" v-model="form.vission_heading" label="Heading" />
                <textarea v-model="form.vission_description" rows="5" :class="`${textareaClass} mt-3`" aria-label="Vision statement" />
            </ContentSection>
        </div>

        <ContentSection title="Our team" description="Team members displayed in the About page grid">
            <AdminContentEditorList title="Team members" add-label="+ Add member" @add="addMember">
                <div v-for="(member, index) in form.team" :key="member.id || `new-${index}`" :class="cardClass">
                    <div class="grid gap-3 sm:grid-cols-2">
                        <div>
                            <label :for="`team-user-${index}`" :class="labelClass">Existing user</label>
                            <select
                                :id="`team-user-${index}`"
                                v-model.number="member.user"
                                :class="fieldClass"
                            >
                                <option :value="null">Select a user</option>
                                <option v-for="user in users" :key="user.id" :value="user.id">
                                    {{ user.name }} · {{ user.email }}
                                </option>
                            </select>
                        </div>
                        <AdminContentFieldInput :id="`team-position-${index}`" v-model="member.position" label="Position" />
                        <div>
                            <label :for="`team-description-${index}`" :class="labelClass">Description</label>
                            <textarea :id="`team-description-${index}`" v-model="member.description" rows="2" :class="textareaClass" />
                        </div>
                        <div class="flex items-center gap-3 rounded-lg border border-[#292929] bg-[#0d0d0d] p-3">
                            <UserAvatar
                                :src="selectedUser(member.user)?.profile_picture || ''"
                                :alt="selectedUser(member.user)?.name || 'Selected user'"
                                class="h-10 w-10"
                            >
                                <template #fallback>
                                    <span class="text-xs font-bold text-white">
                                        {{ selectedUser(member.user)?.name?.charAt(0) || '?' }}
                                    </span>
                                </template>
                            </UserAvatar>
                            <div class="min-w-0">
                                <p class="truncate text-xs font-medium text-white">{{ selectedUser(member.user)?.name || 'No user selected' }}</p>
                                <p class="truncate text-[10px] text-[#777]">Profile name and image come from the account.</p>
                            </div>
                        </div>
                    </div>
                    <AdminContentRemoveButton @click="form.team.splice(index, 1)" />
                </div>
            </AdminContentEditorList>
        </ContentSection>

        <ContentSection title="Our journey" description="Timeline milestones displayed near the bottom of the About page">
            <AdminContentEditorList title="Milestones" add-label="+ Add milestone" @add="addMilestone">
                <div v-for="(milestone, index) in form.journey" :key="milestone.id || `new-${index}`" :class="cardClass">
                    <div class="grid gap-3 sm:grid-cols-[120px_1fr]">
                        <AdminContentFieldInput :id="`journey-year-${index}`" v-model="milestone.year" label="Year" />
                        <AdminContentFieldInput :id="`journey-title-${index}`" v-model="milestone.title" label="Title" />
                        <div class="sm:col-span-2">
                            <label :for="`journey-description-${index}`" :class="labelClass">Description</label>
                            <textarea :id="`journey-description-${index}`" v-model="milestone.description" rows="2" :class="textareaClass" />
                        </div>
                    </div>
                    <AdminContentRemoveButton @click="form.journey.splice(index, 1)" />
                </div>
            </AdminContentEditorList>
        </ContentSection>
    </div>
</template>

<script setup lang="ts">
import type {
    AboutTeamUserOption,
    AboutUsPageContent,
} from '~/utils/types/content'

const props = defineProps<{
    form: AboutUsPageContent
    users: AboutTeamUserOption[]
}>()
const emit = defineEmits<{
    'update:newImageFile': [file: File]
}>()

const form = toRef(props, 'form')
const users = toRef(props, 'users')
const { $swal } = useNuxtApp()
const fileInput = ref<HTMLInputElement | null>(null)

const handleImageChange = async (event: Event) => {
    const input = event.target as HTMLInputElement
    const file = input.files?.[0]

    if (file && await validateFile(file)) {
        form.value.wwr_image = URL.createObjectURL(file)
        emit('update:newImageFile', file)
    }

    input.value = ''
}

const validateFile = async (file: File): Promise<boolean> => {
    const MAX_FILE_SIZE = 50 * 1024 * 1024
    const extension = file.name.split('.').pop()?.toLowerCase()

    let message = ''
    let title = 'Invalid File'

    const allowedExtensions = ['png', 'jpg', 'jpeg']
    const allowedTypes = ['image/png', 'image/jpeg']

    if (!extension || !allowedExtensions.includes(extension) || !allowedTypes.includes(file.type)) {
        message = 'Only PNG, JPG, and JPEG images are allowed.'
    } else if (file.size > MAX_FILE_SIZE) {
        title = 'File Too Large'
        message = 'Image size must not exceed 50 MB.'
    } else {
        try {
            const image = await createImageBitmap(file)
            image.close()
        } catch {
            title = 'Invalid Image'
            message = 'The selected file could not be read as an image.'
        }
    }

    if (!message) return true

    await $swal.fire({
        icon: 'error',
        title,
        text: message,
        confirmButtonText: 'OK',
        confirmButtonColor: '#C1121F',
        background: '#1a1a1a',
        color: '#ffffff',
    })
    return false
}

const currentImageName = computed(() => {
    if (!form.value.wwr_image) return 'No image uploaded'

    try {
        const fileName = decodeURIComponent(
            new URL(form.value.wwr_image).pathname.split('/').pop() || 'Current image'
        )
        const lastDotIndex = fileName.lastIndexOf('.')
        if (lastDotIndex === -1) return fileName.length > 25 ? `${fileName.slice(0, 22)}...` : fileName

        const name = fileName.slice(0, lastDotIndex)
        const extension = fileName.slice(lastDotIndex)
        return name.length > 25 ? `${name.slice(0, 22)}...${extension}` : fileName
    } catch {
        const fileName = form.value.wwr_image.split('/').pop() || 'Current image'
        return fileName.length > 25 ? `${fileName.slice(0, 22)}...` : fileName
    }
})

const addStat = () => form.value.wwr_stats.push({ id: 0, stat: '', value: '', order: form.value.wwr_stats.length })
const addMember = () => form.value.team.push({
    id: 0,
    user: null,
    user_name: '',
    user_email: '',
    user_profile_picture: null,
    position: '',
    description: '',
    order: form.value.team.length,
})
const addMilestone = () => form.value.journey.push({ id: 0, year: '', title: '', description: '', order: form.value.journey.length })
const selectedUser = (userId: number | null) =>
    users.value.find(user => user.id === userId)

const fieldClass = 'w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3.5 py-2.5 text-[13px] text-[#d4d4d4] outline-none transition-colors placeholder:text-[#555] focus:border-[#C1121F]'
const textareaClass = `${fieldClass} resize-none leading-5`
const labelClass = 'mb-1.5 block text-[11px] text-neutral-400'
const cardClass = 'relative rounded-lg border border-[#292929] bg-[#111] p-4 pr-16'
const secondaryButtonClass = 'shrink-0 rounded-lg border border-[#343434] bg-[#1b1b1b] px-3 py-2 text-[10px] font-semibold text-[#bbb] transition hover:border-[#C1121F] hover:text-white'
</script>
