<template>
  <div>
    <NuxtPage />
  </div>
</template>

<script setup lang="ts">
const { init } = useAuth()

onMounted(() => {
    init()
})
</script>
