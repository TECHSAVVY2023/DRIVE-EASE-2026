<script setup lang="ts">
export interface BookingUser {
  id: string
  name: string
}

export interface BookingCar {
  id: string
  brand: string
  model: string
  price_per_day: number
}

export interface Booking {
  id: string
  user_id: string
  car_id: string
  pickup_date: string // 'YYYY-MM-DDTHH:mm' (datetime-local)
  pickup_location: string
  return_date: string
  return_location: string
  discount: number
  number_of_days: number
  subtotal: number
  total_price: number
  status: 'pending' | 'confirmed' | 'completed' | 'cancelled'
}

const open = defineModel<boolean>({ required: true })

const props = defineProps<{
  booking: Booking | null
  users: BookingUser[]
  cars: BookingCar[]
}>()
const emit = defineEmits<{ save: [booking: Booking] }>()

const STATUSES = [
  { value: 'pending', label: 'Pending', active: 'bg-amber-800 text-amber-200' },
  { value: 'confirmed', label: 'Confirmed', active: 'bg-blue-800 text-blue-200' },
  { value: 'completed', label: 'Completed', active: 'bg-emerald-800 text-emerald-200' },
  { value: 'cancelled', label: 'Cancelled', active: 'bg-red-900 text-red-200' },
] as const

function blank(): Booking {
  return {
    id: '',
    user_id: '',
    car_id: '',
    pickup_date: '',
    pickup_location: '',
    return_date: '',
    return_location: '',
    discount: 0,
    number_of_days: 0,
    subtotal: 0,
    total_price: 0,
    status: 'pending',
  }
}

const form = ref<Booking>(blank())

watch(
  () => [open.value, props.booking] as const,
  ([isOpen]) => {
    if (isOpen) form.value = props.booking ? structuredClone(toRaw(props.booking)) : blank()
  },
  { immediate: true },
)

const isNew = computed(() => !form.value.id)

const selectedUser = computed(() => props.users.find(u => u.id === form.value.user_id))
const selectedCar = computed(() => props.cars.find(c => c.id === form.value.car_id))

// Price summary — all derived, never typed in by hand
const numberOfDays = computed(() => {
  const ms = new Date(form.value.return_date).getTime() - new Date(form.value.pickup_date).getTime()
  return Number.isFinite(ms) && ms > 0 ? Math.ceil(ms / 86_400_000) : 0
})
const subtotal = computed(() => numberOfDays.value * (selectedCar.value?.price_per_day ?? 0))
const discount = computed(() => Number(form.value.discount) || 0)
const totalPrice = computed(() => Math.max(0, subtotal.value - discount.value))

const hasValidDates = computed(() => numberOfDays.value > 0)
const discountTooHigh = computed(() => discount.value > subtotal.value)
const canSave = computed(
  () =>
    !!form.value.user_id &&
    !!form.value.car_id &&
    hasValidDates.value &&
    discount.value >= 0 &&
    !discountTooHigh.value,
)

function close() {
  open.value = false
}

function save() {
  if (!canSave.value) return
  emit('save', {
    ...structuredClone(toRaw(form.value)),
    discount: discount.value,
    number_of_days: numberOfDays.value,
    subtotal: subtotal.value,
    total_price: totalPrice.value,
  })
  close()
}

const peso = (n: number) => `₱${n.toLocaleString()}`

const field =
  'w-full rounded-lg border border-neutral-700 bg-neutral-900 px-3 py-2 text-sm text-white placeholder:text-neutral-600 focus:border-red-600 focus:outline-none [color-scheme:dark]'
