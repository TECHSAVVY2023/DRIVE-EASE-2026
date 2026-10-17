export default defineNuxtPlugin(async () => {
    const { init } = useAuth()
    
    onNuxtReady(() => {
        init()
    })
})