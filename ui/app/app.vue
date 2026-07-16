<template>
  <div>
    <NuxtPage />
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { setAuth } = useAuth()

onMounted(async () => {
    const access = route.query.access
    const refresh = route.query.refresh

    if (access && refresh) {
        await setAuth(access as string, refresh as string)
    }
})
</script>