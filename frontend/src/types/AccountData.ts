export interface AccountData {
  id: number
  userid: number
  platform_uuid: string
  fields: {
    key: string
    title: string
    detail: string
  }[]
}
