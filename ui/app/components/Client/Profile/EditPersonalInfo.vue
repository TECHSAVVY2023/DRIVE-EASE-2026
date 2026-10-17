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
                    class="w-full bg-[#111] border border-white/10 rounded px-3 py-2 text-white text-sm focus:outline-none focus:border-[#C1121F] transition-colors"
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
                    class="w-full bg-[#111] border border-white/10 rounded px-3 py-2 text-white text-sm focus:outline-none focus:border-[#C1121F] transition-colors"
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
            class="w-full bg-[#111] border border-white/10 rounded px-3 py-2 text-[#ABABAB] text-sm focus:outline-none focus:border-[#C1121F] transition-colors"
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
                class="w-full bg-[#111] border border-white/10 rounded px-3 py-2 text-white text-sm focus:outline-none focus:border-[#C1121F] transition-colors"
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
                class="w-full bg-[#111] border border-white/10 rounded px-3 py-2 text-white text-sm focus:outline-none focus:border-[#C1121F] transition-colors"
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
</script>