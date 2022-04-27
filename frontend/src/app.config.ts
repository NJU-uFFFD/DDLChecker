export default defineAppConfig({
  pages: [
    'pages/home/index',
    'pages/history/index',
    'pages/profile/index'
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#ffffff',
    backgroundColor: '#f9f9f9',
    navigationBarTitleText: 'WeChat',
    navigationBarTextStyle: 'black',
    // enablePullDownRefresh: true,
  },
  tabBar: {
    custom: false,
    color: '#bbbbbb',
    selectedColor: '#2c68ff',
    backgroundColor: '#ffffff',
    list: [
      {
        pagePath: 'pages/home/index',
        selectedIconPath: './assets/images/list-selected.png',
        iconPath: './assets/images/list.png',
        text: '首页'
      },
      {
        pagePath: 'pages/history/index',
        selectedIconPath: './assets/images/time-selected.png',
        iconPath: './assets/images/time.png',
        text: '历史'
      },
      {
        pagePath: 'pages/profile/index',
        selectedIconPath: './assets/images/profile-selected.png',
        iconPath: './assets/images/profile.png',
        text: '我的'
      },
    ],
  }
})
