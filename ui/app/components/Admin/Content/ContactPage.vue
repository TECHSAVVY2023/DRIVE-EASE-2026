<template>
    <div class="space-y-7">
        <ContentSection title="Contact form introduction" description="Heading and message displayed above the customer contact form">
            <div class="grid gap-4 sm:grid-cols-2">
                <AdminContentFieldInput id="contact-form-heading" v-model="form.form_heading" label="Form heading" />
                <AdminContentFieldInput id="contact-form-description" v-model="form.form_description" label="Form description" />
            </div>
        </ContentSection>

        <ContentSection title="Contact information" description="Phone, email, and address displayed beside the contact form">
            <div class="grid gap-4 sm:grid-cols-2">
                <AdminContentFieldInput id="contact-phone" v-model="form.phone" label="Phone number" />
                <AdminContentFieldInput id="contact-email" v-model="form.email" label="Email address" type="email" />
                <div class="sm:col-span-2">
                    <AdminContentFieldInput id="contact-address" v-model="form.address" label="Business address" />
                </div>
            </div>
        </ContentSection>

        <ContentSection title="Opening hours" description="Weekly schedule displayed on the Contact page">
            <AdminContentEditorList title="Schedule" add-label="+ Add schedule" @add="addSchedule">
                <div v-for="(schedule, index) in form.opening_hours" :key="schedule.id || `new-${index}`" :class="cardClass">
                    <div class="grid gap-3 sm:grid-cols-2">
                        <AdminContentFieldInput :id="`contact-day-${index}`" v-model="schedule.day" label="Day or range" />
                        <AdminContentFieldInput :id="`contact-time-${index}`" v-model="schedule.time" label="Hours" />
                        <label class="flex items-center gap-2 text-[10px] text-[#888] sm:col-span-2">
                            <input v-model="schedule.is_closed" type="checkbox" class="accent-[#C1121F]">
                            Mark as closed
                        </label>
                    </div>
                    <AdminContentRemoveButton @click="form.opening_hours.splice(index, 1)" />
                </div>
            </AdminContentEditorList>
        </ContentSection>

        <ContentSection title="Social links" description="Profiles linked in the Follow us card">
            <div class="grid gap-4 sm:grid-cols-2">
                <AdminContentFieldInput id="facebook-url" v-model="form.facebook_url" label="Facebook URL" />
                <AdminContentFieldInput id="instagram-url" v-model="form.instagram_url" label="Instagram URL" />
                <AdminContentFieldInput id="x-url" v-model="form.x_url" label="X / Twitter URL" />
                <AdminContentFieldInput id="tiktok-url" v-model="form.tiktok_url" label="TikTok URL" />
            </div>
        </ContentSection>
    </div>
</template>

<script setup lang="ts">
import type { ContactPageContent } from '~/utils/types/content'

const props = defineProps<{ form: ContactPageContent }>()
const form = toRef(props, 'form')
const addSchedule = () => form.value.opening_hours.push({
    id: 0,
    day: '',
    time: '',
    is_closed: false,
    order: form.value.opening_hours.length,
})
const cardClass = 'relative rounded-lg border border-[#292929] bg-[#111] p-4 pr-16'
</script>
