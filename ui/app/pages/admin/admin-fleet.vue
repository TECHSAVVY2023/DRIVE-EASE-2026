 <template>
    
    <AdminFleetAddCarModal
        v-model="showVehicleModal"
        :vehicle="selectedVehicle"
        :is-editing="isEditing"
        @save="handleSaveVehicle"
    />

    <div class="flex h-screen bg-[#0D0D0D] font-[poppins] overflow-hidden text-white">

        <!-- Sidebar -->
        <AdminCommonSidebarNav
            :sidebarOpen="sidebarOpen" 
            @close-sidebar="sidebarOpen = false" 
        />

        <!-- Main -->
        <div class="flex-1 flex flex-col overflow-hidden">
            
            <AdminCommonTopbarNav
                :user="user"
                @open-sidebar="handleOpenSidebar"
                @close-sidebar="handleCloseSidebar"
                title="Fleet"
                :isLoggedIn="isLoggedIn"
                :subtitle="currentDate"
            />

            <!-- Content -->
            <main class="flex-1 overflow-y-auto px-8 py-8">
                <!-- Page heading -->
                <div class="flex justify-between items-end mb-[22px]">
                    <div>
                        <h2 class="text-[22px] font-extrabold">
                            Fleet
                        </h2>

                        <div class="text-[#8a8a8a] text-[13px] mt-1">
                            Manage vehicles, availability, and fleet status
                        </div>
                    </div>

                    <button
                        class="
                            bg-[#c81e2c] hover:bg-[#b31a27] transition text-white 
                            font-bold text-sm px-5 py-[11px] rounded-lg"
                        @click="showVehicleModal = true"
                    >
                        + Add vehicle
                    </button>
                </div>

                <!-- Stats -->
                <AdminCommonStatsCards :cards="statCards"/>

                <!-- Fleet overview -->
                <AdminFleetOverview
                    :available-percentage="availablePercentage"
                    :availability="availability"
                    :availability-ring="availabilityRing"
                    :fleet-condition="fleetCondition"
                    :healthy-count="healthyCount"
                    :maintenance-count="maintenanceCount"
                />

                <!-- Vehicle table -->
                <AdminFleetTable
                    :cars="fleet"

                    :search="search"
                    :current-page="currentPage"
                    :count="count"
                    :page-size="pageSize"
                    :total-pages="totalPages"
                    :next-page="nextPage"
                    :previous-page="previousPage"

                    :selected-car-type="selectedCarType"
                    :selected-condition="selectedStatus"
                    
                    :carTypeOptions="carTypeOptions"
                    :is-editing="isEditing"

                    @update:search="search = $event"
                    @update:page="currentPage = $event"

                    @update:selected-car-type="selectedCarType = $event"
                    @update:selected-condition="selectedStatus = $event"

                    @edit="handleEdit"
                    @status="handleStatus"
                    @delete="handleDelete"
                />

            </main>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Car, CarForm } from '~/utils/types/fleet'

const { isLoggedIn } = useAuth()
const { user } = useCurrentUser()
const { $swal } = useNuxtApp()

const showVehicleModal = ref(false)

const sidebarOpen = ref<boolean>(false)

const handleCloseSidebar = (): void => {
    sidebarOpen.value = false
}

const handleOpenSidebar = (): void => {
    sidebarOpen.value = true
}

const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
})

const { 
    fleet, count, currentPage, search, selectedCarType, selectedStatus, carTypeOptions,
    resetFilters, nextPage, previousPage, pageSize, fetchStats, totalCars, availableCount, 
    unavailableCount, maintenanceCount, rentedCount, totalPages,
} = useFleetList()

const statCards = computed(() => [
    {
        label: "Total vehicles",
        value: totalCars.value,
        icon: `<svg viewBox="0 0 24 24" stroke="white" fill="none" stroke-width="1.8"><path d="M5 16h14l-1.5-6h-11L5 16z"/><circle cx="7.5" cy="17.5" r="1.5"/><circle cx="16.5" cy="17.5" r="1.5"/><path d="M6 10 7.5 6h9l1.5 4"/></svg>`
    },
    {
        label: "Available",
        value: availableCount.value,
        icon: `<svg viewBox="0 0 24 24" stroke="white" fill="none" stroke-width="1.8"><path d="M20 6 9 17l-5-5"/></svg>`
    },
    {
        label: "Currently rented",
        value: rentedCount.value,
        icon: `<svg viewBox="0 0 24 24" stroke="white" fill="none" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>`
    },
    {
        label: "Maintenance",
        value: maintenanceCount.value,
        icon: `<svg viewBox="0 0 24 24" stroke="white" fill="none" stroke-width="1.8"><path d="M14 6a5 5 0 0 0-6 6L4 16l4 4 4-4a5 5 0 0 0 6-6l-3 3-3-3 2-4z"/></svg>`
    }
])

