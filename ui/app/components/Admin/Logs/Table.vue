<template>
    <div class="bg-[#161616] border border-[#232323] rounded-xl overflow-hidden">
        
        <!-- Header / Filters -->
        <div
            class="
                flex justify-between items-center
                px-4 sm:px-5
                py-4 sm:py-[18px]
                border-b border-[#232323]
                gap-3 sm:gap-4
                flex-wrap
            "
        >
            <h3 class="text-base font-bold text-white">
                All activity logs
            </h3>

            <div class="flex flex-wrap sm:flex-nowrap md:justify-evenly gap-2 w-full max-w-[600px] sm:w-full">

                <!-- Search -->
                <input
                    :value="props.search"
                    @input="handleSearch"
                    placeholder="Search activity logs..."
                    class="
                        bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg px-3.5 py-[9px] text-[13px]
                        text-[#e4e4e4] placeholder-[#8a8a8a] w-full outline-none
                        focus:border-[#C1121F] transition-colors
                    "
                />

                <!-- Action Filter -->
                <div class="relative flex-1 sm:flex-none">
                    <select
                        :value="props.selectedAction"
                        @change="handleActionChange"
                        class="
                            appearance-none w-full sm:w-auto
                            bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg
                            pl-3.5 pr-9 py-2 text-[13px]
                            text-[#c8c8c8] cursor-pointer outline-none
                            hover:border-[#C1121F] focus:border-[#C1121F]
                            transition-colors
                        "
                    >
                        <option value="">All actions</option>
                        <option value="create">Created</option>
                        <option value="update">Updated</option>
                        <option value="delete">Deleted</option>
                        <option value="status_change">Status changed</option>
                    </select>

                    <svg
                        class="absolute right-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#8a8a8a] pointer-events-none"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <path d="m6 9 6 6 6-6" />
                    </svg>
                </div>

                <!-- Sort Filter -->
                <div class="relative flex-1 sm:flex-none">
                    <select
                        :value="props.selectedSort"
                        @change="handleSortChange"
                        class="
                            appearance-none w-full sm:w-auto
                            bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg
                            pl-3.5 pr-9 py-2 text-[13px]
                            text-[#c8c8c8] cursor-pointer outline-none
                            hover:border-[#C1121F] focus:border-[#C1121F]
                            transition-colors
                        "
                    >   
                        <option value="newest">Newest first</option>
                        <option value="oldest">Oldest first</option>
                    </select>

                    <svg
                        class="absolute right-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[#8a8a8a] pointer-events-none"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <path d="m6 9 6 6 6-6" />
                    </svg>
                </div>

            </div>
        </div>

        <!-- Table scroll container -->
        <div class="table-scroll w-full overflow-x-auto">
            <table class="w-full min-w-[1050px] border-collapse">

                <thead class="bg-[#0f0f0f]">
                    <tr
                        class="
                            text-left text-[12px]
                            text-[#8a8a8a]
                            uppercase tracking-wide
                            font-semibold
                            border-b border-[#232323]
                        "
                    >
                        <th class="px-5 py-3">Administrator</th>
                        <th class="px-5 py-3">Action</th>
                        <th class="px-5 py-3">Description</th>
                        <th class="px-5 py-3">Target</th>
                        <th class="px-5 py-3">Date &amp; Time</th>
                    </tr>
                </thead>

                <tbody>
                    <tr
                        v-for="(log, i) in props.logs"
                        :key="log.id"
                        :class="
                            i !== props.logs.length - 1
                                ? 'border-b border-[#1c1c1c]'
                                : ''
                        "
                    >
                        <!-- Administrator -->
                        <td class="px-5 py-3.5 text-sm">
                            <div class="flex items-center gap-3">

                                <UserAvatar
                                    :src="log.admin_profile_picture"
                                    :alt="`${log.admin_name || 'Admin'} profile picture`"
                                    class="h-7 w-7"
                                />

                                <!-- Administrator Details -->
                                <div class="min-w-0">
                                    <p class="truncate text-sm font-semibold text-white">
                                        {{ log.admin_name || 'Deleted administrator' }}
                                    </p>

                                    <p class="mt-0.5 max-w-[170px] truncate text-xs text-[#666]">
                                        {{ log.admin_reference || 'Deleted administrator' }}
                                    </p>
                                </div>

                            </div>
                        </td>

                        <!-- Action -->
                        <td class="px-5 py-3.5 text-sm">
                        <span
                            class="
                                inline-flex items-center gap-2
                                rounded-md px-2.5 py-1
                                text-xs capitalize whitespace-nowrap
                            "
                            :class="actionClass(log.action)"
                        >
                            <span
                                class="w-1.5 h-1.5 rounded-full"
                                :class="actionDotClass(log.action)"
                            ></span>

                            {{ actionLabel(log.action) }}
                        </span>
                        </td>

                        <!-- Description -->
                        <td class="px-5 py-3.5 text-sm max-w-[320px]">
                            <p class="text-[#c8c8c8] line-clamp-2 break-words">
                                {{ log.description }}
                            </p>
                        </td>

                        <!-- Target -->
                        <td class="px-5 py-3.5 text-sm text-[#e4e4e4]">
                            <div class="font-medium capitalize">
                                {{ formatTargetType(log.target_type) }}
                            </div>
                            <p v-if="log.target_id" class="mt-0.5 text-xs text-[#666]">
                                ID: {{ log.target_id }}
                            </p>
                        </td>

                        <!-- Date -->
                        <td
                            class="
                                px-5 py-3.5 text-sm text-[#8a8a8a]
                                whitespace-nowrap
                            "
                        >
                            <div>{{ new Date(log.created_at).toLocaleString() }}</div>
                            <p class="mt-0.5 text-xs text-[#666]">{{ log.log_reference }}</p>
                        </td>

                    </tr>

                    <!-- Empty state -->
                    <tr v-if="props.logs.length === 0">
                        <td
                            colspan="7"
                            class="
                                px-5 py-10 text-center
                                text-sm text-[#8a8a8a]
                            "
                        >
                            No activity logs found.
                        </td>
                    </tr>
                </tbody>

            </table>
        </div>

        <!-- Pagination -->
        <div
            class="
                flex justify-between items-center
                px-5 py-4
                text-[#8a8a8a] text-[13px]
            "
        >
            <span>
                Showing
                {{
                    props.logs.length
                        ? (props.currentPage - 1) * props.pageSize + 1
                        : 0
                }}
                –
                {{
                    Math.min(
                        props.currentPage * props.pageSize,
                        props.count
                    )
                }}
                of {{ props.count }} logs
            </span>

            <div class="flex gap-1.5">

                <!-- Previous -->
                <button
                    type="button"
                    :disabled="!props.previousPage"
                    @click="
                        emit(
                            'update:page',
                            props.currentPage - 1
                        )
                    "
                    class="
                        w-7 h-7 flex items-center justify-center
                        rounded-md border border-[#2a2a2a]
                    "
                    :class="
                        props.previousPage
                            ? 'cursor-pointer hover:bg-[#222]'
                            : 'opacity-40 cursor-not-allowed'
                    "
                >
                    ‹
                </button>

                <!-- Pages -->
                <button
                    v-for="p in props.totalPages"
                    :key="p"
                    type="button"
                    @click="emit('update:page', p)"
                    class="
                        w-7 h-7 flex items-center justify-center
                        rounded-md border
                    "
                    :class="
                        p === props.currentPage
                            ? 'bg-[#c81e2c] border-[#c81e2c] text-white'
                            : 'border-[#2a2a2a] hover:bg-[#222]'
                    "
                >
                    {{ p }}
                </button>

                <!-- Next -->
                <button
                    type="button"
                    :disabled="!props.nextPage"
                    @click="
                        emit(
                            'update:page',
                            props.currentPage + 1
                        )
                    "
                    class="
                        w-7 h-7 flex items-center justify-center
                        rounded-md border border-[#2a2a2a]
                    "
                    :class="
                        props.nextPage
                            ? 'cursor-pointer hover:bg-[#222]'
                            : 'opacity-40 cursor-not-allowed'
                    "
                >
                    ›
                </button>

            </div>
        </div>

    </div>
</template>

<script setup lang="ts">
import type { AdminActivityLog } from '~/utils/types/logs'

const props = defineProps<{
    logs: AdminActivityLog[]
    search: string
    currentPage: number
    count: number
    pageSize: number
    totalPages: number
    nextPage: string | null
    previousPage: string | null
    selectedAction: string
    selectedSort: string
}>()

const emit = defineEmits<{
    'update:page': [value: number]
    'update:search': [value: string]
    'update:selected-action': [value: string]
    'update:selected-sort': [value: string]
}>()

const actionLabel = (action: AdminActivityLog['action']) => ({
    create: 'Created',
    update: 'Updated',
    delete: 'Deleted',
    status_change: 'Status changed',
}[action])

const actionClass = (action: AdminActivityLog['action']) => ({
    create: 'bg-[#3ddc78]/10 text-[#3ddc78]',
    update: 'bg-blue-500/10 text-blue-400',
    delete: 'bg-[#c81e2c]/10 text-[#f87171]',
    status_change: 'bg-[#e6a23c]/10 text-[#e6a23c]',
}[action])

const actionDotClass = (action: AdminActivityLog['action']) => ({
    create: 'bg-[#3ddc78]',
    update: 'bg-blue-400',
    delete: 'bg-[#c81e2c]',
    status_change: 'bg-[#e6a23c]',
}[action])

const formatTargetType = (value: string) => value ? value.replace(/_/g, ' ') : 'System'

const handleSearch = (event: Event) => {
    emit('update:search', (event.target as HTMLInputElement).value)
}

const handleActionChange = (event: Event) => {
    emit('update:selected-action', (event.target as HTMLSelectElement).value)
}

const handleSortChange = (event: Event) => {
    emit('update:selected-sort', (event.target as HTMLSelectElement).value)
}

</script>
