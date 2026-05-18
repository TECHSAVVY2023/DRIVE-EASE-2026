<template>
    
    <!-- =========================
            Banner container
    ========================== -->
    <div class="relative flex justify-between bg-[#C1121F] px-10 py-10 md:px-26">

        <!-- Left -->
        <div>

            <p class="text-red-200 text-xs mb-1"> {{ subtitle }} </p>
            <h1 class="text-white text-2xl font-extrabold"> {{ title }} </h1>

        </div>

        <!-- Breadcrumbs -->
        <div class="flex items-center gap-2 text-xs mt-4 flex-wrap">

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