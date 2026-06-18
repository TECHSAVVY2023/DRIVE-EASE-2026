<template>
    <ClientOnly>
        <div id="fb-root"></div>

        <div
            id="fb-customer-chat"
            class="fb-customerchat"
        ></div>
    </ClientOnly>
</template>

<script setup>
onMounted(() => {
    const chatbox = document.getElementById('fb-customer-chat')

    if (chatbox) {
        chatbox.setAttribute('page_id', '1234732813046839')
        chatbox.setAttribute('attribution', 'biz_inbox')
    }

    if (!window.FB) {
        const script = document.createElement('script')
        script.src =
        'https://connect.facebook.net/en_US/sdk/xfbml.customerchat.js'
        script.async = true
        script.defer = true
        document.body.appendChild(script)
    }
})
</script>

