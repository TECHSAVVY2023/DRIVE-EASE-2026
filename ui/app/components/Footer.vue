<template>
    <footer class="bg-[#0D0D0D] font-[poppins]">

        <!-- CTA Banner -->
        <div class="bg-[#1a1a1a] px-8 py-12 flex flex-col md:flex-row items-center justify-between gap-4">
            <div>
                <h3 class="text-white font-bold text-lg md:text-xl">Ready to hit the road?</h3>
                <p class="text-gray-400 text-sm mt-1">Sign in and rent your car in minutes!</p>
            </div>
            <button class="
                border border-white text-white text-sm font-semibold
                px-6 py-3 rounded-full
                hover:bg-white hover:text-[#C11F1F]
                transition-colors duration-200
                whitespace-nowrap
            ">
                Sign in to rent
            </button>
        </div>

        <!-- Main Footer -->
        <div class="max-w-6xl mx-auto px-8 py-12 flex flex-col md:flex-row gap-10 md:gap-16">

        <!-- Brand -->
        <div class="flex flex-col justify-center items-center text-center gap-4 md:w-1/3">
            <div class="w-16 h-16 rounded-full overflow-hidden border border-[#2a2a2a]">
                <img
                    src="~/assets/images/logo.png"
                    alt="Drive Ease Logo"
                    class="w-full h-full object-cover"
                />
            </div>

            <p class="text-gray-400 text-sm leading-relaxed max-w-[180px]">
            Your trusted car rental partner across 15+ locations nationwide
            </p>
            <!-- Social Icons -->
            <div class="flex items-center gap-4 mt-2">
            <!-- Facebook -->
            <a href="#" class="text-gray-400 hover:text-white transition-colors duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/>
                </svg>
            </a>
            <!-- X / Twitter -->
            <a href="#" class="text-gray-400 hover:text-white transition-colors duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
            </a>
            <!-- Google -->
            <a href="#" class="text-gray-400 hover:text-white transition-colors duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12.545 10.239v3.821h5.445c-.712 2.315-2.647 3.972-5.445 3.972a6.033 6.033 0 110-12.064c1.498 0 2.866.549 3.921 1.453l2.814-2.814A9.969 9.969 0 0012.545 2C7.021 2 2.543 6.477 2.543 12s4.478 10 10.002 10c8.396 0 10.249-7.85 9.426-11.748l-9.426-.013z"/>
                </svg>
            </a>
            </div>
        </div>

        <!-- Links -->
        <div class="flex flex-1 flex-wrap gap-10 md:justify-end">

            <!-- Quick Links -->
            <div class="flex flex-col gap-3">
            <h4 class="text-white font-semibold text-sm">Quick links</h4>
            <ul class="flex flex-col gap-2">
                <li><a href="#" class="text-gray-400 text-sm hover:text-white transition-colors duration-200">Home</a></li>
                <li><a href="#" class="text-gray-400 text-sm hover:text-white transition-colors duration-200">Fleet</a></li>
                <li><a href="#" class="text-gray-400 text-sm hover:text-white transition-colors duration-200">Contact</a></li>
                <li><a href="#" class="text-gray-400 text-sm hover:text-white transition-colors duration-200">About us</a></li>
            </ul>
            </div>

            <!-- Legal -->
            <div class="flex flex-col gap-3">
            <h4 class="text-white font-semibold text-sm">Legal</h4>
            <ul class="flex flex-col gap-2">
                <li><a href="#" class="text-gray-400 text-sm hover:text-white transition-colors duration-200">Privacy</a></li>
                <li><a href="#" class="text-gray-400 text-sm hover:text-white transition-colors duration-200">Insurance</a></li>
                <li><a href="#" class="text-gray-400 text-sm hover:text-white transition-colors duration-200">Terms</a></li>
            </ul>
            </div>

            <!-- Contact -->
            <div class="flex flex-col gap-3">
            <h4 class="text-white font-semibold text-sm">Contact</h4>
            <ul class="flex flex-col gap-2">
                <li><span class="text-gray-400 text-sm">+639123456789</span></li>
                <li><span class="text-gray-400 text-sm">drive-ease@gmail.com</span></li>
                <li><span class="text-gray-400 text-sm">Cebu city</span></li>
            </ul>
            </div>

        </div>
        </div>

        <!-- Bottom Bar -->
        <div class="border-t border-[#2a2a2a] px-8 py-4">
        <p class="text-gray-500 text-xs text-center">
            © 2026 DriveEase. All rights reserved.
        </p>
        </div>

    </footer>
</template>