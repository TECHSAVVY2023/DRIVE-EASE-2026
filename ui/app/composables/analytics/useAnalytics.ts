import type {
    AnalyticsCustomerInsightsResponse,
    AnalyticsRevenueResponse,
    AnalyticsStatusDistributionResponse,
    AnalyticsStatsResponse,
    AnalyticsTopVehiclesResponse,
    BookingStatsResponse,
} from '~/utils/types/analytics'

export const useAnalytics = () => {
    const { apiFetch } = useApiFetch()

    const fetchBookingStats = async (): Promise<BookingStatsResponse> => {
        return await apiFetch<BookingStatsResponse>('/admin/bookings/stats/')
    }

    const fetchStats = (period: string): Promise<AnalyticsStatsResponse> =>
        apiFetch<AnalyticsStatsResponse>(
            `/admin/analytics/stats/?period=${encodeURIComponent(period)}`
        )

    const fetchRevenue = (period: string): Promise<AnalyticsRevenueResponse> =>
        apiFetch<AnalyticsRevenueResponse>(
            `/admin/analytics/revenue/?period=${encodeURIComponent(period)}`
        )

    const fetchStatusDistribution = (period: string): Promise<AnalyticsStatusDistributionResponse> =>
        apiFetch<AnalyticsStatusDistributionResponse>(
            `/admin/analytics/status-distribution/?period=${encodeURIComponent(period)}`
        )

    const fetchTopVehicles = (period: string): Promise<AnalyticsTopVehiclesResponse> =>
        apiFetch<AnalyticsTopVehiclesResponse>(
            `/admin/analytics/top-vehicles/?period=${encodeURIComponent(period)}`
        )

    const fetchCustomerInsights = (period: string): Promise<AnalyticsCustomerInsightsResponse> =>
        apiFetch<AnalyticsCustomerInsightsResponse>(
            `/admin/analytics/customer-insights/?period=${encodeURIComponent(period)}`
        )

    return {
        fetchStats,
        fetchRevenue,
        fetchStatusDistribution,
        fetchTopVehicles,
        fetchCustomerInsights,
        fetchBookingStats,
    }
}
