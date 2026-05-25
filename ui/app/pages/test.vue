<script setup>
const config = useRuntimeConfig()

console.log('API BASE:', config.public.apiBase)
</script>

<template>
  <div>
    API BASE: {{ config.public.apiBase }}
  </div>
</template>