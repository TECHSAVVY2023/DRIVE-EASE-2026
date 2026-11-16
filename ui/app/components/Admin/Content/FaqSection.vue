<template>
    <ContentSection
        title="Frequently asked questions"
        description="Manage the introduction and questions displayed in the homepage FAQ accordion"
    >
        <div class="space-y-5">
            <div class="grid gap-4 sm:grid-cols-2">
                <div>
                    <label for="faq-heading" :class="labelClass">Section heading</label>
                    <input id="faq-heading" v-model="props.form.faq_heading" :class="fieldClass">
                </div>

                <div>
                    <label for="faq-highlight" :class="labelClass">Highlighted heading</label>
                    <input id="faq-highlight" v-model="props.form.faq_highlight" :class="fieldClass">
                </div>

                <div class="sm:col-span-2">
                    <label for="faq-description" :class="labelClass">Description</label>
                    <textarea id="faq-description" v-model="props.form.faq_description" rows="3" :class="textareaClass" />
                </div>

            </div>

            <div class="border-t border-[#262626] pt-5">
                <div class="mb-3 flex items-center justify-between gap-3">
                    <div>
                        <h3 class="text-xs font-semibold text-white">Questions and answers</h3>
                        <p class="mt-1 text-[10px] text-[#666]">Questions appear in this order on the homepage.</p>
                    </div>

                    <button type="button" :class="secondaryButtonClass" @click="addFaq">
                        + Add question
                    </button>
                </div>

                <div class="space-y-3">
                    <div
                        v-for="(faq, index) in props.form.faqs"
                        :key="faq.id || `new-${index}`"
                        class="grid gap-3 rounded-lg border border-[#292929] bg-[#111] p-4 sm:grid-cols-[32px_1fr_auto]"
                    >
                        <div class="flex h-8 w-8 items-center justify-center rounded bg-[#222] text-xs font-bold text-[#C1121F]">
                            {{ index + 1 }}
                        </div>

                        <div class="grid gap-3 lg:grid-cols-2">
                            <div>
                                <label :for="`faq-question-${index}`" :class="labelClass">Question</label>
                                <input :id="`faq-question-${index}`" v-model="faq.question" :class="compactFieldClass">
                            </div>

                            <div>
                                <label :for="`faq-answer-${index}`" :class="labelClass">Answer</label>
                                <textarea :id="`faq-answer-${index}`" v-model="faq.answer" rows="2" :class="compactTextareaClass" />
                            </div>
                        </div>

                        <button
                            type="button"
                            class="self-start pt-1 text-[10px] text-[#777] transition hover:text-red-400"
                            @click="removeFaq(index)"
                        >
                            Remove
                        </button>
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

function addFaq(): void {
    props.form.faqs.push({
        id: 0,
        question: '',
        answer: '',
        order: props.form.faqs.length,
    })
}

function removeFaq(index: number): void {
    props.form.faqs.splice(index, 1)
}

const fieldClass = `
    w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f]
    px-3.5 py-2.5 text-[13px] text-[#d4d4d4]
    outline-none transition-colors placeholder:text-[#555]
    focus:border-[#C1121F]
`
const labelClass = 'mb-1.5 block text-[11px] text-neutral-400'
const textareaClass = `${fieldClass} resize-none leading-5`
const compactFieldClass = `${fieldClass} px-3 py-2 text-xs`
const compactTextareaClass = `${compactFieldClass} resize-none leading-5`
const secondaryButtonClass = `
    shrink-0 rounded-lg border border-[#343434] bg-[#1b1b1b]
    px-3 py-2 text-[10px] font-semibold text-[#bbb]
    transition hover:border-[#C1121F] hover:text-white
`
</script>
