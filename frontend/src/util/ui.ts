function getAccountIcon(uuid: string): string {
  const table = {
    "f15684f5-d870-4a9d-b859-e7eec3c6e3b5": "/assets/images/jxlf.png",
  }
  return table[uuid] || "/assets/images/hand.png"
}

export {getAccountIcon}