const label = 'mb-1.5 block text-[11px] text-neutral-400'
const section = 'mb-2.5 text-[11px] tracking-wide text-red-600'
</script>

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
            class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-0 sm:p-4"
            @click.self="close"
        >
            <div
            class="flex h-[100dvh] w-full max-w-xl flex-col overflow-hidden rounded-none border border-neutral-800 bg-neutral-900 shadow-2xl sm:h-auto sm:max-h-[90dvh] sm:rounded-2xl"
            role="dialog"
            aria-modal="true"
            >
            <!-- Header -->
            <header class="flex items-center justify-between border-b border-neutral-800 px-5 py-4">
                <div>
                <p class="text-[15px] font-medium text-white">
                    {{ isNew ? 'Add booking' : 'Edit booking' }}
                </p>
                <p v-if="!isNew && selectedUser && selectedCar" class="mt-0.5 text-xs text-neutral-500">
                    {{ selectedUser.name }} · {{ selectedCar.brand }} {{ selectedCar.model }}
                </p>
                </div>
                <button
                class="rounded-md p-1 text-neutral-500 hover:bg-neutral-800 hover:text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-red-600"
                aria-label="Close"
                @click="close"
                >
                <Icon name="tabler:x" class="size-[18px]" />
                </button>
            </header>

            <!-- Body -->
            <div class="flex-1 overflow-y-auto px-5 py-5">
                <!-- Booking -->
                <p :class="section">Booking</p>
                <div class="mb-5 grid grid-cols-1 gap-3 sm:grid-cols-2">
                <div>
                    <label :class="label" for="user">User</label>
                    <select id="user" v-model="form.user_id" :class="field">
                    <option value="" disabled>Select user</option>
                    <option v-for="user in users" :key="user.id" :value="user.id">
                        {{ user.name }}
                    </option>
                    </select>
                </div>
                <div>
                    <label :class="label" for="car">Car</label>
                    <select id="car" v-model="form.car_id" :class="field">
                    <option value="" disabled>Select car</option>
                    <option v-for="car in cars" :key="car.id" :value="car.id">
                        {{ car.brand }} {{ car.model }} — {{ peso(car.price_per_day) }}/day
                    </option>
                    </select>
                </div>
                </div>

                <!-- Schedule -->
                <p :class="section">Schedule</p>
                <div class="mb-3 grid grid-cols-1 gap-3 sm:grid-cols-2">
                <div>
                    <label :class="label" for="pickup_date">Pickup date</label>
                    <input
                    id="pickup_date"
                    v-model="form.pickup_date"
                    type="datetime-local"
                    :class="field"
                    />
                </div>
                <div>
                    <label :class="label" for="pickup_location">Pickup location</label>
                    <input id="pickup_location" v-model="form.pickup_location" :class="field" />
                </div>
                </div>
                <div class="mb-3 grid grid-cols-1 gap-3 sm:grid-cols-2">
                <div>
                    <label :class="label" for="return_date">Return date</label>
                    <input
                    id="return_date"
                    v-model="form.return_date"
                    type="datetime-local"
                    :class="[field, form.return_date && !hasValidDates && '!border-red-600']"
                    />
                </div>
                <div>
                    <label :class="label" for="return_location">Return location</label>
                    <input id="return_location" v-model="form.return_location" :class="field" />
                </div>
                </div>
                <p v-if="form.return_date && !hasValidDates" class="mb-3 text-[11px] text-red-500">
                Return date must be after the pickup date.
                </p>

                <!-- Pricing -->
                <p :class="[section, 'mt-5']">Pricing</p>
                <div class="mb-3">
                <label :class="label" for="discount">Discount (₱)</label>
                <input
                    id="discount"
                    v-model.number="form.discount"
                    type="number"
                    min="0"
                    :class="[field, discountTooHigh && '!border-red-600']"
                    placeholder="0"
                />
                <p v-if="discountTooHigh" class="mt-1.5 text-[11px] text-red-500">
                    Discount can't be more than the subtotal.
                </p>
                </div>

                <!-- Price summary (computed) -->
                <div class="mb-5 flex flex-col gap-2.5 rounded-xl border border-neutral-800 bg-neutral-950 px-4 py-3">
                <div class="flex justify-between text-xs">
                    <span class="text-neutral-400">Number of days</span>
                    <span class="font-medium text-white">{{ numberOfDays }}</span>
                </div>
                <div class="flex justify-between text-xs">
                    <span class="text-neutral-400">Subtotal</span>
                    <span class="font-medium text-white">{{ peso(subtotal) }}</span>
                </div>
                <div v-if="discount > 0" class="flex justify-between text-xs">
                    <span class="text-neutral-400">Discount</span>
                    <span class="font-medium text-red-500">−{{ peso(discount) }}</span>
                </div>
                <div class="flex justify-between border-t border-neutral-800 pt-2.5">
                    <span class="text-sm font-medium text-white">Total price</span>
                    <span class="text-base font-semibold text-white">{{ peso(totalPrice) }}</span>
                </div>
                </div>

                <!-- Status -->
                <p :class="section">Status</p>
                <div class="grid grid-cols-2 gap-2 sm:grid-cols-4">
                <button
                    v-for="option in STATUSES"
                    :key="option.value"
                    class="rounded-lg py-2 text-xs focus:outline-none focus-visible:ring-2 focus-visible:ring-red-600"
                    :class="
                    form.status === option.value
                        ? option.active
                        : 'border border-neutral-700 text-neutral-400 hover:text-white'
                    "
                    @click="form.status = option.value"
                >
                    {{ option.label }}
                </button>
                </div>
            </div>

            <!-- Footer -->
            <footer class="flex justify-end gap-2.5 border-t border-neutral-800 px-5 py-4">
                <button
                class="rounded-lg border border-neutral-700 px-4 py-2 text-xs text-neutral-400 hover:text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-red-600"
                @click="close"
                >
                Cancel
                </button>
                <button
                :disabled="!canSave"
                class="rounded-lg bg-red-600 px-4 py-2 text-xs font-medium text-white hover:bg-red-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-400 disabled:cursor-not-allowed disabled:opacity-50"
                @click="save"
                >
                {{ isNew ? 'Add booking' : 'Save changes' }}
                </button>
            </footer>
            </div>
        </div>
        </Transition>
    </Teleport>
</template>