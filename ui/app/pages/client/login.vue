<template>
    
    <div class="relative min-h-screen flex items-center justify-center font-[poppins]">
    
        <!-- =========================
                Login container
        ========================== -->
        <div 
            class="
                relative z-10 
                w-full max-w-sm mx-4 
                bg-[#111111] rounded-2xl 
                overflow-hidden shadow-2xl 
                border-t-8 border-[#C1121F]
            "
        >
        
            <!-- Card Content -->
            <div class="py-12 flex flex-col items-center gap-6">

                <div class="flex pb-4 flex-col items-center">

                    <img
                        src="~/assets/images/logo1.png"
                        alt="Drive Ease Logo"
                        class="w-auto h-16 object-contain"
                    />

                    <span class="text-gray-400 text-xs italic -mt-1">
                        Drive smart, drive easy
                    </span>

                </div>
        
                <div class="w-full border-t border-[#2a2a2a]"></div>
        
                <div class="px-12">

                    <div class="text-center">
                        
                        <div class="mb-8">

                            <h2 class="text-white font-semibold text-base">Welcome back</h2>
                            <p class="text-gray-400 text-xs mt-1">Sign in to make your booking more convenient</p>
                        
                        </div>
            
                        <!-- Login Buttons -->
                        <div class="flex flex-col gap-3 w-full">

                            <!-- Continue with Google -->
                            <button 
                                @click="handleGoogleLogin"
                                :disabled="isLoading"
                                class="
                                    w-full flex items-center justify-center gap-3
                                    border border-white text-white text-sm font-medium
                                    px-4 py-3 rounded-lg
                                    hover:bg-white hover:text-[#C1121F]
                                    transition-colors duration-200
                                "
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 flex-shrink-0" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                                    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                                    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
                                    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                                </svg>
                                Continue with Google
                            </button>

                        </div>
                
                        <!-- Or divider -->
                        <div class="flex items-center gap-3 w-full my-6">
                            <div class="flex-1 border-t border-[#2a2a2a]"></div>
                            <span class="text-gray-500 text-xs">or</span>
                            <div class="flex-1 border-t border-[#2a2a2a]"></div>
                        </div>
                
                        <!-- Go back home -->
                        <button 
                            @click="navigateTo('/')"
                            class="w-full flex items-center justify-center gap-2
                            border border-white hover:bg-white hover:text-[#c1121f] text-white text-sm font-medium
                            px-4 py-3 rounded-lg
                            hover:border-white
                            transition-colors duration-200
                            ">
                                <svg class="w-4 h-4" fill="currentColor" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 495.398 495.398" xml:space="preserve"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <g> <g> 
                                    <path d="M487.083,225.514l-75.08-75.08V63.704c0-15.682-12.708-28.391-28.413-28.391c-15.669,0-28.377,12.709-28.377,28.391 v29.941L299.31,37.74c-27.639-27.624-75.694-27.575-103.27,0.05L8.312,225.514c-11.082,11.104-11.082,29.071,0,40.158 c11.087,11.101,29.089,11.101,40.172,0l187.71-187.729c6.115-6.083,16.893-6.083,22.976-0.018l187.742,187.747 c5.567,5.551,12.825,8.312,20.081,8.312c7.271,0,14.541-2.764,20.091-8.312C498.17,254.586,498.17,236.619,487.083,225.514z"></path> 
                                    <path d="M257.561,131.836c-5.454-5.451-14.285-5.451-19.723,0L72.712,296.913c-2.607,2.606-4.085,6.164-4.085,9.877v120.401 c0,28.253,22.908,51.16,51.16,51.16h81.754v-126.61h92.299v126.61h81.755c28.251,0,51.159-22.907,51.159-51.159V306.79 c0-3.713-1.465-7.271-4.085-9.877L257.561,131.836z"></path> </g> </g> </g> </g>
                                </svg>
                            Go back home
                        </button>
            
                        <!-- Terms -->
                        <p class="text-gray-500 text-xs text-center mt-4">
                            By signing in you agree to our
                            <a href="#" class="text-white hover:text-[#C1121F] transition-colors duration-200">Terms of Service</a>
                            and
                            <a href="#" class="text-white hover:text-[#C1121F] transition-colors duration-200">Privacy Policy</a>
                        </p>
            
                    </div>

                </div>

            </div>

        </div>

        <!-- Background image -->
        <img
            src="~/assets/images/login-bg.png"
            alt="Background"
            class="absolute inset-0 w-full h-full object-cover"
        />

        <!-- Gradient overlay -->
        <div class="absolute inset-0 bg-gradient-to-b from-[#650B12]/40 to-black"></div>
    
    </div>

</template>
 
<script setup lang="ts">
import { ref, onMounted } from "vue"

/* ================= STATE ================= */
const isLoading = ref<boolean>(false)
const errorMessage = ref<string>("")

/* ================= ROUTE ================= */
const route = useRoute()

onMounted(() => {
    const err = route.query.error as string | undefined

    if (err === "unauthorized") {
        errorMessage.value = "Access denied. Your Google account is not authorized."
    } else if (err === "oauth_failed") {
        errorMessage.value = "Google login failed. Please try again."
    } else if (err === "no_code") {
        errorMessage.value = "OAuth error: no authorization code received."
    }
})

/* ================= AUTH ================= */
const { login } = useAuth()

const handleGoogleLogin = (): void => {
    isLoading.value = true
    errorMessage.value = ""
    login()
}
</script>