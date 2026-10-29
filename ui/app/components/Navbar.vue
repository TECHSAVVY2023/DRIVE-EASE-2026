<template>
    <!-- =========================
            Navbar
    ========================== -->
    <nav 
        class="
            sticky top-0 z-100 h-[76px]
            border-b border-white/[0.07]
            bg-[#050506]/98 shadow-[0_10px_30px_rgba(0,0,0,0.3)] backdrop-blur-xl
            font-[poppins]
        "
    >
        <div class="mx-auto flex h-full w-full max-w-7xl items-center justify-between px-5 sm:px-8">

        <NuxtLink to="/" class="group flex items-center gap-3" aria-label="Drive Ease home">

            <div class="w-11 h-11 rounded-full overflow-hidden ring-1 ring-white/10 group-hover:ring-[#C1121F]/70 transition-colors">
                <img
                    src="~/assets/images/logo.png"
                    alt="Logo"
                    class="w-full h-full object-cover"
                />
            </div>

            <div class="hidden lg:flex flex-col leading-none">
                <span class="text-white text-sm font-extrabold tracking-wide">DRIVE EASE</span>
                <span class="text-[#85858b] text-[9px] tracking-[0.2em] mt-1">CAR RENTAL</span>
            </div>
        </NuxtLink>

        <!-- Desktop Nav Links -->
        <ul class="hidden md:flex items-center gap-1 rounded-full border border-white/[0.06] bg-white/[0.025] p-1 text-sm font-medium">

            <li v-for="link in navLinks" :key="link.to">
                <NuxtLink
                    :to="link.to"
                    class="block rounded-full px-5 py-2 text-[#a0a0a5] transition-colors duration-200 hover:bg-white/[0.04] hover:text-white"
                    :class="isActiveLink(link.to) ? 'bg-white/[0.07] text-white shadow-sm' : ''"
                >
                    {{ link.label }}
                </NuxtLink>
            </li>
        
        </ul>

        <AuthLoading v-if="authLoading" compact class="hidden md:flex" />

        <div v-else-if="isLoggedIn" class="relative hidden md:block">
        <button
            @click="toggleDropdown"
            type="button"
            :aria-expanded="isDropdownOpen"
            aria-label="Open account menu"
            class="
                relative flex items-center gap-2
                bg-[#151517] border border-white/10 hover:border-[#C1121F]
                text-white text-sm
                pl-2 pr-3 py-2 rounded-full
                transition-colors duration-200
            "
        >
            <!-- Notification Badge -->
            <span
                v-if="unreadCount > 0 && !isDropdownOpen"
                class="
                    absolute -top-1 -right-1
                    min-w-[18px] h-[18px]
                    px-1
                    flex items-center justify-center
                    rounded-full
                    bg-[#C1121F]
                    text-[10px] font-bold text-white
                    leading-none
                    z-10
                "
            >
                {{ unreadCount > 99 ? '99+' : unreadCount }}
            </span>

            <!-- Avatar -->
            <div
                class="w-7 h-7 rounded-full bg-[#c1121f] flex items-center justify-center flex-shrink-0"
            >
                <img
                    v-if="props.user?.profile_picture"
                    :src="props.user?.profile_picture"
                    alt="Profile"
                    class="w-7 h-7 rounded-full object-cover"
                />
                <svg v-else class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                </svg>
            </div>

            <span class="hidden sm:block truncate">
                {{ props.user?.given_name }}
            </span>

            <svg
                class="w-4 h-4 text-gray-400 flex-shrink-0 transition-transform duration-200"
                :class="{ 'rotate-180': isDropdownOpen }"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                />
            </svg>
        </button>

        <!-- Dropdown Menu -->
        <div
            v-if="isDropdownOpen"
            class="
                absolute right-0 top-[calc(100%+0.75rem)] w-64 z-50
                bg-[#0c0c0e]/98 border border-white/10 rounded-2xl shadow-2xl
                overflow-hidden
            "
        >

            <div class="flex items-center gap-3 border-b border-white/[0.08] bg-white/[0.025] px-4 py-4">
                <div class="flex h-10 w-10 shrink-0 items-center justify-center overflow-hidden rounded-full bg-[#c1121f]">
                    <img
                        v-if="props.user?.profile_picture"
                        :src="props.user.profile_picture"
                        alt="Profile"
                        class="h-full w-full object-cover"
                    />
                    <svg v-else class="h-5 w-5 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                    </svg>
                </div>
                <div class="min-w-0">
                    <p class="truncate text-sm font-semibold text-white">{{ props.user?.given_name || 'My account' }}</p>
                    <p class="mt-0.5 text-[11px] text-[#85858b]">Manage your Drive Ease account</p>
                </div>
            </div>

            <!-- Profile -->
            <button
                @click="navigateAccount('/client/profile')"
                class="
                    w-full flex items-center gap-3
                    px-4 py-3
                    text-sm text-[#b0b0b5]
                    hover:bg-white/[0.06]
                    transition-colors duration-200
                "
                :class="route.path.startsWith('/client/profile') ? 'bg-white/[0.06] text-white border-l-2 border-[#C1121F]' : ''"
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-white" fill="currentColor" stroke="currentColor" viewBox="0 0 640 640">
                    <path d="M320 312C386.3 312 440 258.3 440 192C440 125.7 386.3 72 320 72C253.7 72 200 125.7 200 192C200 258.3 253.7 312 320 312zM290.3 368C191.8 368 112 447.8 112 546.3C112 562.7 125.3 576 141.7 576L498.3 576C514.7 576 528 562.7 528 546.3C528 447.8 448.2 368 349.7 368L290.3 368z"/>
                </svg>

                <span>Profile</span>
            </button>

            <!-- Transactions -->
            <button
                @click="navigateAccount('/client/transaction')"
                class="
                    w-full flex items-center gap-3
                    px-4 py-3
                    text-sm text-[#b0b0b5]
                    hover:bg-white/[0.06]
                    transition-colors duration-200
                "
                :class="route.path.startsWith('/client/transaction') ? 'bg-white/[0.06] text-white border-l-2 border-[#C1121F]' : ''"
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 640 640">
                    <path d="M160 96C142.3 96 128 110.3 128 128L128 576L192 544L256 576L320 544L384 576L448 544L512 576L512 128C512 110.3 497.7 96 480 96L160 96zM224 192L416 192C429.3 192 440 202.7 440 216C440 229.3 429.3 240 416 240L224 240C210.7 240 200 229.3 200 216C200 202.7 210.7 192 224 192zM224 288L416 288C429.3 288 440 298.7 440 312C440 325.3 429.3 336 416 336L224 336C210.7 336 200 325.3 200 312C200 298.7 210.7 288 224 288zM224 384L352 384C365.3 384 376 394.7 376 408C376 421.3 365.3 432 352 432L224 432C210.7 432 200 421.3 200 408C200 394.7 210.7 384 224 384z"/>
                </svg>
                
                <span>Transactions</span>
            </button>

            <button
                @click="navigateAccount('/client/notifications')"
                class="
                    w-full flex items-center gap-3
                    px-4 py-3
                    text-sm text-[#b0b0b5]
                    hover:bg-white/[0.06]
                    transition-colors duration-200
                "
                :class="route.path.startsWith('/client/notifications') ? 'bg-white/[0.06] text-white border-l-2 border-[#C1121F]' : ''"
            >
                <div class="relative">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="w-5 h-5 text-white shrink-0"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V4a2 2 0 10-4 0v1.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                        />
                    </svg>

                    <span
                        v-if="unreadCount > 0"
                        class="
                            absolute -top-2 -right-2
                            min-w-[18px] h-[18px]
                            px-1
                            flex items-center justify-center
                            rounded-full
                            bg-[#C1121F]
                            text-[10px] font-bold text-white
                            leading-none
                        "
                    >
                        {{ unreadCount > 99 ? '99+' : unreadCount }}
                    </span>
                </div>

                <span>Notifications</span>
            </button>

            <!-- Divider -->
            <div class="border-t border-[#222222]"></div>

            <!-- Logout -->
            <button
                @click="handleLogout"
                class="
                    w-full px-4 py-3 flex items-center gap-3
                    text-sm text-red-400
                    hover:bg-white/[0.06]
                    transition-colors duration-200
                "
            >
                <svg
                    class="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H6a2 2 0 01-2-2V7a2 2 0 012-2h5a2 2 0 012 2v1"
                    />
                </svg>

                <span>Logout</span>
            </button>

        </div>
        </div>
        
        <button
            v-else
            @click="$router.push('/client/login')"
            class="
                hidden md:flex justify-between items-center gap-3
                bg-[#151517] border border-white/10 hover:border-[#C1121F]
                text-white text-sm
                pl-2 pr-4 py-2 rounded-full
                transition-colors duration-200
            "
        >

            <!-- Avatar -->
            <div class="w-7 h-7 rounded-full bg-[#C1121F] flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                </svg>
            </div>

            <!-- Name -->
            <span class="hidden sm:block truncate">
                Login
            </span>

        </button>

        <!-- =========================
                Mobile hamburger
        ========================== -->
        <button 
            @click="emit('toggle-menu')"
            class="md:hidden flex h-10 w-10 items-center justify-center rounded-lg border border-white/10 bg-white/[0.035] text-white transition hover:border-[#C1121F]"
            aria-label="Open navigation menu"
        >
            <svg xmlns="http://www.w3.org/2000/svg" 
                class="w-7 h-7" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
            >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
        </button>
        </div>
    </nav>

</template>

<script setup lang="ts">
import { ref } from 'vue'
const { logout } = useAuth()
const { authLoading } = useCurrentUser()
const route = useRoute()

const navLinks = [
    { label: 'Home', to: '/' },
    { label: 'Fleet', to: '/client/fleet' },
    { label: 'About', to: '/client/about' },
    { label: 'Contact', to: '/client/contact' },
]

const isActiveLink = (to: string): boolean => {
    if (to === '/') return route.path === '/'
    if (to === '/client/fleet') {
        return route.path.startsWith('/client/fleet') || route.path.startsWith('/client/car-details')
    }
    return route.path.startsWith(to)
}

const props = defineProps<{ 
    user: { 
        given_name?: string 
        profile_picture?: string | null
    } | null,
    isLoggedIn: boolean
    authReady: boolean
}>()

const emit = defineEmits<{
    (e: 'toggle-menu'): void
    (e: 'close-sidebar'): void
    (e: 'open-sidebar'): void
}>()

const isDropdownOpen = ref(false)

const toggleDropdown = (): void => {
    isDropdownOpen.value = !isDropdownOpen.value
}

const navigateAccount = async (path: string): Promise<void> => {
    isDropdownOpen.value = false
    await navigateTo(path)
}

const handleLogout = (): void => {
    isDropdownOpen.value = false
    logout()
}

const { fetchUnreadCount } = useNotification()

const unreadCount = ref(0)

const loadUnreadCount = async () => {
    unreadCount.value = await fetchUnreadCount()
}

watch(
    () => props.isLoggedIn,
    async (loggedIn) => {
        if (loggedIn) {
            await loadUnreadCount()
        } else {
            unreadCount.value = 0
        }
    },
    { immediate: true }
)

</script>


