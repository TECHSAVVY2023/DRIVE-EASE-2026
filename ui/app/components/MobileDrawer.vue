<template>
    <!-- Backdrop -->
    <Transition
        enter-active-class="transition-opacity duration-300"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-300"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
    >
        <div
            v-if="menuOpen"
            class="fixed inset-0 z-[9998] bg-black/60 md:hidden"
            @click="emit('close-menu')"
        />
    </Transition>

    <!-- Drawer -->
    <Transition
        enter-active-class="transition-transform duration-300 ease-out"
        enter-from-class="-translate-x-full"
        enter-to-class="translate-x-0"
        leave-active-class="transition-transform duration-300 ease-in"
        leave-from-class="translate-x-0"
        leave-to-class="-translate-x-full"
    >
        <aside
            v-if="menuOpen"
            class="fixed top-0 left-0 z-[9999] w-64 h-full bg-[#111111] flex flex-col px-6 py-8 md:hidden"
        >

            <!-- Close Button + User -->
            <div class="flex flex-col items-center mb-8">

                <button
                    class="self-end text-white mb-6"
                    @click="emit('close-menu')"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="w-6 h-6"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M6 18L18 6M6 6l12 12"
                        />
                    </svg>
                </button>

                <!-- User Icon -->
                <div class="w-14 h-14 rounded-full bg-white flex items-center justify-center mb-2">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="w-8 h-8 text-gray-700"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                    >
                        <path
                            d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"
                        />
                    </svg>
                </div>

                <span class="text-sm font-semibold text-white">
                    Login
                </span>
                
            </div>

            <div class="border-t border-[#2a2a2a] mb-4"></div>

            <!-- Navigation -->
            <ul class="flex flex-col text-sm font-medium text-white">
                <li><a href="/" class="block py-4 text-center border-b border-[#2a2a2a] hover:text-[#c1121f]">Home</a></li>
                <li><a href="/fleet" class="block py-4 text-center border-b border-[#2a2a2a] hover:text-[#c1121f]">Fleet</a></li>
                <li><a href="/about" class="block py-4 text-center border-b border-[#2a2a2a] hover:text-[#c1121f]">About</a></li>
                <li><a href="/contact" class="block py-4 text-center border-b border-[#2a2a2a] hover:text-[#c1121f]">Contacts</a></li>
            </ul>

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

</script>