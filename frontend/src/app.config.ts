export default defineAppConfig({
  pages: [
    'pages/index/index',
    'pages/favo/index',
    'pages/my/index'
    'pages/home/index',
    'pages/history/index',
    'pages/profile/index'
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#fff',
    navigationBarBackgroundColor: '#f6f6f6',
    navigationBarTitleText: 'WeChat',
    navigationBarTextStyle: 'black'
    navigationBarTextStyle: 'black',
    enablePullDownRefresh: true,
  },
  tabBar: {
    custom: true,
    color: '#000000',
    selectedColor: '#6190E8',
    custom: false, /*  若开启custom，需编辑/custom-tab-bar中文件，渲染会很卡，暂不使用  */
    color: '#bbbbbb',
    selectedColor: '#2c68ff',
    backgroundColor: '#ffffff',
    list: [
      {
        pagePath: 'pages/index/index',
        selectedIconPath: 'images/home.png',
        iconPath: 'images/home-outline.png',
        pagePath: 'pages/home/index',
        selectedIconPath: './assets/images/list-selected.png',
        iconPath: './assets/images/list.png',
        text: '首页'
      },
      {
        pagePath: 'pages/favo/index',
        selectedIconPath: 'images/heart.png',
        iconPath: 'images/heart-outline.png',
        text: '喜欢'
        pagePath: 'pages/history/index',
        selectedIconPath: './assets/images/time-selected.png',
        iconPath: './assets/images/time.png',
        text: '历史'
      },
      {
        pagePath: 'pages/my/index',
        selectedIconPath: 'images/accessibility.png',
        iconPath: 'images/accessibility-outline.png',
        text: '个人'
      }
    ]
        pagePath: 'pages/profile/index',
        selectedIconPath: './assets/images/profile-selected.png',
        iconPath: './assets/images/profile.png',
        text: '我的'
      },
    ],
  }
})
