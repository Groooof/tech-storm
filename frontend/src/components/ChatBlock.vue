<template>
    <div class="chat-block" ref="chatBlock">
        <msg v-for="msg in dialogData.msgs" :key="msg.id" :type="msg.type">
            {{ msg.text }}
        </msg>
    </div>
</template>

<script setup>
import { ref, onUpdated } from 'vue'
import Msg from '@/components/Msg.vue'
import { useDialogData } from '@/stores/dialog.js'

const { dialogData } = useDialogData()
const chatBlock = ref(null)

const resize = function () {
    chatBlock.value.scrollTop = chatBlock.value.scrollHeight
}

onUpdated(() => {
    resize()
})

defineExpose({ resize })
</script>

<style>
.chat-block {
  display: flex;
  overflow-y: auto;
  padding: 20px;
  flex-direction: column;
  gap: 20px;
}
</style>