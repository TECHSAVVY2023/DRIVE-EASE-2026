export function useProfileEdit() {
    const { apiFetch } = useApiFetch()

    const profileImage = ref<File | null>(null)
    const profilePreview = ref<string | null>(null)
    const uploadedIdFiles = ref<File[]>([])
    const originalIdImages = ref<string[]>([])
    const existingIdImages = ref<string[]>([])
    const deletedIdImages = ref<string[]>([])

    const profileInput = ref<HTMLInputElement | null>(null)
    const idInput = ref<HTMLInputElement | null>(null)

    function triggerProfileUpload() {
        profileInput.value?.click()
    }

    function triggerIdUpload() {
        idInput.value?.click()
    }

    function handleProfileChange(e: Event) {
        const input = e.target as HTMLInputElement

        if (!input.files) return

        profileImage.value = input.files[0]

        const file = input.files[0]

        profileImage.value = file
        profilePreview.value = URL.createObjectURL(file)
    }

    function handleIdChange(e: Event) {
        const input = e.target as HTMLInputElement

        if (!input.files) return

        uploadedIdFiles.value.push(...Array.from(input.files))

        console.log('Uploaded ID files:', uploadedIdFiles.value)
        console.log('Uploaded ID files length:', uploadedIdFiles.value.length)
    }

    function handleIdDrop(e: DragEvent) {
        const files = e.dataTransfer?.files
        if (!files) return

        uploadedIdFiles.value.push(...Array.from(files))
    }

    function removeIdFile(index: number) {
        uploadedIdFiles.value.splice(index, 1)
    }

    const validateFile = (file: File): boolean => {
        
        const MAX_FILE_SIZE = 50 * 1024 * 1024 //
        const ALLOWED_TYPES = [
            'image/jpeg',
            'image/png',
            'image/jpg'
        ]

        if (!ALLOWED_TYPES.includes(file.type)) {
            alert('Only JPG, PNG, and WEBP images are allowed.')
            return false
        }

        if (file.size > MAX_FILE_SIZE) {
            alert('Image size must not exceed 50 MB.')
            return false
        }

        return true
    }

    const removeExistingId = (index: number, url: string) => {
        deletedIdImages.value.push(url)
        existingIdImages.value.splice(index, 1)
    }

    const uploadProfilePicture = async () => {
        if (!profileImage.value) {
            return null
        }

        if (!validateFile(profileImage.value)) {
            return
        }

        const fd = new FormData()
        fd.append('file', profileImage.value)

        const res = await apiFetch<{ url: string }>('/uploads/', {
            method: 'POST',
            body: fd
        })

        return res.url
    }

    const uploadIdFiles = async () => {
        return await Promise.all(
            uploadedIdFiles.value.map(async (file) => {
                const fd = new FormData()
                fd.append('file', file)

                const res = await apiFetch<{ url: string }>('/uploads/', {
                    method: 'POST',
                    body: fd
                })

                return res.url
            })
        )
    }

    return {
        uploadProfilePicture,
        uploadIdFiles,
        uploadedIdFiles,
        existingIdImages,
        originalIdImages,
        removeExistingId,
        profileImage,
        validateFile,
        profilePreview,
        profileInput,
        idInput,
        triggerProfileUpload,
        triggerIdUpload,
        handleProfileChange,
        handleIdChange,
        handleIdDrop,
        removeIdFile
    }
}