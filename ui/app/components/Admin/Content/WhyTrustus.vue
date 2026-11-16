<template>
    <ContentSection
        title="Why choose us"
        description="Edit the four trust highlights displayed below the hero section"
    >
        <div class="space-y-5">
            <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
                <div class="w-full max-w-xl">
                    <label for="trust-heading" :class="labelClass">
                        Section heading
                    </label>

                    <input
                        id="trust-heading"
                        v-model="props.form.trust_heading"
                        :class="fieldClass"
                    />
                </div>

                <button
                    v-if="props.form.trust_items.length < 4"
                    type="button"
                    class="shrink-0 rounded-lg border border-[#343434] bg-[#1b1b1b] px-3 py-2.5 text-[10px] font-semibold text-[#bbb] transition hover:border-[#C1121F] hover:text-white"
                    @click="addTrustItem"
                >
                    + Add highlight
                </button>
            </div>

            <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
                <div
                    v-for="(stat, index) in props.form.trust_items"
                    :key="stat.id || `new-${index}`"
                    class="rounded-lg border border-[#292929] bg-[#111] p-4"
                >
                    <div class="mb-3 flex items-center justify-between">
                        <span class="text-[10px] font-semibold uppercase tracking-wide text-[#666]">
                            Highlight {{ index + 1 }}
                        </span>

                        <button
                            type="button"
                            class="text-[10px] text-[#777] transition hover:text-red-400"
                            @click="removeTrustItem(index)"
                        >
                            Remove
                        </button>
                    </div>

                    <div class="space-y-3">
                        <div>
                            <label :for="`trust-value-${index}`" :class="labelClass">
                                Value
                            </label>

                            <input
                                :id="`trust-value-${index}`"
                                v-model="stat.value"
                                :class="compactFieldClass"
                            />
                        </div>

                        <div>
                            <label :for="`trust-label-${index}`" :class="labelClass">
                                Label
                            </label>

                            <input
                                :id="`trust-label-${index}`"
                                v-model="stat.label"
                                :class="compactFieldClass"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </ContentSection>
</template>

<script setup lang="ts">
import type { HomepageContent } from '~/utils/types/content'

const props = defineProps<{
    form: HomepageContent
}>()

const addTrustItem = () => {
    props.form.trust_items.push({
        id: 0,
        value: '',
        label: '',
        order: props.form.trust_items.length,
    })
}

const removeTrustItem = (index: number) => {
    props.form.trust_items.splice(index, 1)
}

const fieldClass = `
    w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f]
    px-3.5 py-2.5 text-[13px] text-[#d4d4d4]
    outline-none transition-colors placeholder:text-[#555]
    focus:border-[#C1121F]
`
const labelClass = 'mb-1.5 block text-[11px] text-neutral-400'
const compactFieldClass = `${fieldClass} px-3 py-2 text-xs`

</script>
