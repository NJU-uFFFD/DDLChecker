export default defineAppConfig({
  pages: [
    'pages/ddl_list/index',
    'pages/history/index',
    'pages/profile/index'
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#f6f6f6',
    navigationBarTitleText: 'WeChat',
    navigationBarTextStyle: 'black',
    enablePullDownRefresh: true,
  },
  tabBar: {
    custom: false, /*  若开启custom，需编辑/custom-tab-bar中文件，渲染会很卡，暂不使用  */
    color: '#bbbbbb',
    selectedColor: '#2c68ff',
    backgroundColor: '#ffffff',
    list: [
      {
        pagePath: 'pages/ddl_list/index',
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
