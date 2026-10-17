export function useProfileUploads() {
    const { apiFetch } = useApiFetch()
    const { $swal } = useNuxtApp()

    const profileImage = ref<File | null>(null)
    const profilePreview = ref<string | null>(null)
    const uploadedIdFiles = ref<File[]>([])
    const originalIdImages = ref<string[]>([])
    const existingIdImages = ref<string[]>([])
    const deletedIdImages = ref<string[]>([])

    const idInput = ref<HTMLInputElement | null>(null)

    function triggerIdUpload() {
        idInput.value?.click()
    }

    function handleProfileChange(e: Event) {
        const input = e.target as HTMLInputElement
        const file = input.files?.[0]

        if (!file) return

        profileImage.value = file
        profilePreview.value = URL.createObjectURL(file)

        input.value = ''
    }

    function handleIdChange(e: Event) {
        const input = e.target as HTMLInputElement

        if (!input.files) return

        uploadedIdFiles.value.push(...Array.from(input.files))

        console.log('Uploaded ID files:', uploadedIdFiles.value)
        console.log('Uploaded ID files length:', uploadedIdFiles.value.length)

        console.log(uploadedIdFiles.value)
    }

    function handleIdDrop(e: DragEvent) {
        const files = e.dataTransfer?.files
        if (!files) return

        uploadedIdFiles.value.push(...Array.from(files))
    }

    function removeIdFile(index: number) {
        uploadedIdFiles.value.splice(index, 1)
    }

    const validateFile = async (file: File): Promise<boolean> => {
        const MAX_FILE_SIZE = 50 * 1024 * 1024
        const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'pdf']

        const extension = file.name.split('.').pop()?.toLowerCase()

        if (!extension || !ALLOWED_EXTENSIONS.includes(extension)) {
            $swal.close()

            await $swal.fire({
                icon: 'error',
                title: 'Invalid File',
                text: 'Only JPG, JPEG, PNG, and PDF files are allowed.',
                confirmButtonText: 'OK',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff'
            })

            return false
        }

        if (file.size > MAX_FILE_SIZE) {
            await $swal.fire({
                icon: 'error',
                title: 'File Too Large',
                text: 'File size must not exceed 50 MB.',
                confirmButtonText: 'OK',
                confirmButtonColor: '#C1121F',
                background: '#1a1a1a',
                color: '#ffffff'
            })

            return false
        }

        return true
    }

    const removeExistingId = (index: number, url: string) => {
        console.log("index:",index)
        console.log("url:",url)
        deletedIdImages.value.push(url)
        existingIdImages.value.splice(index, 1)
    }

    const uploadProfilePicture = async (): Promise<string | false | null> => {
        if (!profileImage.value) {
            return null
        }

        if (!(await validateFile(profileImage.value))) {
            return false
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
        idInput,
        triggerIdUpload,
        handleProfileChange,
        handleIdChange,
        handleIdDrop,
        removeIdFile
    }
}