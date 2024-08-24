import {
  getCurrentAccessToken,
  getCurrentRefreshToken,
  updateTokens,
} from '@/lib/tokens.js'
import { jwtClient } from '@/api/client.js'
import { api as authApi } from '@/api/auth.js'
import { api as usersApi } from '@/api/users.js'
import { useDialogData } from '@/stores/dialog.js'

const BASE_URL = import.meta.env.VITE_BACKEND_URL + '/api/v1'

const clientOptions = {
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
}

export const logout = async () => {
  const { authData } = useViewerData()
  const { clearViewerData } = useViewerData()
  const { clearDialogData } = useDialogData()
  await api.auth.logout(authData.refreshToken)
  window.location.replace('/login')
  clearDialogData()
  clearViewerData()
}

const client = jwtClient({
  options: clientOptions,
  refreshTokenUrl: '/tokens/refresh',
  getCurrentAccessToken,
  getCurrentRefreshToken,
  updateTokens,
  authApi,
  logout
})

const api = {
  auth: authApi(client),
  users: usersApi(client),
}

export default api
