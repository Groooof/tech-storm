import { useViewerData } from '@/stores/viewer'

export const getCurrentAccessToken = () => {
  const { authData } = useViewerData()
  return authData.accessToken
}
export const getCurrentRefreshToken = () => {
  const { authData } = useViewerData()
  return authData.refreshToken
}
export const updateTokens = (accessToken, refreshToken) => {
  const { authData } = useViewerData()
  authData.accessToken = accessToken
  authData.refreshToken = refreshToken
}
