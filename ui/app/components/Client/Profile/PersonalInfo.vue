<template>
    <div
        class="bg-[#1a1a1a] border border-[#222] rounded-xl p-5 flex flex-col gap-4"
    >
        <h3 class="text-white font-bold text-base">
            Personal information
        </h3>

        <div class="border-b border-[#323232] w-full"></div>

        <div class="grid grid-cols-2 gap-4">
            <!-- First name -->
            <div class="flex flex-col gap-1">
                <span class="text-[#9E9E9E] text-xs">
                    First name
                </span>

                <span class="text-white text-sm">
                    {{ props.user?.given_name || '—' }}
                </span>
            </div>

            <!-- Last name -->
            <div class="flex flex-col gap-1">
                <span class="text-[#9E9E9E] text-xs">
                    Last name
                </span>

                <span class="text-white text-sm">
                    {{ props.user?.family_name || '—' }}
                </span>
            </div>

            <!-- Email -->
            <div class="flex flex-col gap-1">
                <span class="text-[#9E9E9E] text-xs">
                    Email address
                </span>

                <span class="text-white text-sm">
                    {{ props.user?.email || '—' }}
                </span>
            </div>

            <!-- Contact -->
            <div class="flex flex-col gap-1">
                <span class="text-[#9E9E9E] text-xs">
                    Contact number
                </span>

                <span class="text-white text-sm">
                    {{ props.user?.contact_number || '—' }}
                </span>
            </div>
        </div>

        <!-- Address -->
        <div class="flex flex-col gap-1">
            <span class="text-gray-500 text-xs">
                Address
            </span>

            <span class="text-white text-sm">
                {{ props.user?.address || '—' }}
            </span>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { User } from '~/utils/api/api'

const props = defineProps<{
    user: User | null
}>()

</script>
