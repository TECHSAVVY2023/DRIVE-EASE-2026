export const uploadFile = async (file: File) => {
    const { apiFetch } = useApiFetch()

    const fd = new FormData()
    fd.append('file', file)

    const res = await apiFetch<{ url: string }>('/uploads/', {
        method: 'POST',
        body: fd,
    })

    return res.url
}