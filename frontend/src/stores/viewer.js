import { defineStore } from 'pinia'
import { computed, reactive } from 'vue'
import { useLocalStorage, StorageSerializers } from '@vueuse/core'

export const useViewerData = defineStore('viewer', () => {

  const authData = reactive({
    accessToken: useLocalStorage('_viewer_accessToken', null),
    refreshToken: useLocalStorage('_viewer_refreshToken', null),
  })

  const userData = reactive({
    id: useLocalStorage('_viewer_id', null, { serializer: StorageSerializers.number }),
    username: useLocalStorage('_viewer_username', null),
  })

  const isAuthenticated = computed(() => authData.accessToken && authData.refreshToken)

  const clearViewerData = () => {
    userData.id = null
    userData.username = null
  }

  return {
    authData,
    userData,
    isAuthenticated,
    clearViewerData
  }
})
