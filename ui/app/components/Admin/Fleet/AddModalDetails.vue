<template>
    <!-- Identity -->
    <p :class="section">Identity</p>

    <div class="mb-3 grid grid-cols-3 gap-3">
    <div>
        <label :class="label" for="brand">Brand</label>
        <input id="brand" v-model="form.brand" :class="field" placeholder="Toyota" />
    </div>
    <div>
        <label :class="label" for="model">Model</label>
        <input id="model" v-model="form.model" :class="field" placeholder="Vios" />
    </div>
    <div>
        <label :class="label" for="year">Year</label>
        <input
            id="year"
            v-model.number="form.year"
            type="number"
            :class="field"
            placeholder="2023"
        />
    </div>
    </div>

    <div class="mb-5 grid grid-cols-2 gap-3">

        <div class="relative">
            <label :class="label" for="car_type">Car type</label>

            <input
                id="car_type"
                v-model="carTypeSearch"
                :class="field"
                type="text"
                placeholder="Search or add a car type"
                autocomplete="off"
                @focus="showCarTypeDropdown = true"
                @input="showCarTypeDropdown = true"
                @blur="closeCarTypeDropdown"
            />

            <!-- Dropdown -->
            <div
                v-if="showCarTypeDropdown"
                class="absolute z-20 mt-1 w-full overflow-hidden rounded-lg border border-[#2a2a2a] bg-[#161616] shadow-lg"
            >
                <!-- Existing car types -->
                <button
                    v-for="type in filteredCarTypes"
                    :key="type.id"
                    type="button"
                    class="w-full px-4 py-3 text-left text-sm text-white hover:bg-[#232323]"
                    @mousedown.prevent="selectCarType(type)"
                >
                    {{ type.name }}
                </button>

                <!-- Add new car type -->
                <button
                    v-if="canAddCarType"
                    type="button"
                    class="w-full border-t border-[#2a2a2a] px-4 py-3 text-left text-sm text-red-500 hover:bg-[#232323]"
                    @mousedown.prevent="handleAddCarType"
                >
                    + Add "{{ carTypeSearch.trim() }}"
                </button>

                <!-- No results -->
                <p
                    v-if="filteredCarTypes.length === 0 && !canAddCarType"
                    class="px-4 py-3 text-sm text-neutral-500"
                >
                    No car types found.
                </p>
            </div>
        </div>

        <div>
            <label :class="label" for="price">Price per day (₱)</label>
            <input
                id="price"
                v-model.number="form.price_per_day"
                type="number"
                :class="field"
                placeholder="1800"
            />
        </div>

    </div>

    <!-- Specifications -->
    <p :class="section">Specifications</p>
    <div class="mb-3 grid grid-cols-2 gap-3">
        
        <div>
            <span :class="label">Transmission</span>
            <div class="flex gap-1.5">
                <button
                    v-for="option in (['automatic', 'manual'] as const)"
                    :key="option"
                    class="flex-1 rounded-lg py-2 text-xs capitalize focus:outline-none focus-visible:ring-2 focus-visible:ring-red-600"
                    :class="
                    form.transmission === option
                        ? 'bg-[#c1121f] text-white'
                        : 'border border-neutral-700 text-neutral-400 hover:text-white'
                    "
                    @click="form.transmission = option"
                >
                    {{ option }}
                </button>
            </div>
        </div>

        <div>
            <div class="relative">
                <label :class="label" for="fuel">Fuel type</label>

                <select id="fuel" v-model="form.fuel_type" :class="field" class="appearance-none">
                    <option v-for="fuel in FUEL_TYPES" :key="fuel" :value="fuel">
                        {{ fuel }}
                    </option>
                </select>

                <svg
                    class="pointer-events-none absolute right-3 top-[33px] size-4 text-neutral-500"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                >
                    <path d="m6 9 6 6 6-6" />
                </svg>
            </div>
        </div>

    </div>

    <div class="mb-3 grid grid-cols-2 gap-3">

        <div>
            <label :class="label" for="engine">Engine</label>
            <input
            id="engine"
            v-model="form.engine"
            :class="field"
            placeholder="1.5L Dual VVT-i"
            />
        </div>

        <div>
            <div class="relative">
                <label :class="label" for="seats">Seats</label>
                <select id="seats" v-model.number="form.seats" :class="field" class="appearance-none">
                    <option v-for="count in SEAT_OPTIONS" :key="count" :value="count">
                        {{ count }}
                    </option>
                </select>

                <svg
                    class="pointer-events-none absolute right-3 top-[33px] size-4 text-neutral-500"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                >
                    <path d="m6 9 6 6 6-6" />
                </svg>
            </div>
        </div>

    </div>

    <div class="relative mb-5">
        <label :class="label" for="features">Features</label>

        <!-- Selected features -->
        <div
            v-if="selectedFeatures.length"
            class="mb-3 flex flex-wrap gap-2"
        >
            <span
                v-for="feature in selectedFeatures"
                :key="feature.id"
                class="flex items-center gap-2 rounded-lg border border-[#C1121F] bg-[#C1121F]/10 px-3 py-2 text-xs text-white"
            >
                {{ feature.name }}

                <button
                    type="button"
                    class="text-neutral-400 hover:text-white"
                    @click="removeFeature(feature.slug)"
                >
                    <span aria-hidden="true">&times;</span>
                </button>
            </span>
        </div>

        <!-- Search input -->
        <input
            id="features"
            v-model="featureSearch"
            :class="field"
            type="text"
            placeholder="Search or add a feature"
            autocomplete="off"
            @focus="showFeatureDropdown = true"
            @input="showFeatureDropdown = true"
            @blur="closeFeatureDropdown"
        />

        <!-- Dropdown -->
        <div
            v-if="showFeatureDropdown"
            class="absolute z-20 mt-1 w-full overflow-hidden rounded-lg border border-[#2a2a2a] bg-[#161616] shadow-lg"
        >
            <!-- Existing features -->
            <button
                v-for="feature in filteredFeatures"
                :key="feature.id"
                type="button"
                class="flex w-full items-center justify-between px-4 py-3 text-left text-sm text-white hover:bg-[#232323]"
                @mousedown.prevent="toggleFeature(feature.slug)"
            >
                {{ feature.name }}

                <span
                    v-if="props.form.features.includes(feature.slug)"
                    class="text-red-500"
                >
                    ✓
                </span>
            </button>

            <!-- Add new feature -->
            <button
                v-if="canAddFeature"
                type="button"
                class="w-full border-t border-[#2a2a2a] px-4 py-3 text-left text-sm text-red-500 hover:bg-[#232323]"
                @mousedown.prevent="handleAddFeature"
            >
                + Add "{{ featureSearch.trim() }}"
            </button>

            <!-- No results -->
            <p
                v-if="filteredFeatures.length === 0 && !canAddFeature"
                class="px-4 py-3 text-sm text-neutral-500"
            >
                No features found.
            </p>
        </div>
    </div>

    <!-- Availability -->
    <p :class="section">Availability</p>
    <div class="mb-3">

        <span :class="label">Status</span>
        <div class="flex gap-2">
            <button
            v-for="option in STATUSES"
            :key="option.value"
            class="flex-1 rounded-lg py-2 text-xs focus:outline-none focus-visible:ring-2 focus-visible:ring-red-600"
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

    <div class="mb-2.5">
        <label :class="label" for="note">Note</label>
        <textarea
            id="note"
            v-model="form.note"
            rows="2"
            :class="field"
            placeholder="Last serviced Sept 2026, minor scratch on rear bumper"
        />
    </div>
