<template>
    <!-- Name -->
    <div>
        <div class="grid grid-cols-2 gap-3">
            <div>
                <label
                    class="text-[#9E9E9E] text-[10px] uppercase tracking-wider block mb-1"
                >
                    First Name
                </label>

                <input
                    v-model="props.form.given_name"
                    type="text"
                    :class="fieldClass"
                />
            </div>

            <div>
                <label
                    class="text-[#9E9E9E] text-[10px] uppercase tracking-wider block mb-1"
                >
                    Last Name
                </label>

                <input
                    v-model="props.form.family_name"
                    type="text"
                    :class="fieldClass"
                />
            </div>
        </div>
    </div>

    <!-- Email -->
    <div>
        <label
            class="text-[#9E9E9E] text-[10px] uppercase tracking-wider block mb-1"
        >
            Email Address
        </label>

        <input
            v-model="props.form.email"
            type="email"
            readonly
            :class="fieldClass"
        />
    </div>

    <!-- Contact & Address -->
    <div class="grid grid-cols-2 gap-3">
        <div>
            <label
                class="text-[#9E9E9E] text-[10px] uppercase tracking-wider block mb-1"
            >
                Contact Number
            </label>

            <input
                v-model="props.form.contact_number"
                type="text"
                :class="fieldClass"
            />
        </div>

        <div>
            <label
                class="text-[#9E9E9E] text-[10px] uppercase tracking-wider block mb-1"
            >
                Address
            </label>

            <input
                v-model="props.form.address"
                type="text"
                :class="fieldClass"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
const props = defineProps<{
    form: {
        given_name: string
        family_name: string
        email: string
        contact_number: string
        address: string
    }
}>()

const fieldClass = 'w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3.5 py-2.5 text-[13px] text-[#e4e4e4] outline-none transition-colors placeholder:text-neutral-600 hover:border-[#3a3a3a] focus:border-[#C1121F]'
</script>
