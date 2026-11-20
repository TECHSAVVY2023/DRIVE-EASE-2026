import { uploadFile } from '~/utils/api/upload'
import type { AdminCreateUserFormPayload, AdminEditUserPayload, UserRole } from '~/utils/types/accounts'

interface AssignRoleResult {
    success: boolean
    message: string
}

type AdminEditUserResult = AssignRoleResult

export const useUserAdminEdit = () => {
    const {
        assignUserRole,
        createUserAdmin,
        deleteUserAdmin,
        updateUserAdmin,
        updateUserStatus,
    } = useUsers()
    const { $swal } = useNuxtApp()
    const { validateFile } = useProfileUploads()

    const handleAssignRole = async (
        userReference: string,
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
            const response = await assignUserRole(userReference, role)

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
        userReference: string,
        body: AdminEditUserPayload,
        idFiles: File[] = [],
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

        if (idFiles.length > 5) {
            const message = 'You can upload no more than five valid ID documents.'
            await showValidationWarning(message)
            return { success: false, message }
        }

        for (const file of idFiles) {
            if (!(await validateFile(file))) {
                return { success: false, message: 'One or more ID documents are invalid.' }
            }
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
            const idImageUrls = await Promise.all(idFiles.map(file => uploadFile(file)))
            const response = await updateUserAdmin(userReference, {
                ...body,
                ...(idImageUrls.length ? { id_images: { images: idImageUrls } } : {}),
            })

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

    const handleCreateUser = async (
        body: AdminCreateUserFormPayload,
        idFiles: File[],
    ): Promise<AssignRoleResult> => {
        if (!body.given_name.trim() || !body.family_name.trim() || !body.email.trim()) {
            const message = 'Please complete the first name, last name, and email fields.'
            await showValidationWarning(message)
            return { success: false, message }
        }

        if (idFiles.length > 5) {
            const message = 'You can upload no more than five valid ID documents.'
            await showValidationWarning(message)
            return { success: false, message }
        }

        for (const file of idFiles) {
            if (!(await validateFile(file))) {
                return { success: false, message: 'One or more ID documents are invalid.' }
            }
        }

        $swal.fire({
            title: 'Creating user...',
            text: 'Please wait.',
            background: '#1a1a1a',
            color: '#ffffff',
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => $swal.showLoading(),
        })

        try {
            const idImageUrls = await Promise.all(idFiles.map(file => uploadFile(file)))
            const response = await createUserAdmin({
                ...body,
                id_images: { images: idImageUrls },
            })
            $swal.close()
            await $swal.fire({
                icon: 'success',
                title: 'Success',
                text: response.message,
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
            })
            return { success: true, message: response.message }
        } catch (error: any) {
            const message = getApiErrorMessage(error, 'Failed to create the user.')
            $swal.close()
            await $swal.fire({
                icon: 'error',
                title: 'Creation Failed',
                text: message,
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff',
            })
            return { success: false, message }
        }
    }

    const handleUpdateUserStatus = async (
        userReference: string,
        isActive: boolean,
    ): Promise<AssignRoleResult> => {
        const action = isActive ? 'activate' : 'suspend'
        const confirmation = await $swal.fire({
            icon: 'warning',
            title: `${isActive ? 'Activate' : 'Suspend'} user?`,
            text: isActive
                ? 'The user will be able to sign in again.'
                : 'The user will no longer be able to access their account.',
            showCancelButton: true,
            confirmButtonText: isActive ? 'Activate' : 'Suspend',
            confirmButtonColor: '#C1121F',
            cancelButtonColor: '#333333',
            background: '#1a1a1a',
            color: '#ffffff',
        })
        if (!confirmation.isConfirmed) return { success: false, message: 'Cancelled.' }

        try {
            const response = await updateUserStatus(userReference, isActive)
            await $swal.fire({
                icon: 'success', title: 'Success', text: response.message,
                confirmButtonColor: '#C1121F', background: '#1a1a1a', color: '#ffffff',
            })
            return { success: true, message: response.message }
        } catch (error: any) {
            const message = getApiErrorMessage(error, `Failed to ${action} the user.`)
            await $swal.fire({
                icon: 'error', title: 'Action Failed', text: message,
                confirmButtonColor: '#C1121F', background: '#1a1a1a', color: '#ffffff',
            })
            return { success: false, message }
        }
    }

    const handleDeleteUser = async (
        userReference: string,
        userLabel: string,
    ): Promise<AssignRoleResult> => {
        const confirmation = await $swal.fire({
            icon: 'warning',
            title: 'Delete user permanently?',
            text: `${userLabel} and all related records will be permanently deleted. This cannot be undone.`,
            showCancelButton: true,
            confirmButtonText: 'Delete permanently',
            confirmButtonColor: '#C1121F',
            cancelButtonColor: '#333333',
            background: '#1a1a1a',
            color: '#ffffff',
            focusCancel: true,
        })
        if (!confirmation.isConfirmed) return { success: false, message: 'Cancelled.' }

        try {
            const response = await deleteUserAdmin(userReference)
            await $swal.fire({
                icon: 'success', title: 'Deleted', text: response.message,
                confirmButtonColor: '#C1121F', background: '#1a1a1a', color: '#ffffff',
            })
            return { success: true, message: response.message }
        } catch (error: any) {
            const message = getApiErrorMessage(error, 'Failed to delete the user.')
            await $swal.fire({
                icon: 'error', title: 'Delete Failed', text: message,
                confirmButtonColor: '#C1121F', background: '#1a1a1a', color: '#ffffff',
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

    const getApiErrorMessage = (
        error: any,
        fallback = 'Failed to update the user.',
    ): string => {
        const data = error?.data ?? error?.response?._data

        if (typeof data?.detail === 'string') return data.detail

        if (data && typeof data === 'object') {
            const firstError = Object.values(data).flat().find(
                value => typeof value === 'string'
            )

            if (typeof firstError === 'string') return firstError
        }

        return fallback
    }

    return {
        handleAssignRole,
        handleCreateUser,
        handleUpdateUserStatus,
        handleDeleteUser,
        handleEditUser
    }
}
