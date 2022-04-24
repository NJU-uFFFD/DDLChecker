export default defineAppConfig({
  pages: [
    'pages/index/index',
    'pages/favo/index',
    'pages/my/index'
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#fff',
    navigationBarTitleText: 'WeChat',
    navigationBarTextStyle: 'black'
  },
  tabBar: {
    custom: false,
    color: '#000000',
    selectedColor: '#6190E8',
    backgroundColor: '#ffffff',
    list: [
      {
        pagePath: 'pages/index/index',
        selectedIconPath: 'images/home.png',
        iconPath: 'images/home-outline.png',
        text: '首页'
      },
      {
        pagePath: 'pages/favo/index',
        selectedIconPath: 'images/heart.png',
        iconPath: 'images/heart-outline.png',
        text: '喜欢'
      },
      {
        pagePath: 'pages/my/index',
        selectedIconPath: 'images/accessibility.png',
        iconPath: 'images/accessibility-outline.png',
        text: '个人'
      }
    ]
  }
})
