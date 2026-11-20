export type UserRole = 'Customer' | 'Admin' | 'Super Admin'

export interface User {
    id: number
    user_reference: string
    email: string
    given_name: string
    family_name: string
    contact_number: string
    profile_picture: string | null
    address: string
    date_joined: string
    date_created?: string
    id_images: {
        images: string[]
    }
    status: 'Active' | 'Suspended'
    role: UserRole
    rentals: number
}

export interface UsersResponse {
    count: number
    page: number
    page_size: number
    total_pages: number
    next: string | null
    previous: string | null
    results: User[]
}

export interface UpdateUserStatusResponse {
    message: string
    user: User
}

export interface UpdateProfilePayload {
    given_name: string
    family_name: string
    email: string
    contact_number: string
    address: string
    id_images: {
        images: string[]
    }
    profile_picture?: string
    deleted_images?: string[]
}

export interface AdminEditUserResponse {
    message: string
    user: User
}

export interface DeleteUserResponse {
    message: string
}

export interface AdminCreateUserPayload {
    given_name: string
    family_name: string
    email: string
    contact_number: string
    address: string
    id_images: {
        images: string[]
    }
    role: UserRole
}

export type AdminCreateUserFormPayload = Omit<AdminCreateUserPayload, 'id_images'>

export interface AdminCreateUserResponse {
    message: string
    user: User
}

export interface AdminEditUserPayload {
    given_name: string
    family_name: string
    email: string
    contact_number: string
    address: string
    remove_profile_picture?: boolean
    profile_removal_reason?: string
    remove_id_images?: string[]
    id_removal_reason?: string
    id_images?: {
        images: string[]
    }
    role?: UserRole
}

export interface AssignRoleResponse {
    message: string
    user: User
}

export interface UsersStats {
    total: number
    active: number
    suspended: number
}
