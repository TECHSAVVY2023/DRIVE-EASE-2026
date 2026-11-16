export const useAnalyticsList = () => {
    const { fetchStats } = useAnalytics()

    const formatCurrency = (value: number) =>
        new Intl.NumberFormat('en-PH', {
            style: 'currency',
            currency: 'PHP',
            notation: 'compact',
            maximumFractionDigits: 1,
        }).format(value)

    const formatChange = (value: number | null) => {
        if (value === null) return 'New'
        return `${value >= 0 ? '+' : ''}${value.toFixed(1)}%`
    }

    const loadStats = async (
        selectedPeriod: string,
        requestId: number,
        isLatestRequest: () => boolean
    ) => {
        try {
            const response = await fetchStats(selectedPeriod)

            if (!isLatestRequest()) return null

            return [
                {
                    label: 'Total revenue',
                    value: formatCurrency(response.total_revenue),
                    change: formatChange(response.revenue_change),
                    positive: response.revenue_change === null || response.revenue_change >= 0,
                    icon: 'M12 2v20m5-16H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6'
                },
                {
                    label: 'Total bookings',
                    value: String(response.total_bookings),
                    change: formatChange(response.bookings_change),
                    positive: response.bookings_change === null || response.bookings_change >= 0,
                    icon: 'M8 2v4m8-4v4M3 10h18M5 4h14a2 2 0 0 1 2 2v14H3V6a2 2 0 0 1 2-2Z'
                },
                {
                    label: 'Fleet utilization',
                    value: `${response.fleet_utilization.toFixed(1)}%`,
                    change: formatChange(response.fleet_utilization_change),
                    positive: response.fleet_utilization_change === null || response.fleet_utilization_change >= 0,
                    icon: 'M5 17h14l-1.5-6h-11L5 17Zm2-6 2-4h6l2 4M7 17v2m10-2v2'
                },
                {
                    label: 'Cancellation rate',
                    value: `${response.cancellation_rate.toFixed(1)}%`,
                    change: formatChange(response.cancellation_rate_change),
                    positive: response.cancellation_rate_change === null || response.cancellation_rate_change <= 0,
                    icon: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20Zm-3-13 6 6m0-6-6 6'
                },
            ]
        } catch (error) {
            console.error('Failed to load analytics stats:', error)
            throw error
        }
    }

    return { loadStats }
}
