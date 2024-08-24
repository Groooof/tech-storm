<template>
  <div class="dialog-msg-block" :style="{alignSelf: alignSelf}">
    <span :style="{alignSelf: alignSelfTitle}">{{ title }}</span>
    <div class="msg-frame" :style="{textAlign:textAlign, backgroundColor: backgroundColor}">
      <slot></slot>
    </div>
  </div>
  
</template>

<script setup>

const props = defineProps({
    type: String, // [question;answer]
})

const alignSelf = props.type === 'answer' ? 'self-start' : 'self-end'
const alignSelfTitle = props.type === 'answer' ? 'self-start' : 'self-end'
const textAlign = props.type === 'answer' ? 'start' : 'end'
const backgroundColor = props.type === 'answer' ? '#e5f9f6' : '#e2eaf6'
const title = props.type === 'answer' ? 'Ответ' : 'Вопрос'
</script>

<style>
.dialog-msg-block span {
  font-weight: 700;
  font-size: 0.8em;
  margin: 0 14px;
}

.dialog-msg-block {
  display: flex;
  flex-direction: column;
  gap: 5px;
  max-width: 70%;
  width: fit-content;
}

.msg-frame {
  padding: 10px 20px;
  border-radius: 18px;
}
</style>