interface AvailabilityAlertResponse {
    subscribed: boolean
    message?: string
}

export const useCarAvailabilityAlert = () => {
    const { apiFetch } = useApiFetch()
    const subscribed = ref(false)
    const loading = ref(false)

    const getAlertStatus = async (carReference: string): Promise<void> => {
        const response = await apiFetch<AvailabilityAlertResponse>(
            `/cars/${carReference}/availability-alert/`
        )
        subscribed.value = response.subscribed
    }

    const subscribe = async (carReference: string): Promise<string> => {
        loading.value = true

        try {
            const response = await apiFetch<AvailabilityAlertResponse>(
                `/cars/${carReference}/availability-alert/`,
                { method: 'POST' }
            )
            subscribed.value = response.subscribed
            return response.message ?? 'Availability alert enabled.'
        } finally {
            loading.value = false
        }
    }

    const reset = (): void => {
        subscribed.value = false
        loading.value = false
    }

    return {
        subscribed,
        loading,
        getAlertStatus,
        subscribe,
        reset,
    }
}