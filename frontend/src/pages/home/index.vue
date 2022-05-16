<template>
  <view class="home">
    <HomeDdlListMenu
      @sortMode="sortDdlList"/>

    <view>
      <scroll-view :refresher-triggered="state.refreshing" :scroll-y="true" style="height: 91vh;" @scrolltolower="listLower"
                   @scroll="scroll" @refresherrefresh="listRefresh" refresherEnabled="true">
        <view
          v-for="data in ddlList"
          :key="data">
          <HomeDdlCard :ddlData="data"/>
        </view>
      </scroll-view>
    </view>



    <!-- 手动添加 ddl 的弹出层 -->
    <view>
      <nut-overlay v-model:visible="state.showAdd" :close-on-click-overlay=false :z-index="200">
        <nut-form>

<!--          TODO: 表单内容检验-->

          <nut-form-item label="代办事项标题">
            <input v-model="state.addInfo.title" class="nut-input-text" placeholder="请输入代办事项标题" type="text"/>
          </nut-form-item>

          <nut-form-item label="Deadline">
            <input :value="state.addInfo.date.toLocaleString()" placeholder="选择时间" readonly="true" disabled="true"
                   @click="state.datePickerShow = true">

            <nut-datepicker catchMove
                            v-model="state.addInfo.date"
                            class="datepicker"
                            type="datetime"
                            title="Deadline 选择"
                            v-model:visible="state.datePickerShow"
                            @confirm="datePickerConfirm"
                            :min-date="getMinDate()"
                            :is-show-chinese="true"
                            :lock-scroll="true"
            ></nut-datepicker>
          </nut-form-item>

          <nut-form-item label="详细说明">
            <input v-model="state.addInfo.detail" class="nut-input-text" placeholder="请输入详细说明" type="text"/>
          </nut-form-item>

        </nut-form>

        <nut-button size="large" type="danger" @click="state.showAdd = false">关闭</nut-button>
        <nut-button size="large" type="success" @click="submitDdl()" :loading="state.ddlSubmitting">添加</nut-button>

      </nut-overlay>
    </view>

    <!-- Toast -->
    <nut-toast :msg="toastInfo.msg" v-model:visible="toastInfo.show" :type="toastInfo.type"
               @closed="toastInfo.onClosed" :cover="toastInfo.cover"/>

    <!-- 手动添加 ddl 的按钮 -->
    <nut-button type="primary" id="add_button" @click="addDdl">+</nut-button>
  </view>
</template>

<script lang="ts">
import {reactive, toRefs} from 'vue';
import HomeDdlCard from "../../components/card/HomeDdlCard.vue";
import HomeDdlListMenu from "../../components/menu/HomeDdlListMenu.vue";
import {DDLData} from "../../types/DDLData";
import {request} from "../../util/request"
import Taro from "@tarojs/taro";

export default {
  name: 'home',
  components: {
    HomeDdlCard,
    HomeDdlListMenu
  },
  setup() {
    let ddls = reactive({"ddlList": []});

    let state = reactive({
      "showAdd": false,
      "datePickerShow": false,
      "ddlSubmitting": false,
      "refreshing": false,
      "addInfo": {
        "title": "",
        "date": new Date(),
        "detail": ""
      }
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

    // function sortDdlList(mode: string) {
    //   ddls.ddlList = ddls.ddlList.sort((o1, o2) => {
    //     switch (mode) {
    //       case "a":
    //         return o1.ddl_time.valueOf() - o2.ddl_time.valueOf()
    //       case "b":
    //         return o2.ddl_time.valueOf() - o1.ddl_time.valueOf()
    //       case "c":
    //         return o1.id - o2.id
    //       default:
    //         return o2.id - o1.id
    //     }
    //   })
    // }

    function addDdl() {
      state.addInfo = {
        "title": "",
        "date": new Date(),
        "detail": ""
      }
      state.ddlSubmitting = false
      state.showAdd = true
    }

    function datePickerConfirm({selectedValue}) {
      const date = selectedValue.slice(0, 3).join('-');
      const time = selectedValue.slice(3).join(':');
      state.addInfo.date = new Date(date + ' ' + time);
    }

    const openToast = (type: string, msg: string, cover: boolean = false, title: string = "", bottom: string = "", center: boolean = true) => {
      toastInfo.show = true
      toastInfo.msg = msg
      toastInfo.type = type
      toastInfo.cover = cover
      toastInfo.title = title
      toastInfo.bottom = bottom
      toastInfo.center = center
    }

    function submitDdl() {
      state.ddlSubmitting = true
      const r = request({
        "method": "POST",
        "path": "/ddl/add",
        "data": {
          "title": state.addInfo.title,
          "ddl_time": state.addInfo.date.getTime(),
          "content": state.addInfo.detail
        }
      })

      r.then((res) => {
        if (res.statusCode == 200 && res.data.code == 0) {
          state.showAdd = false
          openToast('success', "添加成功!")
        } else {
          throw JSON.stringify(res)
        }
      }).catch((reason) => {
        Taro.showModal({
          title: '错误',
          content: '添加代办出错: ' + JSON.stringify(reason),
          showCancel: false
        })
        state.ddlSubmitting = false
      })
    }

    function fetchDdls(start, end, callback) {
      const r = request({
        path: "/ddl/list",
        method: "POST",
        data: {
          "start": start,
          "end": end
        }
      })

      r.then((res) => {
        callback(res.data.data.ddl_list)
      }).catch((reason) => {
        console.error("DDL fetch error: " + JSON.stringify(reason))
      })
    }

    function listRefresh() {
      state.refreshing = true
      fetchDdls(0, 10 - 1, (list) => {
        state.refreshing = false
        ddls.ddlList = list
        console.log(list)
      })
    }

    // todo: 获取更多
    fetchDdls(0, 9,(list) => {
      ddls.ddlList = list
    })

    function listLower() {
      // 滑动到底部, 获取新的 ddl
      console.log("下")
    }

    // fetchDdls()

    const getMinDate = (() => {
      let now = new Date()
      return new Date(now.setDate(now.getDate() - 30))
    })



    return {
      ...toRefs(ddls),
      // sortDdlList,
      addDdl,
      datePickerConfirm,
      getMinDate,
      submitDdl,
      listRefresh,
      listLower,
      state,
      toastInfo
    }
  }
}
</script>

<style>
.home {
  background: #f9f9f9;
}

#add_button {
  position: fixed;
  right: 30px;
  bottom: 30px;
}

/* bug fix for datepicker */
.nut-picker-item {
  display: none;
}
</style>
