<template>
    <Transition
        enter-active-class="transition-opacity duration-300"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-200"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
    >
        <div
            v-if="menuOpen"
            class="fixed inset-0 z-[9998] bg-black/75 backdrop-blur-sm md:hidden"
            aria-hidden="true"
            @click="emit('close-menu')"
        />
    </Transition>

    <Transition
        enter-active-class="transition-transform duration-300 ease-out"
        enter-from-class="translate-x-full"
        enter-to-class="translate-x-0"
        leave-active-class="transition-transform duration-250 ease-in"
        leave-from-class="translate-x-0"
        leave-to-class="translate-x-full"
    >
        <aside
            v-if="menuOpen"
            class="fixed inset-y-0 right-0 z-[9999] flex w-[min(88vw,340px)] flex-col border-l border-white/10 bg-[#08080a]/98 shadow-[-24px_0_60px_rgba(0,0,0,0.45)] backdrop-blur-xl md:hidden"
            aria-label="Mobile navigation"
        >
            <header class="flex h-[76px] shrink-0 items-center justify-between border-b border-white/[0.08] px-5">
                <NuxtLink to="/" class="flex items-center gap-3" @click="emit('close-menu')">
                    <img src="~/assets/images/logo.png" alt="Drive Ease" class="h-10 w-10 rounded-full object-cover ring-1 ring-white/10" />
                    <div class="flex flex-col leading-none">
                        <span class="text-sm font-extrabold tracking-wide text-white">DRIVE EASE</span>
                        <span class="mt-1 text-[9px] tracking-[0.2em] text-[#85858b]">CAR RENTAL</span>
                    </div>
                </NuxtLink>

                <button
                    type="button"
                    class="flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 bg-white/[0.035] text-white transition hover:border-[#C1121F] hover:bg-white/[0.06]"
                    aria-label="Close navigation menu"
                    @click="emit('close-menu')"
                >
                    <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18 18 6M6 6l12 12" />
                    </svg>
                </button>
            </header>

            <div class="flex-1 overflow-y-auto px-5 py-5">
                <AuthLoading
                    v-if="authLoading"
                    message="Loading your account..."
                    class="mb-6 min-h-20 rounded-2xl border border-white/[0.08] bg-white/[0.035]"
                />

                <button
                    v-else
                    type="button"
                    class="mb-6 flex w-full items-center gap-3 rounded-2xl border border-white/[0.08] bg-white/[0.035] p-4 text-left transition hover:border-[#C1121F]/60 hover:bg-white/[0.055]"
                    @click="navigateToAccount"
                >
                    <div class="flex h-12 w-12 shrink-0 items-center justify-center overflow-hidden rounded-full bg-[#242427] ring-1 ring-white/10">
                        <img
                            v-if="user?.profile_picture"
                            :src="user.profile_picture"
                            alt="Profile"
                            class="h-full w-full object-cover"
                        />
                        <svg v-else class="h-6 w-6 text-white/75" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
                        </svg>
                    </div>

                    <div class="min-w-0 flex-1">
                        <p class="truncate text-sm font-semibold text-white">
                            {{ isLoggedIn ? (user?.given_name || 'My account') : 'Welcome to Drive Ease' }}
                        </p>
                        <p class="mt-1 text-xs text-[#85858b]">
                            {{ isLoggedIn ? 'View and manage your profile' : 'Sign in to rent a vehicle' }}
                        </p>
                    </div>

                    <svg class="h-4 w-4 shrink-0 text-[#85858b]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m9 5 7 7-7 7" />
                    </svg>
                </button>

                <nav aria-label="Primary navigation">
                    <p class="mb-2 px-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-[#66666d]">Explore</p>
                    <ul class="flex flex-col gap-1">
                        <li v-for="link in navLinks" :key="link.to">
                            <NuxtLink
                                :to="link.to"
                                class="flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium transition-colors"
                                :class="isActiveLink(link.to)
                                    ? 'bg-white/[0.07] text-white'
                                    : 'text-[#a0a0a5] hover:bg-white/[0.045] hover:text-white'"
                                @click="emit('close-menu')"
                            >
                                <span
                                    class="flex h-9 w-9 items-center justify-center rounded-lg border transition-colors"
                                    :class="isActiveLink(link.to)
                                        ? 'border-[#C1121F]/50 bg-[#C1121F]/15 text-[#e53a47]'
                                        : 'border-white/[0.07] bg-white/[0.025] text-[#85858b]'"
                                >
                                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" :d="link.icon" />
                                    </svg>
                                </span>
                                <span>{{ link.label }}</span>
                                <span v-if="isActiveLink(link.to)" class="ml-auto h-1.5 w-1.5 rounded-full bg-[#C1121F]"></span>
                            </NuxtLink>
                        </li>
                    </ul>
                </nav>

                <nav v-if="isLoggedIn" class="mt-6 border-t border-white/[0.08] pt-5" aria-label="Account navigation">
                    <p class="mb-2 px-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-[#66666d]">My account</p>
                    <ul class="flex flex-col gap-1">
                        <li v-for="link in accountLinks" :key="link.to">
                            <NuxtLink
                                :to="link.to"
                                class="flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium transition-colors"
                                :class="route.path.startsWith(link.to)
                                    ? 'bg-white/[0.07] text-white'
                                    : 'text-[#a0a0a5] hover:bg-white/[0.045] hover:text-white'"
                                @click="emit('close-menu')"
                            >
                                <span class="flex h-9 w-9 items-center justify-center rounded-lg border border-white/[0.07] bg-white/[0.025] text-[#85858b]">
                                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" :d="link.icon" />
                                    </svg>
                                </span>
                                <span>{{ link.label }}</span>
                                <span
                                    v-if="link.to === '/client/notifications' && unreadCount > 0"
                                    class="ml-auto min-w-5 rounded-full bg-[#C1121F] px-1.5 py-0.5 text-center text-[10px] font-bold text-white"
                                >
                                    {{ unreadCount > 99 ? '99+' : unreadCount }}
                                </span>
                            </NuxtLink>
                        </li>
                    </ul>
                </nav>
            </div>

            <footer class="shrink-0 border-t border-white/[0.08] p-5">
                <AuthLoading v-if="authLoading" compact />

                <button
                    v-else-if="isLoggedIn"
                    type="button"
                    class="flex w-full items-center justify-center gap-2 rounded-xl border border-red-500/20 bg-red-500/[0.06] px-4 py-3 text-sm font-semibold text-red-400 transition hover:border-red-500/40 hover:bg-red-500/10"
                    @click="handleLogout"
                >
                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0-4-4m4 4H7m6 4v1a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h5a2 2 0 0 1 2 2v1" />
                    </svg>
                    Log out
                </button>

                <button
                    v-else
                    type="button"
                    class="w-full rounded-xl bg-[#C1121F] px-4 py-3 text-sm font-semibold text-white transition hover:bg-[#9B0E18]"
                    @click="navigate('/client/login')"
                >
                    Sign in
                </button>
            </footer>
        </aside>
    </Transition>
