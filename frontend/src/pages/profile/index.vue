<template>
  <view class="page">
    <scroll-view
      :scroll-y="true"
      style="height: 100vh;">

      <ProfileCard
        :nickname=nickname
        :avatarUrl=avatarUrl>
      </ProfileCard>


      <nut-cell-group
        title="账号管理"/>
      <nut-swipe v-for="data in account_list" :key="data.id">
        <AccountCard :accountData="data"/>
        <template #right>
          <nut-button
            style="height:100%; border-radius: 10px"
            type="danger"
            @click="state.showDelete=true;state.deleteInfo=data">
            删除
          </nut-button>
        </template>
      </nut-swipe>
      <AccountCard @click="addAccount"/>

      <nut-dialog
        title="删除账号"
        content="该账号下的 DDL 不会删除 ~"
        close-on-click-overlay
        lock-scroll
        v-model:visible="state.showDelete">
        <template #footer>
          <nut-button plain type="danger" @click="state.showDelete = false">取消</nut-button>
          <nut-button
            type="danger"
            @click="deleteAccount(state.deleteInfo);account_list = account_list.filter((x) => {return x.id !== state.deleteInfo.id})">
            删除
          </nut-button>
        </template>
      </nut-dialog>

      <nut-cell-group
        title="设置"/>
    </scroll-view>

    <!-- Toast -->
    <nut-toast
      :msg="toastInfo.msg"
      v-model:visible="toastInfo.show"
      :type="toastInfo.type"
      @closed="toastInfo.onClosed"
      :cover="toastInfo.cover"
      :duration="1000"
      bg-color="rgba(0, 0, 0, 0.5)"
      :center="false"
      bottom="16%"
    />
  </view>
</template>

<script>
import Taro from '@tarojs/taro';
import {ref, reactive, toRefs} from 'vue'
import AccountCard from "../../components/card/ProfileAccountCard.vue";
import ProfileCard from "../../components/card/ProfileProfileCard.vue";
import {AccountData} from "../../types/AccountData";
import {request} from "../../util/request";

export default {
  name: 'profile',
  components: {
    ProfileCard,
    AccountCard
  },
  data() {
    return {
      account_list: []
    }
  },
  setup() {
    const nickname = ref('Test Username')
    const avatarUrl = ref('../../assets/images/test_avatar.png')
    const state = reactive({
      "deleteInfo": {},
      "showDelete": false,
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


    function addAccount() {
      Taro.navigateTo({
        url: '/pages/accountadd/index'
      })
    }

    function deleteAccount(accountData) {
      state.showDelete = false
      console.log("删除账号 ID: " + accountData.id)
      const r = request({
        method: "POST",
        path: "/account/delete",
        data: {
          "id": accountData.id,
        }
      })

      r.then((res) => {
        if (res.statusCode === 200 && res.data.code === 0) {
          openToast('success', "删除成功!")
        } else {
          throw JSON.stringify(res)
        }
      }).catch((reason) => {
        Taro.showModal({
          title: '错误',
          content: '删除账号出错: ' + JSON.stringify(reason),
          showCancel: false
        })
      })
    }

    //消息通知
    const openToast = (type, msg, cover, title, bottom, center) => {
      toastInfo.show = true
      toastInfo.msg = msg
      toastInfo.type = type
      toastInfo.cover = cover
      toastInfo.title = title
      toastInfo.bottom = bottom
      toastInfo.center = center
    }

    return {
      nickname,
      avatarUrl,
      addAccount,
      deleteAccount,
      state,
      toastInfo,
      openToast,
      console
    }
  },
  beforeMount() {
    const r = request({
      path: "/account/list",
      method: "POST"
    })

    r.then((res) => {
      if (res.statusCode === 200 && res.data.code === 0) {
        this.account_list = res.data.data.account_list
      } else {
        throw JSON.stringify(res)
      }
    }).catch((reason) => {
      console.error(reason)
      Taro.showModal({
        title: '错误',
        content: '发生网络错误: ' + JSON.stringify(reason),
        showCancel: false
      })
    })
  }
}
</script>

<style>

.page {
  background: #f9f9f9;
}

.nut-cell-group__title {
  margin-top: 15px;
}

.nut-cell-group {
  height: 30px;
}

</style>
