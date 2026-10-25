
<template>
    <div
        class="smoked-charcoal-panel rounded-xl p-5 flex items-center justify-between gap-4"
    >
        <div class="flex items-center gap-4">
            <!-- Avatar -->
            <div
                class="w-16 h-16 rounded-full bg-[#C1121F] flex-shrink-0 overflow-hidden flex items-center justify-center"
            >
                <img
                    v-if="props.user?.profile_picture"
                    :src="props.user.profile_picture"
                    :alt="props.user.given_name + ' ' + props.user.family_name"
                    class="w-full h-full object-cover"
                />

                <svg v-else class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                </svg>
            </div>

            <!-- Name + Member since -->
            <div>
                <p class="text-white font-bold text-lg leading-tight">
                    {{ props.user?.given_name }} {{ props.user?.family_name }}
                </p>

                <p class="text-gray-400 text-xs mt-0.5">
                    Member since
                    {{ props.user?.date_created
                        ? new Date(props.user.date_created).getFullYear()
                        : ''
                    }}
                </p>
            </div>
        </div>

        <!-- Edit button -->
        <button
            @click="emit('edit')"
            class="
                bg-[#C1121F] hover:bg-[#9B0E18] rounded-lg
                text-white text-xs font-semibold px-4 py-2
                flex-shrink-0
                transition-colors duration-200
            "
        >
            Edit profile
        </button>
    </div>
</template>

<script setup lang="ts">
import type { User } from '~/utils/types/accounts'

    const props = defineProps<{
        user: User | null
    }>()

    const emit = defineEmits<{
        edit: []
    }>()
</script>
