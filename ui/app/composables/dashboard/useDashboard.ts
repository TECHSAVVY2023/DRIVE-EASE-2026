import type {
    DashboardAttentionResponse,
    DashboardFleetStatusResponse,
    DashboardRecentBookingsResponse,
    DashboardRevenueResponse,
    DashboardStatsResponse,
} from '~/utils/types/dashboard'

export const useDashboard = () => {

    const { apiFetch } = useApiFetch()

    const fetchRevenue = async (month: string): Promise<DashboardRevenueResponse> => {
        return await apiFetch<DashboardRevenueResponse>(
            `/admin/dashboard/revenue/?month=${encodeURIComponent(month)}`
        )
    }

    const fetchStats = async (month: string): Promise<DashboardStatsResponse> => {
        return await apiFetch<DashboardStatsResponse>(
            `/admin/dashboard/stats/?month=${encodeURIComponent(month)}`
        )
    }

    const fetchFleetStatus = async (): Promise<DashboardFleetStatusResponse> =>
        apiFetch<DashboardFleetStatusResponse>('/admin/dashboard/fleet-status/')

    const fetchRecentBookings = async (): Promise<DashboardRecentBookingsResponse> =>
        apiFetch<DashboardRecentBookingsResponse>('/admin/dashboard/recent-bookings/')

    const fetchAttention = async (): Promise<DashboardAttentionResponse> =>
        apiFetch<DashboardAttentionResponse>('/admin/dashboard/attention/')

    return {
        fetchRevenue,
        fetchStats,
        fetchFleetStatus,
        fetchRecentBookings,
        fetchAttention,
    }
}
