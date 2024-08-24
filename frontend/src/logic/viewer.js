import api from '../api'
import { useViewerData } from '@/stores/viewer'

export const login = async (username, password) => {
  const { authData, userData } = useViewerData()
  const tokensResp = await api.auth.getTokens(username, password)
  authData.accessToken = tokensResp.data.access_token
  authData.refreshToken = tokensResp.data.refresh_token
  const userResp = await api.users.getCurrentUserData()
  userData.id = userResp.data.id
  userData.username = userResp.data.username
}


