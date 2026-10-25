<template>
    <!-- Left: Contact Form -->
    <div class="smoked-charcoal-panel md:col-span-3 rounded-xl p-6 flex flex-col gap-5">
        <div>
            <h2 class="text-white font-bold text-lg">How can we help you?</h2>
            <p class="text-[#9E9E9E] text-xs mt-1">Fill out the form below and our team will get back to you within 24 hours.</p>
        </div>

        <!-- Form -->
        <form
            class="flex flex-col gap-4"
            @submit.prevent="handleSubmit"
        >

            <div class="grid grid-cols-2 gap-4">
                <div class="flex flex-col gap-1.5">
                    <label class="text-[#9E9E9E] text-xs">First name</label>
                    <input
                        v-model="formData.firstname"
                        type="text"
                        placeholder="Juan"
                        class="
                            smoked-control rounded-lg px-3 py-2.5 text-white text-sm"
                    />
                </div>

                <div class="flex flex-col gap-1.5">
                    <label class="text-[#9E9E9E] text-xs">Last name</label>
                    <input
                        v-model="formData.lastname"
                        type="text"
                        placeholder="Dela Cruz"
                        class="
                            smoked-control rounded-lg px-3 py-2.5 text-white text-sm"
                    />
                </div>

            </div>

            <div class="grid grid-cols-2 gap-4">

                <div class="flex flex-col gap-1.5">
                    <label class="text-[#9E9E9E] text-xs">Email address</label>
                    <input
                        v-model="formData.contact_email"
                        type="email"
                        required
                        placeholder="juan@email.com"
                        class="
                            smoked-control rounded-lg px-3 py-2.5 text-white text-sm"
                    />
                </div>

                <div class="flex flex-col gap-1.5">
                    <label class="text-[#9E9E9E] text-xs">Contact number</label>
                    <input
                        v-model="formData.contact_number"
                        type="tel"
                        required
                        placeholder="+63 912 345 6789"
                        class="
                            smoked-control rounded-lg px-3 py-2.5 text-white text-sm"
                    />
                </div>

            </div>

            <div class="flex flex-col gap-1.5">
                <label class="text-[#9E9E9E] text-xs">Message</label>
                <textarea
                    v-model="formData.message"
                    rows="5"
                    placeholder="Write your message here..."
                    class="
                        smoked-control rounded-lg px-3 py-2.5 text-white text-sm resize-none"
                ></textarea>
            </div>

            <button class="w-full bg-[#C1121F] hover:bg-[#9B0E18] text-white text-sm font-semibold py-3 rounded-lg transition-colors duration-200">
                Send message
            </button>

        </form>

    </div>
</template>

<script setup lang="ts">

const emit = defineEmits(['submit'])

const props = defineProps<{
    formData: {
        contact_id: string
        firstname: string
        lastname: string
        contact_email: string
        contact_number: string
        message: string
    }
}>()

const formData = props.formData

const handleSubmit = () => {
    emit('submit', formData)
}

</script>
