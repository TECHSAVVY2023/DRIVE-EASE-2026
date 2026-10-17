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
                All users
            </h3>

            <div class="flex flex-wrap sm:flex-nowrap md:justify-evenly gap-2 w-full max-w-[600px] sm:w-full">

                <!-- Search -->
                <input
                    :value="props.search"
                    @input="handleSearch"
                    placeholder="Search users..."
                    class="
                        bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg px-3.5 py-[9px] text-[13px] 
                        text-[#e4e4e4] placeholder-[#8a8a8a] w-full outline-none
                        focus:border-[#C1121F] transition-colors
                    "
                />

                <!-- Role filter -->
                <div class="relative flex-1 sm:flex-none">
                    <select
                        :value="props.selectedRole"
                        @change="handleRoleChange"
                        class="
                            appearance-none w-full sm:w-auto
                            bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg
                            pl-3.5 pr-9 py-2 text-[13px]
                            text-[#c8c8c8] cursor-pointer outline-none
                            hover:border-[#C1121F] focus:border-[#C1121F]
                            transition-colors
                        "
                    >
                        <option value="">Role</option>
                        <option value="Super Admin">Super Admin</option>
                        <option value="Admin">Admin</option>
                        <option value="User">User</option>
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

                <!-- Status filter -->
                <div class="relative flex-1 sm:flex-none">
                    <select
                        :value="props.selectedStatus"
                        @change="handleStatusChange"
                        class="
                            appearance-none w-full sm:w-auto
                            bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg
                            pl-3.5 pr-9 py-2 text-[13px]
                            text-[#c8c8c8] cursor-pointer outline-none
                            hover:border-[#C1121F] focus:border-[#C1121F]
                            transition-colors
                        "
                    >
                        <option value="">Status</option>
                        <option value="Active">Active</option>
                        <option value="Suspended">Suspended</option>
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
            <table class="w-full min-w-[800px] border-collapse">

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
                        <th class="px-5 py-3">User</th>
                        <th class="px-5 py-3">Role</th>
                        <th class="px-5 py-3">Status</th>
                        <th class="px-5 py-3">Joined</th>
                        <th class="px-5 py-3">Rentals</th>
                        <th class="px-5 py-3">Actions</th>
                    </tr>
                </thead>

                <tbody>
                    <tr
                        v-for="(user, i) in props.users"
                        :key="user.email"
                        :class="i !== props.users.length - 1
                            ? 'border-b border-[#1c1c1c]'
                            : ''"
                    >
                        <!-- User -->
                        <td class="px-5 py-3.5 text-sm text-[#e4e4e4]">
                            <div class="flex items-center gap-2.5">
                                <div
                                    v-if="user.profile_picture"
                                    class="w-8 h-8 rounded-full bg-[#2a2a2a]
                                        flex items-center justify-center flex-shrink-0 overflow-hidden"
                                >
                                    <img
                                        :src="user.profile_picture"
                                        :alt="`${user.given_name} ${user.family_name}`"
                                        class="w-full h-full object-cover"
                                    />
                                </div>

                                <div
                                    v-else
                                    class="w-7 h-7 rounded-full bg-[#C1121F]
                                        flex items-center justify-center flex-shrink-0"
                                >
                                    <svg
                                        class="w-4 h-4 text-white"
                                        fill="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4
                                            7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6
                                            1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"
                                        />
                                    </svg>
                                </div>

                                <div class="min-w-0">
                                    <div class="font-semibold text-white truncate">
                                        {{ user.given_name }} {{ user.family_name }}
                                    </div>

                                    <div class="text-[#8a8a8a] text-[12.5px]
                                        truncate max-w-[220px]"
                                    >
                                        {{ user.email }}
                                    </div>
                                </div>
                            </div>
                        </td>

                        <!-- Role -->
                        <td class="px-5 py-3.5 text-sm">
                            <span
                                class="text-xs px-2.5 py-1 rounded-md bg-[#232323]
                                    text-[#c8c8c8] inline-block whitespace-nowrap"
                            >
                                {{ user.role }}
                            </span>
                        </td>

                        <!-- Status -->
                        <td class="px-5 py-3.5 text-sm">
                            <span
                                class="flex items-center gap-[7px] text-[13px] whitespace-nowrap"
                            >
                                <span
                                    class="w-[7px] h-[7px] rounded-full flex-shrink-0"
                                    :class="{
                                        'bg-[#3ddc78]': user.status === 'Active',
                                        'bg-[#c81e2c]': user.status === 'Suspended'
                                    }"
                                ></span>
                                {{ user.status }}
                            </span>
                        </td>

                        <!-- Joined -->
                        <td class="px-5 py-3.5 text-sm text-[#e4e4e4] whitespace-nowrap">
                            {{ formatDate(user.date_joined) }}
                        </td>

                        <!-- Rentals -->
                        <td class="px-5 py-3.5 text-sm text-[#e4e4e4]">
                            {{ user.rentals }}
                        </td>

                        <!-- Actions -->
                        <td class="px-5 py-3.5 text-sm">
                            <div class="flex items-center gap-3 text-[#8a8a8a]">
                                <button
                                    type="button"
                                    class="cursor-pointer hover:text-[#c1121f]"
                                    @click="handleEdit(user)"
                                >
                                    Edit
                                </button>

                                <button
                                    type="button"
                                    class="cursor-pointer hover:text-[#c1121f]"
                                    @click="handleSecondaryAction(user)"
                                >
                                    {{ user.status === 'Active' ? 'Suspend' : 'Activate' }}
                                </button>
                            </div>
                        </td>
                    </tr>

                    <!-- Empty state -->
                    <tr v-if="props.users.length === 0">
                        <td
                            colspan="6"
                            class="px-5 py-10 text-center text-sm text-[#8a8a8a]"
                        >
                            No users found.
                        </td>
                    </tr>
                </tbody>

            </table>
        </div>

        <div class="flex justify-between items-center px-5 py-4 text-[#8a8a8a] text-[13px]">
            <span>
                Showing
                {{ props.users.length ? (props.currentPage - 1) * props.pageSize + 1 : 0 }}
                –
                {{ Math.min(props.currentPage * props.pageSize, props.count) }}
                of {{ props.count }} users
            </span>

            <div class="flex gap-1.5">
                <!-- Previous -->
                <button
                    type="button"
                    :disabled="!props.previousPage"
                    @click="emit('update:page', props.currentPage - 1)"
                    class="w-7 h-7 flex items-center justify-center rounded-md border border-[#2a2a2a]"
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
                    class="w-7 h-7 flex items-center justify-center rounded-md border"
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
                    @click="emit('update:page', props.currentPage + 1)"
                    class="w-7 h-7 flex items-center justify-center rounded-md border border-[#2a2a2a]"
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
import type { User } from '~/utils/api/api'

const props = defineProps<{
    users: User[]
    search: string
    currentPage: number
    count: number
    pageSize: number
    totalPages: number
    nextPage: string | null
    previousPage: string | null
    selectedRole: string
    selectedStatus: string
}>()

const emit = defineEmits<{
    'update:search': [value: string]
    'update:page': [value: number]
    'update:selectedRole': [value: string]
    'update:selectedStatus': [value: string]
    edit: [user: User]
    secondaryAction: [user: User]
}>()

const handleSearch = (event: Event) => {
    const target = event.target as HTMLInputElement
    emit('update:search', target.value)
}

const handleEdit = (user: User) => {
    emit('edit', user)
}

const handleSecondaryAction = (user: User) => {
    emit('secondaryAction', user)
}

const handleRoleChange = (event: Event) => {
    const target = event.target as HTMLSelectElement

    emit('update:selectedRole', target.value)
}

const handleStatusChange = (event: Event) => {
    const target = event.target as HTMLSelectElement

    emit('update:selectedStatus', target.value)
}

const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
    })
}
</script>