</template>

<script setup lang="ts">
import type { CarForm, CarType, Feature } from '~/utils/api/api'

const props = defineProps<{
    form: CarForm
}>()

const CAR_TYPES = [ 'sedan', 'suv', 'hatchback', 'mpv', 'pickup', 'van', ] 

const FUEL_TYPES = [ 'gasoline', 'diesel', 'hybrid', 'electric', ] 

const SEAT_OPTIONS = [2, 4, 5, 7, 8] 

const STATUSES = [ 
    { 
        value: 'available', 
        label: 'Available', 
        active: 'bg-emerald-800 text-emerald-200', 
    },
    { 
        value: 'maintenance', 
        label: 'Maintenance', 
        active: 'bg-amber-800 text-amber-200', 
    }, 
] as const

const field = `
    w-full rounded-lg
    border border-[#2a2a2a]
    pl-3.5 pr-9 py-2
    bg-[#0f0f0f]
    text-sm text-white
    placeholder:text-neutral-600
    focus:border-[#C1121F]
    focus:outline-none
    [appearance:textfield]
    [&::-webkit-inner-spin-button]:appearance-none
    [&::-webkit-outer-spin-button]:appearance-none
`
const label = 'mb-1.5 block text-[11px] text-[#9E9E9E]'
const section = 'mb-2.5 text-[12px] font-bold text-white'

