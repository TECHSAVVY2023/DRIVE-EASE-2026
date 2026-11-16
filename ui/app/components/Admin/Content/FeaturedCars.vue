<template>
    <ContentSection
        title="Featured fleet"
        description="Manage the heading, call to action, and vehicles shown in the homepage carousel"
    >
        <div class="space-y-5">
            <div class="grid gap-4 sm:grid-cols-2">
                <div>
                    <label for="fleet-heading" :class="labelClass">Section heading</label>
                    <input id="fleet-heading" v-model="props.form.fleet_heading" :class="fieldClass" />
                </div>

                <div>
                    <label for="fleet-description" :class="labelClass">Short description</label>
                    <input id="fleet-description" v-model="props.form.fleet_description" :class="fieldClass" />
                </div>
            </div>

            <div class="border-t border-[#262626] pt-5">
                <div class="mb-3 flex items-center justify-between gap-3">
                    <div>
                        <h3 class="text-xs font-semibold text-white">Featured vehicles</h3>
                        <p class="mt-1 text-[10px] text-[#666]">
                            Select vehicles from your fleet and provide a separate transparent PNG for the homepage.
                        </p>
                    </div>

                    <button 
                        type="button" 
                        :class="secondaryButtonClass"
                        @click="addFeaturedVehicle"
                    >
                        + Add vehicle
                    </button>
                </div>

                <div class="grid gap-3 lg:grid-cols-3">

                    <div
                        v-for="(vehicle, index) in props.form.featured_cars"
                        :key="index"
                        class="rounded-lg border border-[#292929] bg-[#111] p-4"
                    >
                        <div class="mb-4 flex items-center justify-between">
                            <span class="flex h-6 w-6 items-center justify-center rounded bg-[#C1121F]/10 text-[10px] font-bold text-[#C1121F]">
                                {{ index + 1 }}
                            </span>

                            <button 
                                type="button" 
                                class="text-[10px] text-[#777] transition hover:text-red-400"
                                @click="removeFeaturedVehicle(index)"
                            >
                                Remove
                            </button>
                        </div>

                        <div class="space-y-4">
                            <div>
                                <label :for="`fleet-car-${index}`" :class="labelClass">
                                    Select existing vehicle
                                </label>

                                <div class="relative">
                                    <select
                                        :id="`fleet-car-${index}`"
                                        v-model.number="vehicle.car"
                                        :class="`${compactFieldClass} appearance-none pr-9`"
                                    >
                                        <option :value="0">Choose from fleet</option>

                                        <option
                                            v-for="car in props.form.cars"
                                            :key="car.id"
                                            :value="car.id"
                                        >
                                            {{ car.brand }} {{ car.model }} {{ car.year }} · {{ car.car_reference }}
                                        </option>
                                    </select>

                                    <svg
                                        class="pointer-events-none absolute right-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-[#777]"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        stroke-width="2"
                                    >
                                        <path d="m6 9 6 6 6-6" />
                                    </svg>
                                </div>
                            </div>

                            <div class="grid grid-cols-2 gap-2 rounded-lg border border-[#252525] bg-[#0d0d0d] p-3">
                                <div>
                                    <p class="text-[9px] uppercase tracking-wide text-[#5f5f5f]">
                                        Vehicle
                                    </p>

                                    <p class="mt-1 truncate text-[11px] font-medium text-[#d0d0d0]">
                                                {{ getSelectedCar(vehicle)
                                                    ? selectedCarName(vehicle)
                                                    : 'Not selected'
                                        }}
                                    </p>
                                </div>

                                <div>
                                    <p class="text-[9px] uppercase tracking-wide text-[#5f5f5f]">
                                        Database price
                                    </p>

                                    <p class="mt-1 text-[11px] font-medium text-[#d0d0d0]">
                                        {{ getSelectedCar(vehicle)?.price_per_day ?? '—' }}
                                    </p>
                                </div>

                                <p class="col-span-2 border-t border-[#222] pt-2 text-[9px] leading-4 text-[#666]">
                                    Name and price are automatically taken from the selected fleet record.
                                </p>
                            </div>

                            <div>
                                <label :for="`fleet-image-${index}`" :class="labelClass">
                                    Featured PNG
                                </label>

                                <div class="rounded-lg border border-dashed border-[#333] bg-[#0d0d0d] p-3">
                                    <div class="flex items-center justify-between gap-3">
                                        <div class="min-w-0">
                                            <p class="truncate text-[10px] font-medium text-[#bbb]">
                                                {{ featuredImageFiles[index]?.name || imageFileName(vehicle.featured_image) }}
                                            </p>

                                            <p class="mt-1 text-[9px] text-[#606060]">
                                                Transparent PNG made for the homepage carousel
                                            </p>
                                        </div>

