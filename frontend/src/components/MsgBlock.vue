<template>
    <div class="msg-block">
        <div class="msg-input-frame">
            <textarea class="msg-input-textarea" @keydown.enter.exact.prevent="sendMsg" v-model="inputText" rows="1" ref="inputTextarea"></textarea>
            <img @click="sendMsg" class="send-btn" width=25px height="25px"
                src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADwAAAA8CAYAAAA6/NlyAAAACXBIWXMAAAsTAAALEwEAmpwYAAAFMklEQVR4nOWbDYhUVRTHf7PrR6ZZW5jpRlnZh6ZRLdkXLEWLFWYUfVBRFhhmIW1QIVSESPQhVBQViRUlUpRFCIlZ9k1llEWZJWWFG1mWFpltq7YzceJcODzmvXn3zZ2ZN7t/ODAz797zzv9+nXPPvQODC60MMBSAg2KeDQXmMkAwFrgJuBIYXub5MOBl4GKaGC1AF/AC8DZwrHl2AjBeP0sDrAC2aC83HWTIzge+A3bqZzc39wUWAqfo972B14ASsIAm7c3dSuAV4BBTZiawHjhZv48E1mjZPUA7TYDx2oM/qOEivwCzTJlxwHLgd+Ak/W0U8Jap8yJN0pt7jNFFYClwgFmRhfh2YCtwnP6+H/ChqVcCziKHaNfe3BwxVmSTNoLDROBN0+NT9Pc24KNI3W+0cXKBVtOb/5YhKj38kM5HdJWVRunT5z3AkfrsQODzMjq6yQEm6qrZU8ZAJ58BHabOqcCX5rmMhCOMH15fRkcvsH+DOP7v/C8BXtf5GEf074irEddyb2QEyCJ2mHFTG2J0LWkE0aPU4F8TSDpZBUwwdWeUmdMbjYsRt/Rtgr6OepEcnrI3nYhLmWPqj9UVOVruKxNBScN8n6BzbT2IHqO9+VsKkk5kwRoTcTXbYub0GDNqfqyg9+pakdzLszedSO+cbfQcrjrKlV1n/K806k8VdG9Tu4Jisvbmdg+SIv3AYo2GBEPUdeyMKf+xWWnlnT+neMeiUCRHmN4sZRDxk9OMvuOVUFz594DRZgeUZqoUjW/OjA7tlR0Zifaq3xXXFOdqovKOGQUdHiNJVvpMGK0r57qMJK3hRxu9Z2i4V8loGU2C04E/Pd53ftbe/KtKon9ogxVMnLs4Rb2VZsHp9BxVm33zVpPVsZeqlOfUlzpclXL+vWSG/XSdCj7vvZ0MGBoJ0H1E3MWFRpeEf6+mrPu8ScGcC/zj+e5dkUb2hmy5Pkj5sqIO133MnnaOx7R4Vt2T4LyMjS06qkYLMK/CPPrC5JCcq/nEw9Al+h7BpSaF4ysy34NhnKZJ7At2q2txadER6np2eRj5uCF7WSTD4SMbarXJn6kxrAQEk8zvnRkWu0eNkbM1AitllOupIUYZQyXke8ozhha5x+ibm6G+lR0mGqspLtJ8kq+BNj/cXSVZkceoEx7MYNydpv4tVRJ1MrWeeal+D8NuM3XnByL7LnXGqhRGFSOZwwWByIpcHppQC3BazImcCxKSDOqPpG4WBSS71YShQdAKLFPl9yU0SFxeSbZ+12i5guaXSwHl7lqR7QcuSCh7a4xBD5gy1wYmK415aEiySw3ZSsmwNs0lR40St2XRFXMykEVWNIqsw5NljHLnPdEpMCtlXipJzqGBZN2GIbpYJWUNR6prypJk2GTi74aQdXg/YlQatOu2Mim3FRUJWBpOVnBFJE3jm2lZmYJsn0nGZ8YThqw9WffFMBNb2xXaBzMSDsZEniEAegKQdViohl1XhY4hWr/cxsQmGjJjgi46IdCum3hJxVYLSRfdZVzep+QUyxNuw2XBwcDTmiTIJU5kAKGgOWZ3PWhAowA8ovPpawYR2SJwQyC9k/RUMNdkuwPpna6nC30mgT/gyZaA1Xm5OFYAHq4R2V5zlOounTUUhcFEVnBzjYfxGnPgnQvM0xDxxkD6puSZrIM7vgyBaXr4tjovZAt63rNWb6XWAm0hMhWhXU8pYCDQpQuTXErJFe43C5T8FSYEOs1qfAc5w5bAqzGa8RCyb+idrFxhKnBmYJ3ydxq5vhD8vmO1+A9LpwyL7TESjAAAAABJRU5ErkJggg==">
        </div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useDialogData } from '@/stores/dialog.js'

const inputTextarea = ref(null)
const inputText = ref('')
const emit = defineEmits([
  'sendMsg'
])

const resizeInputTextarea = function () {
  if (inputTextarea.value) {
    inputTextarea.value.style.height = 'auto'
    inputTextarea.value.style.height = inputTextarea.value.scrollHeight + 'px'
  }
  if (!inputText.value.trim()) {
    inputText.value = ''
    inputTextarea.value.style.height = 'auto'
  }
}

const sendMsg = function () {
  const text = inputText.value
  inputText.value = ''
  if (!text.trim()) return

  emit('sendMsg', text)
  const { dialogData } = useDialogData()
  const msg = {
    'id': -1,
    'type': 'question',
    'text': text
  }
  dialogData.msgs.push(msg)
}

watch(inputText, (newValue, oldValue) => {
  resizeInputTextarea()
})
</script>

<style>
.send-btn {
  margin: 0 10px;
  align-self: self-end;
}

.msg-input-textarea {
  flex-grow: 1;
  border: none;
  outline: none;
  resize: none;
  font: inherit;
  font-size: 18px;
  max-height: 150px;
}

.msg-input-frame {
  padding: 14px;
  border: 1px solid #7394d3;
  border-radius: 20px;
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
}
</style>