</template>

<script setup lang="ts">
const props = defineProps<{
    menuOpen: boolean
}>()

const emit = defineEmits<{
    (e: 'close-menu'): void
}>()

const { logout, isLoggedIn } = useAuth()
const { user, authLoading } = useCurrentUser()
const { fetchUnreadCount } = useNotification()
const route = useRoute()
const unreadCount = ref(0)

const navLinks = [
    { label: 'Home', to: '/', icon: 'M3 11.5 12 4l9 7.5M5.5 10v9.5h13V10M9.5 19.5v-6h5v6' },
    { label: 'Fleet', to: '/client/fleet', icon: 'M5 17h14M6.5 17v2M17.5 17v2M4 13l1.5-5h13l1.5 5v4H4v-4Zm2.5 1h.01M17.5 14h.01' },
    { label: 'About', to: '/client/about', icon: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm0-10v6m0-10h.01' },
    { label: 'Contact', to: '/client/contact', icon: 'M4 5h16v14H4V5Zm0 2 8 6 8-6' },
]

const accountLinks = [
    { label: 'Profile', to: '/client/profile', icon: 'M20 21a8 8 0 0 0-16 0m8-10a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z' },
    { label: 'Transactions', to: '/client/transaction', icon: 'M6 3h12v18l-3-2-3 2-3-2-3 2V3Zm3 5h6m-6 4h6' },
    { label: 'Notifications', to: '/client/notifications', icon: 'M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9Zm-8 12h4' },
]

const isActiveLink = (to: string): boolean => {
    if (to === '/') return route.path === '/'
    if (to === '/client/fleet') {
        return route.path.startsWith('/client/fleet') || route.path.startsWith('/client/car-details')
    }
    return route.path.startsWith(to)
}

const navigate = async (path: string): Promise<void> => {
    emit('close-menu')
    await navigateTo(path)
}

const navigateToAccount = (): void => {
    navigate(isLoggedIn.value ? '/client/profile' : '/client/login')
}

const handleLogout = (): void => {
    emit('close-menu')
    logout()
}

const handleEscape = (event: KeyboardEvent): void => {
    if (event.key === 'Escape' && props.menuOpen) emit('close-menu')
}

watch(
    isLoggedIn,
    async (loggedIn) => {
        unreadCount.value = loggedIn ? await fetchUnreadCount() : 0
    },
    { immediate: true }
)

watch(
    () => props.menuOpen,
    (isOpen) => {
        if (import.meta.client) document.body.style.overflow = isOpen ? 'hidden' : ''
    }
)

onMounted(() => window.addEventListener('keydown', handleEscape))

onBeforeUnmount(() => {
    window.removeEventListener('keydown', handleEscape)
    document.body.style.overflow = ''
})
</script>
