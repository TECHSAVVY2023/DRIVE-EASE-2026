<template>
    <div class="flex items-center px-5 py-4 gap-4">
        <div class="w-14 h-14 rounded-full bg-[#C1121F] flex-shrink-0 overflow-hidden flex items-center justify-center">
            <img
                v-if="props.profilePreview || props.user?.profile_picture"
                :src="props.profilePreview || props.user?.profile_picture || ''"
                alt="Profile"
                class="w-full h-full object-cover"
            />

            <svg v-else class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
            </svg>
        </div>

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


