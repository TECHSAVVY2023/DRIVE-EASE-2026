<template>
    <div class="flex flex-col gap-4 w-[100%]">
        <div class="flex flex-col gap-1.5">
            <label class="text-gray-400 text-xs">Pickup date</label>
            <input
                type="datetime-local"
                v-model="form.pickupDate"
                :min="minDateTime"
                required
                class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm focus:outline-none focus:border-[#C1121F] transition-colors duration-200"
            />
        </div>
        <div class="flex flex-col gap-1.5">
            <label class="text-gray-400 text-xs">Return date</label>
            <input
                type="datetime-local"
                v-model="form.returnDate"
                :min="minDateTime"
                required
                class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm focus:outline-none focus:border-[#C1121F] transition-colors duration-200"
            />
        </div>
        <div class="flex flex-col gap-1.5">
            <label class="text-gray-400 text-xs">Pickup location</label>
            <input type="text" required v-model="form.location" placeholder="e.g. Cagayan De Oro City" class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm placeholder-[#444] focus:outline-none focus:border-[#C1121F] transition-colors duration-200" />
        </div>
    </div>
</template>

<script setup lang="ts">

const props = defineProps<{
    form: any
}>()

const now = new Date()
const pad = (n: number) => String(n).padStart(2, '0')

const minDateTime =
    `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}T${pad(now.getHours())}:${pad(now.getMinutes())}`

</script>