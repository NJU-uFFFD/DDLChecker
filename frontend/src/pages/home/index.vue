<template>
  <view class="home">

    <!--分类与排序菜单-->
    <nut-menu>
      <nut-menu-item
        v-model="menu.value1"
        @change="listRefresh"
        :options="menu.options1"/>
      <nut-menu-item
        v-model="menu.value2"
        @change="listRefresh"
        :options="menu.options2"/>
    </nut-menu>

    <!--DDL列表-->
    <scroll-view
      :refresher-triggered="state.refreshing"
      :scroll-y="true"
      style="height: 91vh;"
      @scrolltolower="listLower"
      @scroll="scroll"
      @refresherrefresh="listRefresh"
      refresherEnabled="true">
      <view
        v-for="data in ddl_list"
        :key="data">
        <nut-swipe>
          <HomeDdlCard
            :ddlData="data"
            @onClick="onDdlClick"
            @onCompleteStatusChange="completeDdl"/>
          <template #right>
            <nut-button style="height:100%;border-radius: 10px" type="danger" @click="deleteDdl(data)">删除</nut-button>
          </template>
        </nut-swipe>

      </view>
    </scroll-view>

    <!-- DDL详情 -->
    <nut-dialog
      :title=state.ddlDetailData.title
      close-on-click-overlay
      lock-scroll
      v-model:visible="state.showDetails">
      <nut-countdown
        #default
        style="display: flex;justify-content: center"
        :end-time="state.ddlDetailData.ddl_time"
        format="还剩 DD 天 HH 时 mm 分 ss 秒"
      />
      <nut-cell
        style="box-shadow: 0 0 0 0"
        :title="state.ddlDetailData.content"/>
      <!-- 查改 -->
      <!--      <nut-form>-->
      <!--        <nut-form-item label="截止时间">-->
      <!--          <input-->
      <!--            :value="state.pickerDate.toLocaleString()"-->
      <!--            :placeholder="state.pickerDate.toLocaleString()"-->
      <!--            readonly-->
      <!--            disabled-->
      <!--            @click="state.datePickerShow = true"/>-->
      <!--        </nut-form-item>-->
      <!--        <nut-form-item label="详细说明">-->
      <!--          <input-->
      <!--            v-model="state.ddlDetailData.content"-->
      <!--            class="nut-input-text"-->
      <!--            :placeholder="state.ddlDetailData.content"-->
      <!--            type="text"/>-->
      <!--        </nut-form-item>-->
      <!--      </nut-form>-->

    </nut-dialog>

    <!-- 手动添加 ddl 的弹出层 -->
    <nut-dialog
      title="添加待办"
      v-model:visible="state.showAdd"
      close-on-click-overlay
      lock-scroll
      ok-text="添加"
      @ok="submitDdl">
      <nut-form>
        <!--TODO: 表单内容检验-->
        <nut-form-item label="待办标题">
          <input
            v-model="state.addInfo.title"
            class="nut-input-text"
            placeholder="请输入待办标题"
            type="text"/>
        </nut-form-item>
        <nut-form-item label="截止时间">
          <input
            :value="state.pickerDate.toLocaleString()"
            placeholder="选择时间"
            readonly
            disabled
            @click="state.datePickerShow = true"/>
        </nut-form-item>
        <nut-form-item label="详细说明">
          <input
            v-model="state.addInfo.detail"
            class="nut-input-text"
            placeholder="请输入详细说明"
            type="text"/>
        </nut-form-item>
      </nut-form>
      <template #footer>
        <nut-button
          plain type="info"
          @click="state.showAdd = false">取消
        </nut-button>
        <nut-button
          type="info"
          @click="submitDdl"
          :loading="state.ddlSubmitting">添加
        </nut-button>
      </template>
    </nut-dialog>

    <!-- 选择DDL时间 -->
    <nut-datepicker catchMove
                    v-model="state.pickerDate"
                    type="datetime"
                    title="Deadline 选择"
                    v-model:visible="state.datePickerShow"
                    @confirm="datePickerConfirm"
                    :min-date="getMinDate()"
                    :is-show-chinese="true"
                    :lock-scroll="true"
    />
    <!-- Toast -->
    <nut-toast
      :msg="toastInfo.msg"
      v-model:visible="toastInfo.show"
      :type="toastInfo.type"
      @closed="toastInfo.onClosed"
      :cover="toastInfo.cover"/>

    <!-- 手动添加 ddl 的按钮 -->
    <nut-button type="primary" class="add_button" icon="uploader" @click="addDdl"/>
  </view>
</template>

<script lang="ts">
import {reactive, toRefs} from 'vue';
import HomeDdlCard from "../../components/card/HomeDdlCard.vue";
import {DDLData} from "../../types/DDLData";
import {request} from "../../util/request"
import Taro from "@tarojs/taro";

