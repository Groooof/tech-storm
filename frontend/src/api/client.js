import axios from 'axios'

let refreshTokensPromise = null

export function jwtClient({
  options,
  getCurrentAccessToken,
  getCurrentRefreshToken,
  updateTokens,
  refreshTokenUrl,
  authApi,
  logout
}) {
  const client = axios.create(options)

  client.interceptors.request.use(
    (config) => {
      if (config.authorization !== false) {
        const token = getCurrentAccessToken()
        if (token) config.headers.Authorization = 'Bearer ' + token
      }
      return config
    },
    (error) => Promise.reject(error)
  )

  client.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response?.status !== 401) return Promise.reject(error)

      const refreshToken = getCurrentRefreshToken()
      if (!refreshToken) return Promise.reject(error)

      const originalRequest = error.config
      if (originalRequest?.url !== refreshTokenUrl && originalRequest?._retry !== true) {
        if (!refreshTokensPromise) {
          refreshTokensPromise = authApi(client)
            .refreshTokens(refreshToken)
            .then((response) => {
              refreshTokensPromise = null
              return {
                accessToken: response.data.access_token,
                refreshToken: response.data.refresh_token
              }
            })
            .catch(async () => {
              await logout()
              return Promise.reject(error)
            })
        }

        return refreshTokensPromise.then((newTokens) => {
          updateTokens(newTokens.accessToken, newTokens.refreshToken)
          originalRequest._retry = true
          return client(originalRequest)
        })
      }

      return Promise.reject(error)
    }
  )

  return client
}
