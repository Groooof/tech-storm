export const api = (client) =>
    Object({
      async getCurrentUserData() {
        const url = '/users/me'
        return await client.get(url)
      },
      async getCurrentUserMessages() {
        const url = '/users/me/messages'
        return await client.get(url)
      }
    })
  