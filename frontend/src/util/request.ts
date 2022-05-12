import Taro from "@tarojs/taro";
import {WX_SERVICE, USE_CONTAINER, SERVER_ADDR, TEST_WX_OPENID} from "../config"

// 封装一下发起请求的部分, 便于本地测试时调用
function request(args) {
  if (USE_CONTAINER) {

    // 添加需要的 header
    if (args.header === undefined) {
      args.header = {
        'X-WX-SERVICE': WX_SERVICE,
      }
    } else {
      args.header['X-WX-SERVICE'] = WX_SERVICE
    }

    return Taro.cloud.callContainer(args)
  } else{

    // 不使用容器服务, 本地测试
    args.url = SERVER_ADDR + args.path
    // 使用测试用 OPENID
    if (args.header === undefined) {
      args.header = {
        'X-WX-OPENID': TEST_WX_OPENID,
      }
    } else {
      args.header['X-WX-OPENID'] = TEST_WX_OPENID
    }
    return Taro.request(args)
  }
}


export {request}
