<template>
  <div class="container">
    <div class="container-spacer">
      <chat-block></chat-block>
      <msg-block @sendMsg="onSendMsg"></msg-block>
    </div>
  </div>
</template>

<script setup>
import MsgBlock from '@/components/MsgBlock.vue'
import ChatBlock from '@/components/ChatBlock.vue'
import { useDialogData } from '@/stores/dialog.js'
import { useViewerData } from '@/stores/viewer.js'
import { loadMessages } from '@/logic/messages.js'
import { onMounted } from 'vue'

const { dialogData } = useDialogData()
const { userData } = useViewerData()

onMounted(loadMessages)

var ws = new WebSocket("ws://192.168.87.146:8081/api/v1/messages/ws");

const onSendMsg = function (text) {
  ws.onmessage = function(event) {
    const data = JSON.parse(event.data)
    const lastMsg = dialogData.msgs[dialogData.msgs.length - 1]
    if (data.type === 'message_id') {
      if (lastMsg.id === -1) {
        lastMsg.id = data.data
      }
    } else
    if (data.type === 'answer') {
      const msg = {'id': data.data.id, 'type': 'answer', 'text': data.data.text}
      console.log(msg)
      if (lastMsg.id === msg.id) {
        lastMsg.text = lastMsg.text + msg.text
      } else {
        dialogData.msgs.push(msg)
      }
    }
};

  const data = JSON.stringify({'user_id': userData.id, 'text': text})
  ws.send(data)
}

</script>

<style>
.container {
  height: 100%;
  display: flex;
  justify-content: center;
  background-color: #f5f5f5;
}

.container-spacer {
  background-color: #ffffff;
  border: 1px solid #e2eaf6;
  border-radius: 20px;
  margin: 10px 0;
  display: flex;
  flex-direction: column;
  max-width: 1200px;
  width: 100%;
  padding: 30px 40px;
  gap: 10px;
  justify-content: end;
}
</style>
