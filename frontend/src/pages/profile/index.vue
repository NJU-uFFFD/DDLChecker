<template>
  <view class="page">
    <scroll-view
      :scroll-y="true"
      style="height: 100vh;">

      <nut-cell
        class="profile-profile-card"
        :title=state.username>
        <template #icon>
          <nut-avatar
            class="profile-avatar"
            size="large"
            :icon="state.avatarUrl"
            @active-avatar="state.showChangeAvatar=true;state.profileDetail.avatar=state.avatar"/>
        </template>
        <template #link>
          <nut-icon
            style="position: absolute;right:5vw;padding: 5vw 5vw;"
            name="edit"
            size="20"
            @click.stop="state.showChangeUsername=true;state.profileDetail.username=state.username;"/>
        </template>
      </nut-cell>

      <!-- 修改头像的弹出层 -->
      <nut-popup
        position="top"
        style="height:70vh;"
        round
        safe-area-inset-bottom
        v-model:visible="state.showChangeAvatar">
        <nut-cell-group
          title="更换头像"
          style="position:relative;top:2vh;width:90vw;left:5vw;box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1)">
          <nut-grid
            :column-num="5"
            :border="false"
            gutter="4">
            <nut-grid-item
              v-for="i in 30" :key="i">
              <nut-avatar
                size="large"
                :icon="`cloud://prod-8gf8jswafda304f9.7072-prod-8gf8jswafda304f9-1311194591/images/avatar${i}.png`"
                @active-avatar="state.avatar=i;state.profileDetail.avatar=i;changeProfile(state.profileDetail)"
              />
            </nut-grid-item>
          </nut-grid>
        </nut-cell-group>
      </nut-popup>

      <!-- 修改用户名的弹出层 -->
      <nut-popup
        position="top"
        style="height:40vh;"
        round
        safe-area-inset-bottom
        v-model:visible="state.showChangeUsername">
        <nut-cell-group style="position:relative;top:2vh;width:90vw;left:5vw;box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1)">
          <nut-cell>
            <nut-input
              v-model="state.profileDetail.username"
              style="height: auto;font-size: 20px;padding-left: 0;"
              maxLength="10"
              :border="false"
            />
          </nut-cell>
        </nut-cell-group>
        <nut-button
          type="info"
          plain
          style="height:8vh;width:40vw;left:6.6vw;position:fixed;top: 28vh;font-size: 20px"
          @click="state.showChangeUsername = false">
          取消
        </nut-button>
        <nut-button
          type="info"
          style="height:8vh;width:40vw;right:6.6vw;position:fixed;top: 28vh;font-size: 20px"
          @click="changeProfile(state.profileDetail)"
          :loading="state.profileChangeSubmitting">
          修改
        </nut-button>
      </nut-popup>


      <nut-cell-group
        title="账号管理"/>
      <nut-swipe v-for="data in account_list" :key="data.id">
        <AccountCard :accountData="data" :description="data.status"/>
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
      <SettingCard settingTitle="夜间模式 (绝赞施工中…)"/>
      <SettingCard settingTitle="定时任务 (绝赞施工中…)"/>
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

<script lang="ts">
import Taro from '@tarojs/taro';
import {ref, reactive, toRefs} from 'vue'
import AccountCard from "../../components/card/ProfileAccountCard.vue";
import SettingCard from "../../components/card/ProfileSettingCard.vue";
import {AccountData} from "../../types/AccountData";
import {request} from "../../util/request";
import {getAvatarUrl} from "../../util/ui";

export default {
  name: 'profile',
  components: {
    AccountCard,
    SettingCard
  },
  data() {
    return {
      account_list: []
    }
  },
  setup() {
    const state = reactive({
      "deleteInfo": {},
      "showDelete": false,
      "username": '',
      "avatar": 0,
      "avatarUrl": '',
      "showChangeUsername": false,
      "showChangeAvatar": false,
      "profileDetail": {
        "username": '',
        "avatar": 0
      },
      "profileChangeSubmitting": false
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

    function changeProfile(profile) {
      if (profile.username.length > 10) {
        openToast('fail', "用户名过长!")
        return
      }
      const data = {}
      if (profile.username != '')
        data['username'] = profile.username
      if (profile.avatar != 0)
        data['avatar'] = profile.avatar

      state.profileChangeSubmitting = true
      const r = request({
        path: "/user/profile/edit",
        method: "POST",
        data: data
      })
      r.then((res) => {
        if (res.statusCode == 200 && res.data.code == 0) {
          openToast('success', "修改成功!")
        } else {
          throw JSON.stringify(res)
        }
      }).catch((reason) => {
        console.error("Profile edit error: " + JSON.stringify(reason))
      }).finally(() => {
        fetchProfile()
        state.profileDetail = {
          username: profile.username,
          avatar: profile.avatar
        }
        state.profileChangeSubmitting = false
        state.showChangeUsername = false
        state.showChangeAvatar = false
      })

    }

    function fetchProfile() {
      const r = request({
        path: "/user/profile",
        method: "POST",
      })
      r.then((res) => {
        if (res.statusCode == 200 && res.data.code == 0) {
          state.username = res.data.data.username
          state.avatar = res.data.data.avatar
          state.avatarUrl = getAvatarUrl(state.avatar)
        } else {
          throw JSON.stringify(res)
        }
      }).catch((reason) => {
        console.error("Profile fetch error: " + JSON.stringify(reason))
      })
    }


    function addAccount() {
      Taro.navigateTo({
        url: '/pages/accountadd/index'
      })
    }

    function deleteAccount(accountData: AccountData) {
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
    const openToast = (type: string, msg: string, cover: boolean = false, title: string = "", bottom: string = "", center: boolean = true) => {
      toastInfo.show = true
      toastInfo.msg = msg
      toastInfo.type = type
      toastInfo.cover = cover
      toastInfo.title = title
      toastInfo.bottom = bottom
      toastInfo.center = center
    }

    fetchProfile()

    return {
      addAccount,
      deleteAccount,
      state,
      toastInfo,
      openToast,
      changeProfile
    }
  },
  beforeMount() {
    const r = request({
      path: "/account/list",
      method: "POST"
    })

    r.then((res) => {
      if (res.statusCode === 200 && res.data.code === 0) {
        //请无视这个ts的报错
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

.profile-profile-card {
  align-items: center;
  border-radius: 0;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
  font-size: 20px;
}

.profile-avatar {
  margin-right: 20px;
}

.nut-grid-item__content {
  padding: 0 0;
}

</style>
