function getPlatformInfo(uuid: string): string {
  const table = {
    "f15684f5-d870-4a9d-b859-e7eec3c6e3b5": {
      "icon": "/assets/images/jxlf.png",
      "name": "教学立方"
    },
    "68dc1014-7bfe-4ea3-a000-5734303d9f59": {
      "icon": "/assets/images/spoc.png",
      "name": "南大SPOC"
    },
    "69921ef9-fe15-4731-930d-b60a644da254": {
      "icon": "/assets/images/mooc.png",
      "name": "中国大学MOOC"
    },
    "00000000-0000-0000-0000-000000000000": {
      "icon": "/assets/images/hand.png",
      "name": "手动添加"
    }
  }
  return table[uuid] || {"icon": "/assets/images/hand.png", "name": "手动添加"}
}


function formatTime(timestamp: number): string {
  const weekdayZhCN = {"0": "日", "1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六"}
  const t = new Date(timestamp)

  return String(`${t.getFullYear()}年${t.getMonth() + 1}月${t.getDate()}日
          星期${weekdayZhCN[t.getDay()]}
          ${t.getHours() > 9 ? t.getHours() : "0" + t.getHours()}:
          ${t.getMinutes() > 9 ? t.getMinutes() : "0" + t.getMinutes()}`)
}

export {getPlatformInfo, formatTime}
