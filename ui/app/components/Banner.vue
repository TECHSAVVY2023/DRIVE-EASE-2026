<template>

    <!-- =========================
            Banner container
    ========================== -->
    <div class="relative flex flex-col items-center text-center md:flex-row md:items-center md:justify-between md:text-left gap-4 md:gap-6 bg-[#C1121F] px-6 py-8 sm:px-10 sm:py-10 md:px-16 lg:px-26">

        <!-- Left -->
        <div class="min-w-0">

            <p class="text-red-200 text-xs mb-1"> {{ subtitle }} </p>
            <h1 class="text-white text-xl sm:text-2xl font-extrabold break-words"> {{ title }} </h1>

        </div>

        <!-- Breadcrumbs -->
        <div class="flex items-center justify-center gap-2 text-xs flex-wrap mt-3 md:mt-0 md:justify-end md:shrink-0">

            <template
                v-for="(breadcrumb, index) in breadcrumbs"
                :key="breadcrumb.label"
            >

                <!-- Link -->
                <NuxtLink
                    v-if="breadcrumb.to"
                    :to="breadcrumb.to"
                    class="text-red-200 hover:text-white transition-colors duration-200"
                >
                    {{ breadcrumb.label }}
                </NuxtLink>

                <!-- Current Page -->
                <span
                    v-else
                    class="text-white font-semibold"
                >
                    {{ breadcrumb.label }}
                </span>

                <span
                    v-if="index !== breadcrumbs.length - 1"
                    class="text-red-300"
                >
                    /
                </span>

            </template>

        </div>

    </div>
</template>

<script setup lang="ts">
type Breadcrumb = {
    label: string
    to?: string
}

defineProps<{
    subtitle: string
    title: string
    breadcrumbs: Breadcrumb[]
}>()
</script>