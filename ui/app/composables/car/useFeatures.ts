import { ref } from 'vue'

import type { Feature } from '~/utils/types/fleet'

export function useFeatures() {
    const { apiFetch } = useApiFetch()

    const features = ref<Feature[]>([])
    const loading = ref(false)
    const error = ref<unknown>(null)

    const fetchFeatures = async () => {
        loading.value = true
        error.value = null

        try {
            features.value = await apiFetch<Feature[]>('/features/')
        } catch (err) {
            error.value = err
            console.error('Failed to fetch features:', err)
        } finally {
            loading.value = false
        }
    }

    const addFeature = async (name: string) => {
        const trimmedName = name.trim()

        if (!trimmedName) {
            throw new Error('Feature name is required.')
        }

        // Prevent duplicate features locally.
        const existingFeature = features.value.find(
            feature => feature.name.toLowerCase() === trimmedName.toLowerCase()
        )

        if (existingFeature) {
            return existingFeature
        }

        error.value = null

        try {
            const newFeature = await apiFetch<Feature>('/features/', {
                method: 'POST',
                body: {
                    name: trimmedName,
                    slug: trimmedName.toLowerCase().replace(/\s+/g, '-'),
                },
            })

            features.value.push(newFeature)

            return newFeature
        } catch (err) {
            error.value = err
            console.error('Failed to add feature:', err)
            throw err
        }
    }

    return {
        features,
        loading,
        error,
        fetchFeatures,
        addFeature,
    }
}