export default {
  name: 'home',
  components: {
    HomeDdlCard,
  },
  setup() {
    let ddls = reactive<{ ddl_list: DDLData [] }>({ddl_list: []});

    let state = reactive({
      "showAdd": false,
      "datePickerShow": false,
      "ddlSubmitting": false,
      "refreshing": false,
      "offset": 0,
      "more": true,
      "addInfo": {
        "title": "",
        // "date": new Date(),
        "detail": ""
      },
      "showDetails": false,
      "ddlDetailData": {},
      "pickerDate": new Date(),
      "showEditDate": false,
      "showEditContent": false
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

    const menu = reactive({
      options1: [
        {text: '全部DDL', value: 0},
        {text: '紧急DDL', value: 1},
        {text: '宽松DDL', value: 2},
        {text: '超时DDL', value: 3},
      ],
      options2: [
        {text: '由近至远', value: false},
        {text: '由远至近', value: true},
      ],
      value1: 0,
      value2: false
    });

    const openToast = (type: string, msg: string, cover: boolean = false, title: string = "", bottom: string = "", center: boolean = true) => {
      toastInfo.show = true
      toastInfo.msg = msg
      toastInfo.type = type
      toastInfo.cover = cover
      toastInfo.title = title
      toastInfo.bottom = bottom
      toastInfo.center = center
    }

    // 添加 DDL 相关
    function submitDdl() {
      state.ddlSubmitting = true
      const r = request({
        "method": "POST",
        "path": "/ddl/add",
        "data": {
          "title": state.addInfo.title,
          "ddl_time": state.pickerDate.getTime(),
          "content": state.addInfo.detail
        }
      })

      r.then((res) => {
        if (res.statusCode == 200 && res.data.code == 0) {
          state.showAdd = false
          openToast('success', "添加成功!")
          listRefresh()
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

    function addDdl() {
      state.addInfo = {
        "title": "",
        "detail": ""
      }
      state.pickerDate = new Date()
      state.ddlSubmitting = false
      state.showAdd = true
    }

    function datePickerConfirm({selectedValue}) {
      state.pickerDate = new Date(selectedValue[0], selectedValue[1] - 1, selectedValue[2], selectedValue[3], selectedValue[4])
    }

    // 获取 DDL 相关
    function fetchDdls(start: number, end: number, callback: Function) {
      state.refreshing = true
      const r = request({
        path: "/ddl/list",
        method: "POST",
        data: {
          "start": start,
          "end": end,
          "filter": {
            "is_completed": false,
            "is_overtime": menu.value1 == 3
          },
          "sorter": {
            "reversed": menu.value2
          }
        }
      })

      r.then((res) => {
        callback(res.data.data.ddl_list)
      }).catch((reason) => {
        console.error("DDL fetch error: " + JSON.stringify(reason))
      }).finally(() => {
        state.refreshing = false
      })
    }

    // 刷新列表
    function listRefresh() {
      console.log("ddl refresh.")
      state.refreshing = true
      state.offset = 10
      state.more = true
      fetchDdls(0, 10, (list: DDLData[]) => {
        state.refreshing = false
        ddls.ddl_list = list
        console.log(list)
      })
    }

    function listLower() {
      if (!state.more || state.refreshing) {
        return
      }
      // 滑动到底部, 获取新的 ddl
      fetchDdls(state.offset, state.offset + 10, (list) => {
        if (list.length == 0) {
          console.log("无更多项目.")
          state.more = false
        }
        ddls.ddl_list.push.apply(ddls.ddl_list, list)
      })
      state.offset += 10
    }

    // 获取 DDL 时间下限
    const getMinDate = (() => {
      let now = new Date()
      return new Date(now.setDate(now.getDate() - 30))
    })

    // 查看DDL详情
    const onDdlClick = (ddlData) => {
      state.ddlDetailData = ddlData
      state.showDetails = true
      state.pickerDate = new Date(ddlData.ddl_time)
    };

    // 删除 DDL
    function deleteDdl(ddlData) {
      console.log("删除 DDL ID: " + ddlData.id)
      const r = request({
        method: "POST",
        path: "/ddl/delete",
        data: {
          "id": ddlData.id
        }
      })

      r.then((res) => {
        if (res.statusCode == 200 && res.data.code == 0) {
          openToast('success', "删除成功!")
        } else {
          throw JSON.stringify(res)
        }
      }).catch((reason) => {
        Taro.showModal({
          title: '错误',
          content: '删除代办出错: ' + JSON.stringify(reason),
          showCancel: false
        })
      }).finally(() => {
        listRefresh()
      })
    }

    // 完成/撤销完成 DDL
    function completeDdl(ddlData) {
      console.log((ddlData.is_completed == true ? "完成 DDL ID: " : "撤销 DDL ID: ") + ddlData.id + " 并更新")
      const r = request({
        method: "POST",
        path: "/ddl/update",
        data: {
          "id": ddlData.id,
          "is_completed": ddlData.is_completed
        }
      })

      r.then((res) => {
        if (res.statusCode == 200 && res.data.code == 0) {
          openToast('success', ddlData.is_completed == true ? "完成待办成功!" : "撤销成功!")
        } else {
          throw JSON.stringify(res)
        }
      }).catch((reason) => {
        Taro.showModal({
          title: '错误',
          content: (ddlData.is_completed == true ? '完成待办出错: ' : '撤销出错: ') + JSON.stringify(reason),
          showCancel: false
        })
      })
    }

    // 第一次加载列表
    listRefresh()

    return {
      ...toRefs(ddls),
      menu,
      addDdl,
      datePickerConfirm,
      getMinDate,
      submitDdl,
      listRefresh,
      listLower,
      state,
      toastInfo,
      onDdlClick,
      deleteDdl,
      completeDdl
    }
  }
}
</script>

<style>
.home {
  background: #f9f9f9;
}

.add_button {
  position: fixed;
  right: 30px;
  bottom: 30px;
}

/*表单内行高设置*/
.nut-cell {
  line-height: normal;
}
</style>
