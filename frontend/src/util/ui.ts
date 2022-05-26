function getPlatformInfo(uuid: string): string {
  const table = {
    "f15684f5-d870-4a9d-b859-e7eec3c6e3b5": {
      "icon": "/assets/images/jxlf.png",
      "name": "教学立方"
    },
    "68dc1014-7bfe-4ea3-a000-5734303d9f59": {
      "icon": "/assets/images/spoc.png",
      "name": "南大SPOC"
    }
  }
  return table[uuid] || {"icon": "/assets/images/hand.png", "name": "手动添加"}
}

export {getPlatformInfo}
