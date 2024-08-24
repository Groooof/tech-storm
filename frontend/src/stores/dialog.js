import { reactive } from 'vue'
import { defineStore } from 'pinia'

export const useDialogData = defineStore('dialog', () => {
  const dialogData = reactive({
    msgs: [],
  })

  const clearDialogData = () => {
    dialogData.msgs = []
  }

  return {
    clearDialogData, dialogData
  }
})
