<template>
    <div class="bg-[#111111] font-sans">

        <!-- =========================
             Hero Section
        ========================== -->
        <section class="relative flex items-center min-h-[600px] overflow-hidden">

            <!-- Hero Content -->
            <div
                class="
                    relative z-10
                    flex flex-col justify-center items-center text-center
                    w-full px-12 py-16 pb-[55%]

                    md:w-1/2
                    md:items-start md:text-left
                    md:px-0 md:pb-16 md:pl-20

                    lg:pl-16
                    xl:pl-36
                "
            >
                <h1
                    class="
                        text-5xl sm:text-5xl md:text-4xl lg:text-6xl
                        font-[poppins] font-extrabold
                        leading-tight tracking-tight uppercase text-white
                    "
                >
                    Drive Smart<br />
                    Drive Easy
                </h1>

                <p class="mt-2 text-sm text-[#9E9E9E] font-[poppins]">
                    "Affordable. Reliable. Ready when you are."
                </p>

                <!-- CTA Buttons -->
                <div class="mt-12 flex gap-4">

                    <button
                        class="
                            px-8 py-4 rounded-[10px]
                            bg-[#C1121F] hover:bg-[#6B0A10]
                            text-sm text-white font-[poppins]
                            transition-colors duration-250
                        "
                    >
                        View cars
                    </button>

                    <button
                        class="
                            px-8 py-4 rounded-[10px]
                            border border-white
                            text-sm text-white font-[poppins]
                            hover:bg-white hover:text-[#C1121F]
                            transition-colors duration-200
                        "
                    >
                        Sign up
                    </button>
                </div>
            </div>

            <!-- =========================
                 Desktop Hero Image
            ========================== -->
            <div
                class="
                    absolute top-0 right-0
                    hidden md:block
                    h-full w-[35%]
                    bg-[#C1121F]
                    overflow-visible
                "
            >
                <img
                    src="~/assets/images/car1.png"
                    alt="Toyota Wigo"
                    class="
                        absolute top-1/2 -translate-y-1/2
                        md:-left-20 lg:-left-36
                        w-full scale-[1.3]
                        object-contain drop-shadow-2xl
                    "
                />
            </div>

            <!-- =========================
                 Mobile Hero Image
            ========================== -->
            <div class="absolute bottom-0 left-0 right-0 h-[50%] md:hidden">

                <!-- Red Background -->
                <div
                    class="
                        absolute bottom-0 left-0 right-0
                        h-[55%] bg-[#C1121F]
                    "
                ></div>

                <!-- Car Image -->
                <img
                    src="~/assets/images/car1.png"
                    alt="Toyota Wigo"
                    class="
                        absolute bottom-2 left-1/2
                        w-[75%] -translate-x-1/2
                        object-contain drop-shadow-2xl z-10
                    "
                />
            </div>
        </section>
    </div>
</template>