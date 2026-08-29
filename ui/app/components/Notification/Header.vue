<template>
    <div class="flex items-center justify-between gap-3 px-4 sm:px-5 pt-4 sm:pt-5 pb-4 border-b border-[#222]">
        <div class="min-w-0">
            <h2 class="text-white font-extrabold text-base">
                All notifications
            </h2>

            <p class="text-gray-400 text-xs mt-0.5">
                {{ total }} total / {{ unreadCount }} unread
            </p>
        </div>

        <div class="flex items-center gap-2 shrink-0">

            <!-- Mark all as read -->
            <button
                @click="emit('mark-all-read')"
                aria-label="Mark all as read"
                class="
                    hidden sm:inline-flex whitespace-nowrap text-xs 
                    flex item-center gap-1
                    border border-[#333333] hover:border-white text-[#8F8F8F] hover:text-white
                    px-3 py-1.5 rounded-lg transition-colors duration-200"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="w-4 h-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                    />
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                </svg>
                <span>Mark all as read</span>
            </button>
            <button
                @click="emit('mark-all-read')"
                aria-label="Mark all as read"
                class="sm:hidden flex items-center justify-center h-8 w-8 border border-[#2a2a2a] text-gray-400 rounded-lg hover:border-white hover:text-white transition-colors duration-200"
            >
                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                </svg>
            </button>

            <!-- Delete all -->
            <button
                @click="emit('delete-all')"
                aria-label="Delete all"
                class="
                    hidden sm:inline-flex whitespace-nowrap text-xs 
                    flex items-center gap-1
                    border border-[#2a2a2a] hover:border-[#c1121f] hover:text-[#c1121f] text-[#8F8F8F]
                    px-3 py-1.5 rounded-lg transition-colors duration-200
                "
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="w-4 h-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5-3h4m-7 3h10M10 11v6m4-6v6"
                    />
                </svg>

                Delete all
            </button>
            <button
                @click="emit('delete-all')"
                aria-label="Delete all"
                class="sm:hidden flex items-center justify-center h-8 w-8 border border-[#2a2a2a] text-gray-400 rounded-lg hover:border-red-500 hover:text-red-400 transition-colors duration-200"
            >
                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                </svg>
            </button>

        </div>
    </div>
</template>

<script setup lang="ts">
import type { Notification } from '~/utils/api/api'

const props = defineProps<{
    notifications: Notification[]
    total: number
    unreadCount: number
}>()

const emit = defineEmits<{
    'mark-all-read': []
    'delete-all': []
}>()
</script>