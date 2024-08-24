import api from '@/api'
import { useDialogData } from '@/stores/dialog.js'


export const loadMessages = async function () {
    const resp = await api.users.getCurrentUserMessages()
    const messagesApiData = await resp.data
  
    const { dialogData } = useDialogData()
    dialogData.msgs = []
    messagesApiData.forEach((messageApiData) => {
      const messageData = {
        id: messageApiData.id,
        type: messageApiData.type_,
        text: messageApiData.text
      }
      dialogData.msgs.push(messageData)
    })
  }