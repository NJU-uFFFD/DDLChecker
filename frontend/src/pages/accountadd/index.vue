<template>
  <view class="page">
    <!-- 账号列表 -->
    <scroll-view :scroll-y="true" style="height: 100vh;">
      <nut-cell-group title="选择需要添加的账号"/>
      <AccountCard
        v-for="data in accounts"
        :key="data"
        :accountData=data
        description="点击添加"
        @onClick="addAccountPopup"
      />
    </scroll-view>

    <!-- 弹出层 -->
    <nut-overlay v-model:visible="state.showPopup" :close-on-click-overlay="false">
      <div class="content">
        <nut-form>
          <nut-form-item
            v-for="field in fields" :key="field"
            :label="field.title"
            label-width="60px"
            label-align="center"
            body-align="center">
            <input
              :id="field.key"
              class="nut-input-text"
              :placeholder="field.detail"
              :type="field.key !== 'password' ? 'text': 'password'"/>
          </nut-form-item>
        </nut-form>


        <nut-button type="info" plain
          style="height:6vh;width:40vw;left:6.6vw;bottom:35vh;position:fixed;"
          @click="state.showPopup = false">
          取消
        </nut-button>
        <nut-button type="info"
          style="height:6vh;width:40vw;right:6.6vw;bottom:35vh;position:fixed;"
          @click="submitAccount()">
          添加
        </nut-button>
      </div>
    </nut-overlay>
  </view>
</template>

<script>
import AccountCard from "../../components/card/ProfileAccountCard"
import {request} from "../../util/request";
import Taro from "@tarojs/taro";
import {reactive, toRef, toRefs} from "vue";


export default {
  name: "index",
  components: {
    AccountCard,
  },
  data() {
    return {
      accounts: []
    }
  },
  setup() {
    let form_fields = reactive({fields: []});
    let state = reactive({
      showPopup: false,
      platform_uuid: undefined,
      input: {},
      adding: false
    })

    let toastInfo = reactive({
      msg: 'toast',
      type: 'text',
      show: false,
      cover: false,
      title: '',
      bottom: '',
      center: true,
    })

    const openToast = (type, msg, cover = false, title = "", bottom = "", center = true) => {
      toastInfo.show = true
      toastInfo.msg = msg
      toastInfo.type = type
      toastInfo.cover = cover
      toastInfo.title = title
      toastInfo.bottom = bottom
      toastInfo.center = center
    }

    function addAccountPopup(data) {

      if (data.bound) {
        Taro.showModal({
          title: '提示',
          content: '每门课程只能绑定一个账号, 请取消绑定当前账号再试.',
          showCancel: false
        })
        return
      }

      state.showPopup = true
      state.platform_uuid = data.platform_uuid
      const d = data.fields
      console.log(d)
      form_fields.fields = []
      for (const name in d) {
        form_fields.fields.push({"key": name, "title": d[name].name, "detail": d[name].detail})
        state.input[name] = ""
      }
      console.log(form_fields)
    }

    function submitAccount() {

      state.adding = true

      const r = request({
        method: "POST",
        path: "/account/add",
        data: {
          platform_uuid: state.platform_uuid,
          fields: state.input
        }
      })

      r.then((res) => {
        if (res.statusCode === 200 && res.data.code === 0) {
          openToast('success', "添加成功!")
          Taro.navigateBack()
        } else {
          throw JSON.stringify(res)
        }
      }).catch((reason) => {
        Taro.showModal({
          title: '错误',
          content: '添加账号出错: ' + JSON.stringify(reason),
          showCancel: false
        })
      }).finally(() =>
        state.adding = false
      )
    }

    return {
      ...toRefs(form_fields),
      state,
      addAccountPopup,
      submitAccount,
      toastInfo
    }
  },
  beforeMount() {
    const r = request({
      path: "/account/available",
      method: "POST"
    })

    r.then((res) => {
      if (res.statusCode === 200 && res.data.code === 0) {
        this.accounts = res.data.data.available_account_type
        console.log(this.accounts)
      } else {
        throw JSON.stringify(res)
      }
    }).catch((reason) => {
      console.error(reason)
      Taro.showModal({
        title: '错误',
        content: '发生网络错误: ' + JSON.stringify(reason),
        showCancel: false,
        success: () => {
          Taro.navigateBack()
        }
      })
    })
  }

}

</script>

<style>
.page {
  background-color: #f9f9f9;
}

.content {
  position: fixed;
  top: 35vh;
  right: 2vw;
  width: 96vw;
}

/*表单内行高设置*/
.nut-cell {
  line-height: normal;
}

.nut-cell-group__title {
  margin-top: 15px;
}

.nut-cell-group {
  height: 30px;
}

</style>
