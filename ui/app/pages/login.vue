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
                
                            <!-- Continue with Outlook -->
                            <button class="
                                w-full flex items-center justify-center gap-3
                                border border-white text-white text-sm font-medium
                                px-4 py-3 rounded-lg
                                hover:bg-white hover:text-[#C1121F]
                                transition-colors duration-200
                            ">
                                <!-- Outlook icon -->
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 flex-shrink-0" x="0px" y="0px" width="100" height="100" viewBox="0 0 48 48">
                                    <path fill="#40c4ff" d="M31.323,8.502L7.075,23.872l-2.085-3.29v-2.835c0-1.032,0.523-1.994,1.389-2.556l14.095-9.146	c2.147-1.393,4.914-1.394,7.061-0.001L31.323,8.502z"></path>
                                    <path fill="#1976d2" d="M27.317,5.911c0.073,0.043,0.145,0.088,0.217,0.135l11,7.136L11.259,30.47l-4.185-6.603	l20.017-12.713C28.988,9.95,29.071,7.241,27.317,5.911z"></path>
                                    <path fill="#0d47a1" d="M22.142,33.771L11.26,30.47l23.136-14.666c1.949-1.235,1.944-4.08-0.009-5.308l-0.104-0.065	l0.3,0.186l7.041,4.568c0.866,0.562,1.389,1.524,1.389,2.556v2.744L22.142,33.771z"></path>
                                    <path fill="#29b6f6" d="M20.886,43h15.523c3.646,0,6.602-2.956,6.602-6.602V17.797c0,1.077-0.554,2.079-1.466,2.652	l-23.09,14.498c-1.246,0.782-2.001,2.15-2.001,3.62C16.454,41.016,18.438,43,20.886,43z"></path>
                                    <radialGradient id="jOGZKH9xgyi24L29LbTdga_RUIFhdJm8fbJ_gr1" cx="-509.142" cy="-26.522" r=".07" gradientTransform="matrix(-170.8609 259.7254 674.0181 443.4041 -69097.734 144024.688)" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#49deff"></stop><stop offset=".724" stop-color="#29c3ff"></stop></radialGradient>
                                    <path fill="url(#jOGZKH9xgyi24L29LbTdga_RUIFhdJm8fbJ_gr1)" d="M27.198,42.999H11.589c-3.646,0-6.602-2.956-6.602-6.602V17.783	c0,1.076,0.552,2.076,1.461,2.649l23.067,14.543c1.263,0.796,2.029,2.185,2.029,3.678C31.544,41.053,29.598,42.999,27.198,42.999z"></path>
                                    <path fill="#80d8ff" d="M27.198,42.999H11.589c-3.646,0-6.602-2.956-6.602-6.602V17.783c0,1.076,0.552,2.076,1.461,2.649	l23.067,14.543c1.263,0.796,2.029,2.185,2.029,3.678C31.544,41.053,29.598,42.999,27.198,42.999z"></path>
                                    <path fill="#fff" d="M11.282,36.236c-1.398,0-2.545-0.437-3.442-1.312c-0.897-0.874-1.346-2.015-1.346-3.423	c0-1.486,0.455-2.689,1.366-3.607c0.911-0.918,2.103-1.377,3.577-1.377c1.393,0,2.526,0.439,3.401,1.318	c0.879,0.879,1.319,2.037,1.319,3.475c0,1.478-0.456,2.669-1.366,3.574C13.885,35.786,12.716,36.236,11.282,36.236z M11.323,34.381	c0.762,0,1.375-0.26,1.839-0.78c0.464-0.52,0.696-1.244,0.696-2.171c0-0.966-0.226-1.718-0.676-2.256	c-0.451-0.538-1.053-0.806-1.805-0.806c-0.775,0-1.4,0.278-1.873,0.833c-0.473,0.551-0.71,1.281-0.71,2.19	c0,0.923,0.237,1.653,0.71,2.19C9.977,34.114,10.583,34.381,11.323,34.381z"></path>
                                    <path fill="#1565c0" d="M6.453,23h10.094C18.454,23,20,24.546,20,26.453v10.094C20,38.454,18.454,40,16.547,40H6.453	C4.546,40,3,38.454,3,36.547V26.453C3,24.546,4.546,23,6.453,23z"></path>
                                    <path fill="#fff" d="M11.453,36.518c-1.4,0-2.55-0.452-3.449-1.355c-0.899-0.903-1.348-2.082-1.348-3.537	c0-1.536,0.456-2.778,1.369-3.726c0.913-0.949,2.107-1.423,3.584-1.423c1.396,0,2.532,0.454,3.408,1.362	c0.881,0.908,1.321,2.105,1.321,3.591c0,1.527-0.456,2.758-1.369,3.692C14.061,36.053,12.889,36.518,11.453,36.518z M11.493,34.601	c0.763,0,1.378-0.269,1.843-0.806c0.465-0.538,0.698-1.285,0.698-2.243c0-0.998-0.226-1.775-0.677-2.331	c-0.452-0.556-1.055-0.833-1.809-0.833c-0.777,0-1.403,0.287-1.877,0.861c-0.474,0.569-0.711,1.323-0.711,2.263	c0,0.953,0.237,1.707,0.711,2.263C10.145,34.326,10.752,34.601,11.493,34.601z"></path>
                                </svg>
                                Continue with Outlook
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
                            border border-[#2a2a2a] text-white text-sm font-medium
                            px-4 py-3 rounded-lg
                            hover:border-white
                            transition-colors duration-200
                            ">
                            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
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
 
<script setup>
// UI only — no functionality yet
</script>