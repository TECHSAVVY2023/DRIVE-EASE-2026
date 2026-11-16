<template>
    <div class="flex items-center px-5 py-4 gap-4">
        <UserAvatar
            :src="props.profilePreview || props.user?.profile_picture"
            :alt="`${props.user?.given_name || 'User'} profile picture`"
            class="h-14 w-14"
        />

        <div>
            <p class="text-white font-medium text-sm font-[Poppins]">
                {{ props.user?.given_name }} {{ props.user?.family_name }}
            </p>

            <p class="text-[#929292] text-xs">
                Member since
                {{ props.user?.date_created
                    ? new Date(props.user.date_created).getFullYear()
                    : ''
                }}
            </p>
        </div>

        <button
            type="button"
            @click="triggerProfileUpload"
            class="ml-auto text-white/60 border border-white/20 hover:border-white/40 hover:text-white text-xs px-3 py-1.5 rounded transition-colors"
        >
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
</template>

<script setup lang="ts">
import type { User } from '~/utils/types/accounts'

const props = defineProps<{
    user: User | null
    profilePreview: string | null
}>()

const emit = defineEmits<{
    change: [event: Event]
}>()

const profileInput = ref<HTMLInputElement | null>(null)

const triggerProfileUpload = () => {
    profileInput.value?.click()
}

const handleProfileChange = (event: Event) => {
    emit('change', event)
}
</script>


