<template>
    <Teleport to="body">
        <Transition
            enter-active-class="transition duration-150"
            leave-active-class="transition duration-100"
            enter-from-class="opacity-0"
            leave-to-class="opacity-0"
        >
            <div
                v-if="open"
                class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 p-4"
                @click.self="close"
            >
                <div
                    class="w-full max-w-md overflow-hidden rounded-2xl border-t-5 border-t-[#C1121F] bg-[#111111]"
                    role="dialog"
                    aria-modal="true"
                    aria-labelledby="assign-role-title"
                >
                    <header class="flex items-start justify-between border-b border-white/10 px-6 py-5">
                        <div>
                            <h2
                                id="assign-role-title"
                                class="text-lg font-extrabold text-white"
                            >
                                Assign user role
                            </h2>

                            <p class="mt-1 text-xs text-[#929292]">
                                Select a user and assign their account role
                            </p>
                        </div>

                        <button
                            type="button"
                            class="mt-0.5 text-white/40 transition-colors hover:text-white"
                            aria-label="Close modal"
                            @click="close"
                        >
                            <svg
                                class="h-4 w-4"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                            >
                                <path
                                    stroke-linecap="round"
                                    d="M6 6l12 12M18 6 6 18"
                                />
                            </svg>
                        </button>
                    </header>

                    <form @submit.prevent="save">
                        <div class="space-y-5 px-6 py-5">
                            <div>
                                <label
                                    for="role-user"
                                    class="mb-1.5 block text-xs text-neutral-400"
                                >
                                    User
                                </label>

                                <div class="relative">
                                    <select
                                        id="role-user"
                                        v-model.number="selectedUserId"
                                        :class="fieldClass"
                                        required
                                    >
                                        <option :value="null" disabled>
                                            Select a user
                                        </option>

                                        <option
                                            v-for="account in users"
                                            :key="account.id"
                                            :value="account.id"
                                        >
                                            {{ account.given_name }}
                                            {{ account.family_name }}
                                            — {{ account.email }}
                                        </option>
                                    </select>
                                    <svg
                                        class="pointer-events-none absolute right-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-[#8a8a8a]"
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

                            <div>
                                <label
                                    for="account-role"
                                    class="mb-1.5 block text-xs text-neutral-400"
                                >
                                    Role
                                </label>

                                <div class="relative">
                                    <select
                                        id="account-role"
                                        v-model="selectedRole"
                                        :class="fieldClass"
                                        required
                                    >
                                        <option value="" disabled>
                                            Select a role
                                        </option>

                                        <option value="User">User</option>
                                        <option value="Admin">Admin</option>
                                        <option value="Super Admin">
                                            Super Admin
                                        </option>
                                    </select>
                                    <svg
                                        class="pointer-events-none absolute right-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-[#8a8a8a]"
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

                            <div
                                v-if="selectedUser"
                                class="rounded-xl border border-[#2a2a2a] bg-[#0f0f0f] p-4"
                            >
                                <p class="text-sm font-semibold text-white">
                                    {{ selectedUser.given_name }}
                                    {{ selectedUser.family_name }}
                                </p>

                                <p class="mt-1 text-xs text-neutral-500">
                                    Current role: {{ selectedUser.role }}
                                </p>
                            </div>

                        </div>

                        <footer class="flex justify-end gap-2.5 border-t border-neutral-800 px-5 py-4">
                            <button
                                type="button"
                                class="rounded-lg border border-[#2a2a2a] px-4 py-2 text-xs text-[#CCCCCC] transition-colors hover:border-white hover:text-white"
                                @click="close"
                            >
                                Cancel
                            </button>

                            <button
                                type="submit"
                                :disabled="!canSave"
                                class="rounded-lg bg-[#C1121F] px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-[#b31a27] disabled:cursor-not-allowed disabled:opacity-50"
                            >
                                Save changes
                            </button>
                        </footer>
                    </form>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup lang="ts">
import type { User, UserRole } from "~/utils/types/accounts"

const open = defineModel<boolean>({ required: true })

const props = defineProps<{
    users: User[]
    user: User | null
}>()

const emit = defineEmits<{
    save: [payload: { userId: number; role: UserRole }]
}>()

const selectedUserId = ref<number | null>(null)
const selectedRole = ref<UserRole | "">("")

const selectedUser = computed(() =>
    props.users.find(
        account => account.id === selectedUserId.value
    )
)

const canSave = computed(() =>
    selectedUserId.value !== null &&
    selectedRole.value !== "" &&
    selectedRole.value !== selectedUser.value?.role
)

watch(selectedUser, account => {
    selectedRole.value = account?.role ?? ""
})

watch(
    () => [open.value, props.user] as const,
    ([isOpen, user]) => {
        if (isOpen && user) {
            selectedUserId.value = user.id
            selectedRole.value = user.role
            return
        }

        if (!isOpen) {
            selectedUserId.value = null
            selectedRole.value = ""
        }
    },
    { immediate: true },
)

function close() {
    open.value = false
}

function save() {
    if (!canSave.value || selectedUserId.value === null) return

    emit("save", {
        userId: selectedUserId.value,
        role: selectedRole.value as UserRole,
    })
}

const fieldClass = `
    appearance-none w-full rounded-lg
    border border-[#2a2a2a]
    bg-[#0f0f0f]
    pl-3.5 pr-9 py-2
    text-[13px] text-[#c8c8c8]
    cursor-pointer outline-none
    hover:border-[#C1121F]
    focus:border-[#C1121F]
    transition-colors
`
</script>
