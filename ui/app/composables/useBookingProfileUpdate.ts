import type { User } from "~/utils/api/api"

interface BookingProfileForm {
    lastName: string
    address: string
    contact: string
}

interface UpdateUserProfileParams {
    user: User | null
    form: BookingProfileForm
    uploadedIdFiles: File[]
    existingIdImages: string[]
    originalIdImages: string[]
    validateFile: (file: File) => Promise<boolean>
    uploadIdFiles: () => Promise<string[]>
}

export function useBookingProfileUpdate() {
    const { apiFetch } = useApiFetch()

    async function updateUserProfile({
        user,
        form,
        uploadedIdFiles,
        existingIdImages,
        originalIdImages,
        validateFile,
        uploadIdFiles
    }: UpdateUserProfileParams): Promise<void> {

        const removedImages = originalIdImages.filter(
            url => !existingIdImages.includes(url)
        )

        if (uploadedIdFiles.length > 0) {
            for (const file of uploadedIdFiles) {
                if (!(await validateFile(file))) {
                    return
                }
            }

            const newIdUrls = await uploadIdFiles()

            const idUrls = [
                ...existingIdImages,
                ...newIdUrls
            ]

            const body: any = {
                id_images: {
                    images: idUrls
                }
            }

            if (!user?.family_name) {
                body.family_name = form.lastName
            }

            if (!user?.address) {
                body.address = form.address
            }

            if (!user?.contact_number) {
                body.contact_number = form.contact
            }

            if (removedImages.length > 0) {
                body.deleted_images = removedImages
            }

            await apiFetch('/auth/me/', {
                method: 'PATCH',
                body
            })
        }
    }

    return {
        updateUserProfile
    }
}