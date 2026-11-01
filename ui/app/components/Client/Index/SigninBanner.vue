<template>
    <!-- =========================
            CTA Banner
    ========================== -->
    <div class="bg-[#1a1a1a] px-8 py-12 flex flex-col md:flex-row items-center justify-between gap-4">
        
        <div>

            <h3 class="text-white font-bold text-lg md:text-xl">Ready to hit the road?</h3>

            <p class="text-gray-400 text-sm mt-1">Sign in and rent your car in minutes!</p>

        </div>

        <button 
            @click="$router.push('/login')"
            class="
                border border-white text-white text-sm font-semibold
                px-6 py-3 rounded-full
                hover:bg-white hover:text-[#C11F1F]
                transition-colors duration-200
                whitespace-nowrap
            "
        >
            Sign in to rent
        </button>

    </div>
</template>