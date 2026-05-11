<template>
    <!-- =========================
            Navbar
    ========================== -->
    <nav 
        class="
            sticky top-0 
            flex h-[72px] items-center justify-between 
            px-8 py-4 
            bg-black z-50 
            font-[poppins]
        "
    >
        
        <div class="flex items-center gap-2 ml-8">

            <div class="w-12 h-12 rounded-full overflow-hidden">
                <img
                    src="~/assets/images/logo.png"
                    alt="Logo"
                    class="w-full h-full object-cover"
                />
            </div>

        </div>

        <!-- Desktop Nav Links -->
        <ul class="hidden md:flex items-center gap-10 text-white text-sm font-medium tracking-wide">

            <li><a href="/" class="hover:text-[#c1121f] transition-colors duration-200">Home</a></li>
            <li><a href="#" class="hover:text-[#c1121f] transition-colors duration-200">Fleet</a></li>
            <li><a href="#" class="hover:text-[#c1121f] transition-colors duration-200">About</a></li>
            <li><a href="/contact" class="hover:text-[#c1121f] transition-colors duration-200">Contact</a></li>
        
        </ul>

        <!-- Desktop Login Button -->
        <button
            @click="$router.push('/login')"
            class="
                hidden md:flex
                items-center gap-2

                px-5 py-2
                rounded-full

                border border-[#3C3C3C]
                bg-[#0D0D0D]

                text-sm font-semibold text-white

                hover:border-[#C1121F]
                transition-colors duration-200
            "
        >
            <!-- User Icon -->
            <svg
                xmlns="http://www.w3.org/2000/svg"
                class="w-4 h-4 text-white"
                viewBox="0 0 24 24"
                fill="currentColor"
            >
                <path
                    d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"
                />
            </svg>

            <span>Login</span>
        </button>

        <!-- =========================
                Mobile hamburger
        ========================== -->
        <button 
            @click="emit('toggle-menu')"
            class="md:hidden text-white"
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
    </nav>

</template>

<script setup lang="ts">

const emit = defineEmits<{
    (e: 'toggle-menu'): void
}>()

</script>

