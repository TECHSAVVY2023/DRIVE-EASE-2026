import type { Car } from '~/utils/types/fleet'

export const useSimilarCars = () => {
    const { apiFetch } = useApiFetch()
    const similarCars = ref<Car[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)

    const fetchSimilarCars = async (carReference: string): Promise<void> => {
        loading.value = true
        error.value = null

        try {
            similarCars.value = await apiFetch<Car[]>(
                `/cars/${carReference}/similar/`
            )
        } catch (fetchError: unknown) {
            similarCars.value = []
            error.value = fetchError instanceof Error
                ? fetchError.message
                : 'Unable to load similar cars.'
        } finally {
            loading.value = false
        }
    }

    return {
        similarCars,
        loading,
        error,
        fetchSimilarCars,
    }
}
