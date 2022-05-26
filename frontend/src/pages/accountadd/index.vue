<template>
  <nut-cell>选择需要添加的账号</nut-cell>

  <!-- 账号列表 -->
  <div v-for="data in accounts" :key="data">
    <AccountCard
      :accountData=data
      description="点击添加"
      @onClick="addAccountPopup"
    />
  </div>

  <!-- 弹出层 -->
  <nut-overlay
    v-model:visible="state.showPopup"
    :close-on-click-overlay="false">
    <div class="content">
      <nut-form>
        <nut-form-item
          v-for="field in fields"
          :key="field"
          :label="field.title">
          <input
            :id="field.key"
            class="nut-input-text"
            :placeholder="field.detail"
            :type="field.key !== 'password' ? 'text': 'password'"/>
        </nut-form-item>
      </nut-form>

      <nut-button
        size="large"
        type="info"
        @click="submitAccount(field)">
        添加
      </nut-button>
    </div>
  </nut-overlay>
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
      showPopup: false
    })

    function addAccountPopup(data) {
      state.showPopup = true
      const d = data.fields
      console.log(d)
      form_fields.fields = []
      for (const name in d) {
        form_fields.fields.push({"key": name, "title": d[name].name, "detail": d[name].detail})
      }
      console.log(form_fields)
    }

    function submitAccount(data) {
      console.log(data)
    }

    return {
      ...toRefs(form_fields),
      state,
      addAccountPopup,
      submitAccount
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
.content {
  position: fixed;
  top: 30vh;
  right: 2vw;
  width: 96vw;
}
</style>