const availability = computed(() => [
    {
        label: 'Available',
        value: availableCount.value,
        dot: 'bg-[#3ddc78]',
    },
    {
        label: 'Unavailable',
        value: unavailableCount.value,
        dot: 'bg-[#e0a83e]',
    },
    {
        label: 'Maintenance',
        value: maintenanceCount.value,
        dot: 'bg-[#e05252]',
    },
])

const availablePercentage = computed(() => {
    if (!totalCars.value) return 0

    return Math.round(
        (availableCount.value / totalCars.value) * 100
    )
})

const availabilityRing = computed(() => {
    const percentage = availablePercentage.value;

    return {
        background: `conic-gradient(#3ddc78 0% ${percentage}%, #252525 ${percentage}% 100%)`
    };
});

const fleetCondition = computed(() => {
    if (!totalCars.value) return 0

    return Math.round(
        ((totalCars.value - maintenanceCount.value) / totalCars.value) * 100
    )
})

const healthyCount = computed(() => {
    return totalCars.value - maintenanceCount.value
})

const { handleCreateVehicle: createVehicle } = useCarAdminAdd()

async function handleCreateVehicle(form: CarForm) {
    const result = await createVehicle(form)

    if (!result.success) return

    showVehicleModal.value = false
    window.location.reload()
}

const isEditing = ref(false)

const selectedVehicle = ref<CarForm | null>(null)
const originalVehicleImageUrls = ref<string[]>([])

const handleEdit = (car: Car) => {
    isEditing.value = true

    originalVehicleImageUrls.value = [
        car.meta?.primary_image,
        ...(car.meta?.images ?? []),
    ].filter((url): url is string => Boolean(url))

    selectedVehicle.value = {
        id: car.car_id,
        car_type: car.car_type, // Map this if your options use strings
        brand: car.brand,
        model: car.model,
        year: car.year,
        price_per_day: Number(car.price_per_day),
        transmission: car.transmission.toLowerCase() as CarForm['transmission'],
        engine: car.engine,
        fuel_type: car.fuel_type.toLowerCase() as CarForm['fuel_type'],
        seats: car.seats,
        note: car.note ?? '',
        status: car.status as CarForm['status'],

        features: [...car.features],

        images: [...new Set([
            car.meta?.primary_image,
            ...(car.meta?.images ?? []),
        ].filter((url): url is string => Boolean(url)))]
            .map(url => ({ url })),
        thumbnail_url: car.meta?.primary_image ?? null,
    }

    console.log('All car images:', car.meta?.images)
    console.log('Thumbnail:', car.meta?.primary_image)
    showVehicleModal.value = true
}

const { handleUpdateVehicle: updateVehicle, handleSecondaryAction: updateStatus, 
        handleDeleteVehicle: deleteVehicle
 } = useCarAdminEdit()

async function handleUpdateVehicle(form: CarForm) {
    const result = await updateVehicle(
        form,
        originalVehicleImageUrls.value,
    )

    if (!result.success) return

    showVehicleModal.value = false
    window.location.reload()
}

async function handleStatus(car: Car) {
    const result = await updateStatus(car)

    if (!result.success) return

    window.location.reload()
}

async function handleDelete(car: Car) {
    const result = await $swal.fire({
        title: 'Delete vehicle?',
        text: `Are you sure you want to delete ${car.brand} ${car.model}?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        background: '#1a1a1a',
        confirmButtonColor: '#C1121F',
        color: '#ffffff',
    })

    if (!result.isConfirmed) return

    const response = await deleteVehicle(car)

    if (!response.success) return

    window.location.reload()
}

async function handleSaveVehicle(form: CarForm) {
    if (form.id) {
        await handleUpdateVehicle(form)
    } else {
        await handleCreateVehicle(form)
    }
}

onMounted(async () => {
    await fetchStats()
    resetFilters()
})

onMounted(() => {
    document.documentElement.classList.add('admin-page')
})

onBeforeUnmount(() => {
    document.documentElement.classList.remove('admin-page')
})

</script>
