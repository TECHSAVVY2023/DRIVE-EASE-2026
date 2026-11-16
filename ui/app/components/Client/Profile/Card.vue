
<template>
    <div
        class="smoked-charcoal-panel rounded-xl p-5 flex items-center justify-between gap-4"
    >
        <div class="flex items-center gap-4">
            <!-- Avatar -->
            <UserAvatar
                :src="props.user?.profile_picture"
                :alt="`${props.user?.given_name || ''} ${props.user?.family_name || ''}`.trim()"
                class="h-16 w-16"
            />

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