const { carTypes, fetchCarTypes, addCarType } = useCarTypes()

onMounted(() => {
    fetchCarTypes()
})

const carTypeSearch = ref('')
const showCarTypeDropdown = ref(false)

const filteredCarTypes = computed(() => {
    const search = carTypeSearch.value.trim().toLowerCase()

    return carTypes.value.filter(type =>
        type.name.toLowerCase().includes(search)
    )
})

const canAddCarType = computed(() => {
    const search = carTypeSearch.value.trim().toLowerCase()

    return (
        search.length > 0 &&
        !carTypes.value.some(
            type => type.name.toLowerCase() === search
        )
    )
})

function selectCarType(type: CarType) {
    props.form.car_type = type.slug
    carTypeSearch.value = type.name
    showCarTypeDropdown.value = false
}

async function handleAddCarType() {
    try {
        const newType = await addCarType(carTypeSearch.value)

        props.form.car_type = newType.slug
        carTypeSearch.value = newType.name
        showCarTypeDropdown.value = false
    } catch (err) {
        console.error('Failed to add car type:', err)
    }
}

function closeCarTypeDropdown() {
    showCarTypeDropdown.value = false
}

const {
    features,
    loading: featuresLoading,
    fetchFeatures,
    addFeature,
} = useFeatures()

const toggleFeature = (featureSlug: string) => {
    const selected = props.form.features

    if (selected.includes(featureSlug)) {
        props.form.features = selected.filter(
            slug => slug !== featureSlug
        )
    } else {
        props.form.features = [...selected, featureSlug]
    }
}

onMounted(() => {
    fetchFeatures()
})

const featureSearch = ref('')
const showFeatureDropdown = ref(false)

// Features currently selected in the form.
const selectedFeatures = computed(() =>
    features.value.filter(feature =>
        props.form.features.includes(feature.slug)
    )
)

// Filter features based on the search input.
const filteredFeatures = computed(() => {
    const search = featureSearch.value.trim().toLowerCase()

    return features.value.filter(feature =>
        feature.name.toLowerCase().includes(search)
    )
})

// Show the Add option only if the name doesn't already exist.
const canAddFeature = computed(() => {
    const search = featureSearch.value.trim().toLowerCase()

    if (!search) return false

    return !features.value.some(
        feature => feature.name.toLowerCase() === search
    )
})

// Remove a selected feature.
const removeFeature = (featureSlug: string) => {
    props.form.features = props.form.features.filter(
        slug => slug !== featureSlug
    )
}

// Add a new feature and select it.
const handleAddFeature = async () => {
    const name = featureSearch.value.trim()

    if (!name) return

    try {
        const feature = await addFeature(name)

        if (!props.form.features.includes(feature.slug)) {
            props.form.features = [
                ...props.form.features,
                feature.slug,
            ]
        }

        featureSearch.value = ''
        showFeatureDropdown.value = true
    } catch (err) {
        console.error('Failed to add feature:', err)
    }
}

// Close the dropdown when the input loses focus.
const closeFeatureDropdown = () => {
    showFeatureDropdown.value = false
}

watch(
    () => props.form.car_type,
    (carType) => {
        carTypeSearch.value = carType ?? ''
    },
    { immediate: true }
)

watchEffect(() => {
    console.log('Form feature IDs:', props.form.features)
    console.log('Available features:', features.value)
    console.log('Selected features:', selectedFeatures.value)
})

</script>