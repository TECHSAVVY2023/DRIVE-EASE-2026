import type { AdminEditUserPayload, UserRole } from '~/utils/types/accounts'

interface AssignRoleResult {
    success: boolean
    message: string
}

type AdminEditUserResult = AssignRoleResult

export const useUserAdminEdit = () => {
    const { assignUserRole, updateUserAdmin } = useUsers()
    const { $swal } = useNuxtApp()

    const handleAssignRole = async (
        userId: number,
        role: UserRole,
    ): Promise<AssignRoleResult> => {
        $swal.fire({
            title: 'Assigning role...',
            text: 'Please wait.',
            background: '#1a1a1a',
            color: '#ffffff',
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => $swal.showLoading(),
        })

        try {
            const response = await assignUserRole(userId, role)

            $swal.close()

            await $swal.fire({
                icon: 'success',
                title: 'Success',
                text: response.message,
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
                allowOutsideClick: false,
                allowEscapeKey: false,
                scrollbarPadding: false,
            })

            return {
                success: true,
                message: response.message,
            }
        } catch (error: any) {
            const message =
                error?.data?.detail ??
                error?.response?._data?.detail ??
                'Failed to assign the user role.'

            $swal.close()

            await $swal.fire({
                icon: 'error',
                title: 'Error',
                text: message,
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
            })

            return {
                success: false,
                message,
            }
        }
    }

    const handleEditUser = async (
        userId: number,
        body: AdminEditUserPayload,
    ): Promise<AdminEditUserResult> => {
        if (!body.email.trim()) {
            const message = 'Please enter an email address.'

            await $swal.fire({
                icon: 'warning',
                title: 'Incomplete Form',
                text: message,
                background: '#1a1a1a',
                confirmButtonColor: '#C1121F',
                color: '#ffffff',
            })

            return { success: false, message }
        }

        if (body.remove_profile_picture && !body.profile_removal_reason?.trim()) {
            const message = 'Please provide a reason for removing the profile picture.'
            await showValidationWarning(message)
            return { success: false, message }
        }

        if (body.remove_id_images?.length && !body.id_removal_reason?.trim()) {
            const message = 'Please provide a reason for removing the selected ID documents.'
            await showValidationWarning(message)
            return { success: false, message }
        }

        $swal.fire({
            title: 'Saving changes...',
            text: 'Please wait.',
            background: '#1a1a1a',
            color: '#ffffff',
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => $swal.showLoading(),
        })

        try {
            const response = await updateUserAdmin(userId, body)

            $swal.close()

            await $swal.fire({
                icon: 'success',
                title: 'Success',
                text: response.message,
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
                allowOutsideClick: false,
                allowEscapeKey: false,
                scrollbarPadding: false,
            })

            return { success: true, message: response.message }
        } catch (error: any) {
            const message = getApiErrorMessage(error)

            console.error('Failed to update user:', error)
            $swal.close()

            await $swal.fire({
                icon: 'error',
                title: 'Update Failed',
                text: message,
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
            })

            return { success: false, message }
        }
    }

    const showValidationWarning = async (message: string) => {
        await $swal.fire({
            icon: 'warning',
            title: 'Incomplete Form',
            text: message,
            background: '#1a1a1a',
            confirmButtonColor: '#C1121F',
            color: '#ffffff',
        })
    }

    const getApiErrorMessage = (error: any): string => {
        const data = error?.data ?? error?.response?._data

        if (typeof data?.detail === 'string') return data.detail

        if (data && typeof data === 'object') {
            const firstError = Object.values(data).flat().find(
                value => typeof value === 'string'
            )

            if (typeof firstError === 'string') return firstError
        }

        return 'Failed to update the user.'
    }

    return {
        handleAssignRole,
        handleEditUser
    }
}
