<template>
    <Teleport to="body">
        <Transition
            enter-active-class="transition duration-150"
            leave-active-class="transition duration-100"
            enter-from-class="opacity-0"
            leave-to-class="opacity-0"
        >
        <div
            v-if="open"
            class="fixed inset-0 z-101 flex items-center justify-center bg-black/70 p-4"
            @click.self="close"
        >
            <div
                class="
                    flex max-h-[90vh] w-full max-w-xl flex-col overflow-hidden 
                    rounded-2xl bg-[#111111] border-t-[#C1121F] border-t-5 shadow-2xl
                "
                role="dialog"
                aria-modal="true"
            >

            <!-- Header -->
            <header class="flex items-start justify-between px-4 sm:px-6 pt-5 sm:pt-4 pb-4 border-b border-white/10">

                <div>
                    <h2 class="text-white font-extrabold text-lg font-[Poppins]">
                        {{ props.isEditing ? 'Edit a car' : 'Add a car' }}
                    </h2>
                    <p class="text-[#929292] text-xs mt-1">
                        {{
                            props.isEditing
                                ? 'Update the details of this vehicle'
                                : 'Enter the details to add a new vehicle to your fleet'
                        }}
                    </p>
                </div>

                <button 
                    @click="close" 
                    class="text-white/40 hover:text-white transition-colors mt-0.5"
                >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>

            </header>

            <!-- Body -->
            <div class="flex-1 overflow-y-auto px-5 py-5">
                <!-- Photos -->
                <AdminFleetAddModalImgUploader
                    v-model:images="form.images"
                    v-model:thumbnail-url="form.thumbnail_url"
                />

                <AdminFleetAddModalDetails 
                    :form="form"
                />

            </div>

            <!-- Footer -->
            <footer class="flex justify-end gap-2.5 border-t border-neutral-800 px-5 py-4">

                <button 
                    class="
                        rounded-lg px-4 py-2 border border-[#2a2a2a] 
                        hover:border-white text-[#CCCCCC] hover:text-white text-sm 
                        transition-colors duration-200 cursor-pointer
                    "
                    @click="close"
                >
                    Cancel
                </button>

                <button
                    class="
                        rounded-lg bg-[#C1121F] hover:bg-[#b31a27] px-4 py-2 
                        text-xs font-medium text-white transition-colors 
                        duration-200 cursor-pointer
                    "
                    @click="save"
                >
                    {{ props.isEditing ? 'Save changes' : 'Add vehicle' }}
                </button>
                
            </footer>
            </div>
        </div>
        </Transition>
    </Teleport>
</template>

<script setup lang="ts">
import type { CarForm } from '~/utils/api/api'

const form = ref<CarForm>(blank())

const open = defineModel<boolean>({ required: true })
    
const props = defineProps<{
    vehicle: CarForm | null
    isEditing: boolean
}>()

const emit = defineEmits<{ save: [vehicle: CarForm] }>()

function blank(): CarForm {
    return {
        id: '',
        car_type: null,
        brand: '',
        model: '',
        year: null,
        price_per_day: null,
        transmission: 'automatic',
        engine: '',
        fuel_type: 'gasoline',
        seats: 5,
        note: '',
        status: 'available',

        features: [],

        images: [],
        thumbnail_url: null,
    }
}

watch(
    () => [open.value, props.vehicle] as const,
    ([isOpen, vehicle]) => {
        if (!isOpen) return

        if (vehicle) {
            // Edit mode: populate the form with the selected vehicle.
            form.value = {
                ...blank(),
                ...toRaw(vehicle),
                features: [...vehicle.features],
                images: [...vehicle.images],
            }
        } else {
            // Add mode: reset the form.
            form.value = blank()
        }
    },
    { immediate: true },
)

function close() {
  open.value = false
}

function save() {
    const vehicle = toRaw(form.value)

    emit('save', {
        ...vehicle,
        features: [...vehicle.features],
        images: vehicle.images.map(image => ({ ...image })),
    })
}

</script>