const path = require('path');
const config = {
  projectName: 'frontend',
  date: '2022-4-15',
  designWidth: 375,
  deviceRatio: {
    640: 2.34 / 2,
    750: 1,
    828: 1.81 / 2,
    375: 2,
  },
  plugins: ['@tarojs/plugin-html'],
  sass: {
    resource: [
      path.resolve(__dirname, '..', 'src/assets/styles/custom_theme.scss')
    ],
    // 默认京东 APP 10.0主题 > @import "@nutui/nutui-taro/dist/styles/variables.scss";
    // 京东科技主题 > @import "@nutui/nutui-taro/dist/styles/variables-jdt.scss";
    data: `@import "@nutui/nutui-taro/dist/styles/variables.scss";`
  },
  sourceRoot: 'src',
  outputRoot: 'dist',
  defineConstants: {},
  copy: {
    patterns: [
      {from: 'src/assets/images/', to: 'dist/assets/images/'},
    ],
    options: {}
  },
  framework: 'vue3',
  mini: {
    postcss: {
      pxtransform: {
        enable: true,
        config: {}
      },
      url: {
        enable: true,
        config: {
          limit: 1024 // 设定转换尺寸上限
        }
      },
      cssModules: {
        enable: false, // 默认为 false，如需使用 css modules 功能，则设为 true
        config: {
          namingPattern: 'module', // 转换模式，取值为 global/module
          generateScopedName: '[name]__[local]___[hash:base64:5]'
        }
      }
    }
  },
  h5: {
    publicPath: '/',
    staticDirectory: 'static',
    postcss: {
      autoprefixer: {
        enable: true,
        config: {}
      },
      cssModules: {
        enable: false, // 默认为 false，如需使用 css modules 功能，则设为 true
        config: {
          namingPattern: 'module', // 转换模式，取值为 global/module
          generateScopedName: '[name]__[local]___[hash:base64:5]'
        }
      }
    }
  }
}

module.exports = function (merge) {
  if (process.env.NODE_ENV === 'development') {
    return merge({}, config, require('./dev'))
  }
  return merge({}, config, require('./prod'))
}
