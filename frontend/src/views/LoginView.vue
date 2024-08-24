<template>
  <div class="container-center">
    <fieldset class="form-card">
      <legend>Авторизация</legend>
      <div class="form-card-content-wrapper">
        <div class="form-input">
          <div class="form-input-label">Имя пользователя</div>
          <input v-model="authData.username" @keyup.enter="onSubmit" @click="onInputClick" />
        </div>
        <div class="form-input">
          <div class="form-input-label">Пароль</div>
          <input
            type="password"
            v-model="authData.password"
            @keyup.enter="onSubmit"
            @click="onInputClick"
          />
        </div>
        <div class="form-submit-row">
          <div class="form-alert">{{ alert }}</div>
          <div class="form-submit-btn" @click="onSubmit">Войти</div>
        </div>
      </div>
    </fieldset>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/logic/viewer'

const authData = {
  workNumber: null,
  password: null
}
const alert = ref(null)
const router = useRouter()

const onInputClick = () => {
  alert.value = null
}

const onSubmit = () => {
  if (authData.username && authData.password) {
    login(authData.username, authData.password)
      .then(() => router.push({ name: 'main' }))
      .catch((error) => {
        if (
          error.response &&
          error.response.status === 400 &&
          error.response.data.detail === 'WRONG_CREDENTIALS'
        ) {
          alert.value = 'Такой учетной записи не существует!'
        }
      })
  }
}
</script>

<style>
.form-alert {
  font-size: 12px;
  color: #d64057;
}

.form-submit-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-submit-btn:active {
  transform: scale(0.95);
}

.form-submit-btn:hover {
  background-color: #dedede;
}

.form-submit-btn {
  border: 2px solid black;
  width: fit-content;
  padding: 0px 10px;
  cursor: pointer;
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}

.form-input {
  display: flex;
  gap: 15px;
  justify-content: space-between;
}

.form-card {
  border: 2px solid black;
  padding: 0 10px;
}

.form-card-content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
  height: 100%;
  padding: 10px;
}

.container-center {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
