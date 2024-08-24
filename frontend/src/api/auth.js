export const api = (client) =>
  Object({
    async refreshTokens(refreshToken) {
      const url = '/tokens/refresh'
      const requestBody = { refresh_token: refreshToken }
      return await client.post(url, requestBody)
    },
    async getTokens(username, password) {
      console.log(username, password)
      const url = '/tokens'
      const requestBody = { username: username, password: password }
      return await client.post(url, requestBody, { authorization: false })
    },
    async logout(refreshToken) {
      const url = '/tokens/delete'
      const requestBody = { refresh_token: refreshToken }
      return await client.post(url, requestBody)
    }
  })