<button
    type="button"
    :class="secondaryButtonClass"
    @click="fileInputs[index]?.click()"
>
    {{ vehicle.featured_image || featuredImageFiles[index] ? 'Replace image' : 'Choose image' }}
</button>

<input
    :ref="el => setFileInput(el, index)"
    type="file"
    accept="image/png"
    class="hidden"
    @change="handleImageChange($event, index)"
>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>

            </div>
        </div>
    </ContentSection>
</template>

<script setup lang="ts">
import type { ComponentPublicInstance } from 'vue'
import type { HomepageContent, HomePageFeaturedCar } from '~/utils/types/content';

const props = defineProps<{
    form: HomepageContent
}>()

const addFeaturedVehicle = () => {
    props.form.featured_cars.push({
        id: 0,
        car: 0,
        car_name: '',
        car_reference: '',
        price_per_day: '',
        featured_image: '',
        order: props.form.featured_cars.length,
    })

    // Keep the selected-file array aligned with featured_cars by index.
    featuredImageFiles.value.push(null)
}

function getSelectedCar(vehicle: HomePageFeaturedCar) {
    return props.form.cars.find(car => car.id === vehicle.car)
}

function selectedCarName(vehicle: HomePageFeaturedCar) {
    const car = getSelectedCar(vehicle)
    return car ? `${car.brand} ${car.model} ${car.year}` : 'Not selected'
}

function imageFileName(imageUrl: string | null) {
    if (!imageUrl) return 'No image selected'
    return imageUrl.split('/').pop() || imageUrl
}

function removeFeaturedVehicle(index: number) {
    props.form.featured_cars.splice(index, 1)
    // Removing both entries prevents the next vehicle receiving this file.
    featuredImageFiles.value.splice(index, 1)
}

const fileInputs = ref<(HTMLInputElement | null)[]>([])
const featuredImageFiles = defineModel<(File | null)[]>(
    'featuredImageFiles',
    { required: true }
)

function setFileInput(
    element: Element | ComponentPublicInstance | null,
    index: number,
) {
    fileInputs.value[index] = element as HTMLInputElement | null
}

function handleImageChange(event: Event, index: number) {
    const input = event.target as HTMLInputElement
    const file = input.files?.[0]

    if (!file) return

    if (file.type !== 'image/png') {
        input.value = ''
        featuredImageFiles.value[index] = null
        return
    }

    featuredImageFiles.value[index] = file
}

const fieldClass = `
    w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f]
    px-3.5 py-2.5 text-[13px] text-[#d4d4d4]
    outline-none transition-colors placeholder:text-[#555]
    focus:border-[#C1121F]
`
const labelClass = 'mb-1.5 block text-[11px] text-neutral-400'
const secondaryButtonClass = `
    shrink-0 rounded-lg border border-[#343434] bg-[#1b1b1b]
    px-3 py-2 text-[10px] font-semibold text-[#bbb]
    transition hover:border-[#C1121F] hover:text-white
`
const compactFieldClass = `${fieldClass} px-3 py-2 text-xs`
</script>
