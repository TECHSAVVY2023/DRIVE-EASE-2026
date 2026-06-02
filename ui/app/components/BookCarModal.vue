<template>
    <Teleport to="body">
        <Transition
        enter-active-class="transition-opacity duration-200"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-200"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
        >
            <div
                v-if="modelValue"
                class="fixed inset-0 z-999 bg-black/70 px-auto overflow-y-auto"
                @click.self="$emit('update:modelValue', false)"
            >
                <Transition
                    enter-active-class="transition-all duration-200"
                    enter-from-class="opacity-0 scale-95"
                    enter-to-class="opacity-100 scale-100"
                    leave-active-class="transition-all duration-200"
                    leave-from-class="opacity-100 scale-100"
                    leave-to-class="opacity-0 scale-95"
                >
                <div class="min-h-full flex justify-center px-4 py-20">
                    <div
                        v-if="modelValue"
                        class="
                            bg-[#111111] border-t-[#C1121F] border-t-5 rounded-xl 
                            w-full max-w-md font-[poppins] flex flex-col
                        "
                    >
                        <!-- Header -->
                        <div class="px-6 pt-6 pb-4 flex-shrink-0">
                            <h2 class="text-white font-extrabold text-lg">Book this car</h2>
                            <p class="text-[#929292] text-xs mt-1">Complete all steps to confirm your reservation</p>
                        </div>

                        <!-- Steps -->
                        <div class="pt-4 pb-4 flex items-center justify-center border-t border-b border-[#3F3F3F] gap-2">
                            <div
                                v-for="(step, i) in steps"
                                :key="i"
                                class="flex items-center gap-2"
                            >
                                <!-- Step bubble -->
                                <div class="flex items-center gap-2">
                                <div
                                    class="w-7 h-7 rounded-md flex items-center justify-center text-xs font-bold flex-shrink-0"
                                    :class="currentStep > i + 1
                                    ? 'bg-green-500 text-white'
                                    : currentStep === i + 1
                                        ? 'bg-[#C1121F] text-white'
                                        : 'bg-[#2a2a2a] text-gray-400'"
                                >
                                    <svg v-if="currentStep > i + 1" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                                    </svg>
                                    <span v-else>{{ i + 1 }}</span>
                                </div>
                                <div class="flex flex-col leading-tight">
                                    <span class="text-white text-[10px] font-semibold">{{ step.title }}</span>
                                    <span class="text-[#929292] text-[9px]">{{ step.subtitle }}</span>
                                </div>
                                </div>
                                <!-- Connector -->
                                <div v-if="i < steps.length - 1" class="w-4 h-px bg-[#2a2a2a] flex-shrink-0 mx-1"></div>
                            </div>
                        </div>

                    <!-- Content -->
                    <div class="px-6 py-6 flex flex-col gap-4">

                    <!-- Car summary card -->
                    <div class="flex items-center gap-3 bg-[#1a1a1a] border border-[#C1121F]/50 rounded-xl overflow-hidden">
                        <div class="w-24 h-16 flex-shrink-0 bg-[#141414] overflow-hidden">
                            <img
                                :src="`${useApiBase()}${car?.images[0]?.image}`"
                                :alt="`${car?.brand} ${car?.model}`"
                                class="w-full h-full object-cover"
                            />
                        </div>

                        <div class="flex-1 min-w-0 py-2">
                            <p class="text-white text-sm font-bold">
                                {{ car?.brand }} {{ car?.model }}
                            </p>
                            <p class="text-gray-400 text-xs">
                                ₱{{ car?.price_per_day }} / day
                            </p>
                        </div>

                        <div class="pr-3 flex-shrink-0">
                            <span
                                class="flex items-center gap-1 text-[10px] font-semibold text-green-400 bg-green-500/10 border border-green-500/20 px-2 py-1 rounded-full"
                            >
                                <span class="w-1.5 h-1.5 rounded-full bg-green-400"></span>
                                AVAILABLE
                            </span>
                        </div>
                    </div>

                    <!-- Step 1: Your Info & ID -->
                    <template v-if="currentStep === 1">
                        <div class="flex flex-col gap-4">

                        <!-- First + Last name -->
                        <div class="grid grid-cols-2 gap-3">
                            <div class="flex flex-col gap-1.5">
                            <label class="text-gray-400 text-xs">First name</label>
                            <input
                                v-model="form.firstName"
                                type="text"
                                class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm placeholder-[#444] focus:outline-none focus:border-[#C1121F] transition-colors duration-200"
                            />
                            </div>
                            <div class="flex flex-col gap-1.5">
                            <label class="text-gray-400 text-xs">Last name</label>
                            <input
                                v-model="form.lastName"
                                type="text"
                                class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm placeholder-[#444] focus:outline-none focus:border-[#C1121F] transition-colors duration-200"
                            />
                            </div>
                        </div>

                        <!-- Address -->
                        <div class="flex flex-col gap-1.5">
                            <label class="text-gray-400 text-xs">Address</label>
                            <input
                            v-model="form.address"
                            type="text"
                            class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm placeholder-[#444] focus:outline-none focus:border-[#C1121F] transition-colors duration-200"
                            />
                        </div>

                        <!-- Contact number -->
                        <div class="flex flex-col gap-1.5">
                            <label class="text-gray-400 text-xs">Contact number</label>
                            <input
                            v-model="form.contact"
                            type="tel"
                            class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm placeholder-[#444] focus:outline-none focus:border-[#C1121F] transition-colors duration-200"
                            />
                        </div>

                        <!-- Upload ID -->
                        <div class="flex flex-col gap-1.5">
                            <label class="text-gray-400 text-xs">Upload image of two valid IDs</label>
                            <p class="text-gray-500 text-[10px]">Valid ID that are accepted: national ID, driver license ID, passport.</p>

                            <!-- Drop zone -->
                            <div
                            class="border-2 border-dashed border-[#C1121F]/40 hover:border-[#C1121F] rounded-xl h-24 flex items-center justify-center cursor-pointer transition-colors duration-200"
                            @click="triggerUpload"
                            @dragover.prevent
                            @drop.prevent="handleDrop"
                            >
                            <p class="text-gray-500 text-xs text-center px-4">Click to upload image or drag and drop</p>
                            </div>
                            <input ref="fileInput" type="file" accept="image/*" multiple class="hidden" @change="handleFileChange" />
                        </div>

                        <!-- Uploaded previews -->
                        <div v-if="uploadedImages.length" class="flex flex-col gap-1.5">
                            <label class="text-gray-400 text-xs">Uploaded images</label>
                            <div class="flex gap-2 flex-wrap">
                            <div
                                v-for="(img, i) in uploadedImages"
                                :key="i"
                                class="relative w-16 h-12 rounded-lg overflow-hidden border border-[#2a2a2a] flex-shrink-0"
                            >
                                <img :src="img" alt="Uploaded ID" class="w-full h-full object-cover" />
                                <button
                                @click="removeImage(i)"
                                class="absolute top-0.5 right-0.5 w-4 h-4 bg-black/70 rounded-full flex items-center justify-center"
                                >
                                <svg class="w-2.5 h-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                                </svg>
                                </button>
                            </div>
                            </div>
                        </div>

                        </div>
                    </template>

                    <!-- Step 2: Schedule & Location (placeholder) -->
                    <template v-else-if="currentStep === 2">
                        <div class="flex flex-col gap-4">
                        <div class="flex flex-col gap-1.5">
                            <label class="text-gray-400 text-xs">Pickup date</label>
                            <input type="date" v-model="form.pickupDate" class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm focus:outline-none focus:border-[#C1121F] transition-colors duration-200" />
                        </div>
                        <div class="flex flex-col gap-1.5">
                            <label class="text-gray-400 text-xs">Return date</label>
                            <input type="date" v-model="form.returnDate" class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm focus:outline-none focus:border-[#C1121F] transition-colors duration-200" />
                        </div>
                        <div class="flex flex-col gap-1.5">
                            <label class="text-gray-400 text-xs">Pickup location</label>
                            <input type="text" v-model="form.location" placeholder="e.g. Cagayan De Oro City" class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg px-3 py-2.5 text-white text-sm placeholder-[#444] focus:outline-none focus:border-[#C1121F] transition-colors duration-200" />
                        </div>
                        </div>
                    </template>

                    <!-- Step 3: Review & Confirm (placeholder) -->
                    <template v-else-if="currentStep === 3">
                        <div class="bg-[#1a1a1a] border border-[#222] rounded-xl p-4 flex flex-col gap-3 text-sm">
                        <div class="flex justify-between">
                            <span class="text-gray-400 text-xs">Name</span>
                            <span class="text-white text-xs font-semibold">{{ form.firstName }} {{ form.lastName }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400 text-xs">Address</span>
                            <span class="text-white text-xs font-semibold">{{ form.address }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400 text-xs">Contact</span>
                            <span class="text-white text-xs font-semibold">{{ form.contact }}</span>
                        </div>
                        <div class="border-t border-[#222] pt-2 flex justify-between">
                            <span class="text-gray-400 text-xs">Pickup date</span>
                            <span class="text-white text-xs font-semibold">{{ form.pickupDate }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400 text-xs">Return date</span>
                            <span class="text-white text-xs font-semibold">{{ form.returnDate }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-gray-400 text-xs">Location</span>
                            <span class="text-white text-xs font-semibold">{{ form.location }}</span>
                        </div>
                        </div>
                    </template>

                    <!-- Actions -->
                    <div class="flex flex-col gap-2 mt-2">
                        <button
                        @click="handleNext"
                        class="w-full bg-[#C1121F] hover:bg-red-700 text-white text-sm font-bold py-3 rounded-lg transition-colors duration-200"
                        >
                        {{ currentStep === steps.length ? 'Confirm booking' : 'Next step' }}
                        </button>
                        <button
                        @click="closeModal"
                        class="w-full border border-[#2a2a2a] hover:border-white text-white text-sm font-semibold py-3 rounded-lg transition-colors duration-200"
                        >
                        Cancel
                        </button>
                    </div>

                    </div>
                    </div>
                </div>

                </Transition>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup lang="ts">
import { ref, reactive, onUnmounted } from 'vue'
import { useApiBase } from '~/utils/api/api'
import type { Car } from '~/utils/api/api'

const closeModal = () => {
    if (import.meta.client) {
        document.documentElement.style.overflow = 'hidden'
    }

    emit('update:modelValue', false)
}

interface Step {
  title: string
  subtitle: string
}

interface BookingForm {
    firstName: string
    lastName: string
    address: string
    contact: string
    pickupDate: string
    returnDate: string
    location: string
}


const props = defineProps<{
  modelValue: boolean
  car: Car | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'confirm', form: BookingForm): void
}>()

const steps: Step[] = [
  { title: 'Your info', subtitle: '& ID' },
  { title: 'Schedule', subtitle: '& Location' },
  { title: 'Review', subtitle: '& Confirm' },
]

const currentStep = ref<number>(1)
const fileInput = ref<HTMLInputElement | null>(null)
const uploadedImages = ref<string[]>([])

const form = reactive<BookingForm>({
  firstName: '',
  lastName: '',
  address: '',
  contact: '',
  pickupDate: '',
  returnDate: '',
  location: '',
})

function handleNext(): void {
  if (currentStep.value < steps.length) {
    currentStep.value++
  } else {
    emit('confirm', { ...form })
    emit('update:modelValue', false)
  }
}

function triggerUpload(): void {
  fileInput.value?.click()
}

function handleFileChange(e: Event): void {
  const input = e.target as HTMLInputElement
  if (!input.files) return
  Array.from(input.files).forEach(file => {
    const reader = new FileReader()
    reader.onload = (ev) => {
      if (ev.target?.result) {
        uploadedImages.value.push(ev.target.result as string)
      }
    }
    reader.readAsDataURL(file)
  })
}

function handleDrop(e: DragEvent): void {
    const files = e.dataTransfer?.files
    if (!files) return
    Array.from(files).forEach(file => {
        const reader = new FileReader()
        reader.onload = (ev) => {
        if (ev.target?.result) {
            uploadedImages.value.push(ev.target.result as string)
        }
        }
        reader.readAsDataURL(file)
    })
}

function removeImage(index: number): void {
  uploadedImages.value.splice(index, 1)
}

let scrollY = 0

watch(
    () => props.modelValue,
    (open) => {
        if (!import.meta.client) return

        if (open) {
            const scrollbarWidth =
                window.innerWidth - document.documentElement.clientWidth

            document.documentElement.style.overflow = 'hidden'

            // prevent layout shift
            document.body.style.paddingRight = `${scrollbarWidth}px`
        } else {
            setTimeout(() => {
                document.documentElement.style.overflow = ''
                document.body.style.paddingRight = ''
            }, 200)
        }
    },
    { immediate: true }
)

// onUnmounted(() => {
//     if (import.meta.client) {
//         document.documentElement.style.overflow = ''
//     }
// })
</script>