
export interface AdminActivityLog {
    id: number
    log_reference: string
    admin: number | null
    admin_name: string
    admin_reference: string | null
    admin_profile_picture: string | null
    action: 'create' | 'update' | 'delete' | 'status_change'
    description: string
    target_type: string
    target_id: string
    created_at: string
}

export interface LogsResponse {
    count: number
    next: string | null
    previous: string | null
    results: AdminActivityLog[]
}
