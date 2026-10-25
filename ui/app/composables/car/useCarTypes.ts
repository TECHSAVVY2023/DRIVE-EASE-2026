import { ref } from 'vue'

import type { CarType } from '~/utils/types/fleet'

export function useCarTypes() {
    const { apiFetch } = useApiFetch()

    const carTypes = ref<CarType[]>([])
    const loading = ref(false)
    const error = ref<unknown>(null)

    const fetchCarTypes = async () => {
        loading.value = true
        error.value = null

        try {
            carTypes.value = await apiFetch<CarType[]>('/car-types/')
        } catch (err) {
            error.value = err
            console.error('Failed to fetch car types:', err)
        } finally {
            loading.value = false
        }
    }

    const addCarType = async (name: string) => {
        const trimmedName = name.trim()

        if (!trimmedName) {
            throw new Error('Car type name is required.')
        }

        // Prevent duplicate types locally.
        const existingType = carTypes.value.find(
            type => type.name.toLowerCase() === trimmedName.toLowerCase()
        )

        if (existingType) {
            return existingType
        }

        error.value = null

        try {
            const newType = await apiFetch<CarType>('/car-types/', {
                method: 'POST',
                body: {
                    name: trimmedName,
                    slug: trimmedName.toLowerCase().replace(/\s+/g, '-'),
                },
            })

            carTypes.value.push(newType)

            return newType
        } catch (err) {
            error.value = err
            console.error('Failed to add car type:', err)
            throw err
        }
    }

    return {
        carTypes,
        loading,
        error,
        fetchCarTypes,
        addCarType,
    }
}
