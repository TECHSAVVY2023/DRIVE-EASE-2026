<template>
    <div class="pt-4 pb-4 flex items-center justify-center border-t border-b border-[#3F3F3F] gap-2">
        <div
            v-for="(step, i) in steps"
            :key="i"
            class="flex items-center gap-2"
        >
            <!-- Step bubble -->
            <div class="flex items-center gap-2">
                <div
                    class="w-8 h-8 rounded-md flex items-center justify-center text-sm font-bold flex-shrink-0"
                    :class="
                        currentStep > i + 1
                            ? 'bg-green-500 text-white'
                            : currentStep === i + 1
                                ? 'bg-[#C1121F] text-white'
                                : 'bg-[#2a2a2a] text-gray-400'
                    "
                >
                    <svg
                        v-if="currentStep > i + 1"
                        class="w-3.5 h-3.5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2.5"
                            d="M5 13l4 4L19 7"
                        />
                    </svg>

                    <span v-else>{{ i + 1 }}</span>
                </div>

                <div class="flex flex-col leading-tight">
                    <span class="text-white text-sm font-semibold">
                        {{ step.title }}
                    </span>
                    <span class="text-[#929292] text-xs">
                        {{ step.subtitle }}
                    </span>
                </div>
            </div>

            <!-- Connector -->
            <div
                v-if="i < steps.length - 1"
                class="w-4 h-px bg-[#2a2a2a] flex-shrink-0 mx-1"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
interface Step {
    title: string
    subtitle: string
}

defineProps<{
    currentStep: number
    steps: Step[]
}>()
</script>