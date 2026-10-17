
<template>
    <div
        class="bg-[#1a1a1a] border border-[#222] rounded-xl p-5 flex items-center justify-between gap-4"
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

                <span
                    v-else
                    class="text-white text-2xl font-extrabold"
                >
                    {{ props.user?.given_name?.charAt(0) }}
                </span>
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
import type { User } from '~/utils/api/api'

    const props = defineProps<{
        user: User | null
    }>()

    const emit = defineEmits<{
        edit: []
    }>()
</script>