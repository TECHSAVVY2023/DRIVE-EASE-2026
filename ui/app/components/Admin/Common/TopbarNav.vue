<template>
    <!-- Top Navbar -->
    <header
        class="
            w-full bg-[#0D0D0D] border-b border-[#1f1f1f]
            px-4 py-4
            flex items-center justify-between
            sm:px-6 lg:px-8
        "
    >
        <!-- Left Side -->
        <div class="flex items-center gap-3 min-w-0 relative z-10">

            <!-- Mobile Menu Button -->
            <button
                @click="handleOpenSidebar"
                class="
                    flex justify-center items-center text-white
                    w-10 h-10 rounded-lg border border-[#2a2a2a]
                    md:hidden hover:border-[#C1121F]
                    transition-colors duration-200
                "
                aria-label="Open sidebar"
            >
                <svg
                    class="w-5 h-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M4 6h16M4 12h16M4 18h16"
                    />
                </svg>
            </button>

            <!-- Breadcrumbs -->
            <nav
                aria-label="Breadcrumb"
                class="flex items-center gap-2 min-w-0"
            >
                <!-- Admin Icon + Label -->
                <div class="flex items-center gap-2 shrink-0">
                    <div
                        class="
                            flex items-center justify-center
                            w-8 h-8 rounded-lg
                            bg-[#C1121F]/15
                            border border-[#C1121F]/30
                        "
                    >
                        <svg
                            class="w-4 h-4 text-[#E63946]"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="1.8"
                                d="M3 10.5 12 3l9 7.5M5.5 9v11h13V9M9 20v-6h6v6"
                            />
                        </svg>
                    </div>

                    <span class="text-gray-300 text-sm font-medium whitespace-nowrap">
                        Admin
                    </span>
                </div>

                <!-- Separator -->
                <svg
                    class="w-4 h-4 text-gray-600 shrink-0"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="m9 18 6-6-6-6"
                    />
                </svg>

                <!-- Current Page -->
                <span
                    class="text-white text-base sm:text-lg font-semibold truncate"
                    aria-current="page"
                >
                    {{ props.title }}
                </span>
            </nav>
        </div>

        <!-- Right Side -->
        <div class="flex items-center gap-2 sm:gap-4">
            <AuthLoading v-if="authLoading" compact />
            <AdminCommonTopbarNavUserMenu
                v-else
                :user="user"
                :logout="logout"
            />
        </div>
    </header>
</template>

<script setup lang="ts">
const { logout } = useAuth()
const { authLoading } = useCurrentUser()

const props = defineProps<{
    user?: {
        given_name?: string
        profile_picture?: string | null
    } | null
    title: string
    subtitle?: string
    isLoggedIn: boolean
}>()

const emit = defineEmits<{
    (e: 'close-sidebar'): void
    (e: 'open-sidebar'): void
}>()

const handleOpenSidebar = (): void => {
    emit('open-sidebar')
}
</script>
