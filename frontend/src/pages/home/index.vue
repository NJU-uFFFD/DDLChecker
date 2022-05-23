<template>
  <view class="home">

    <!--筛选与排序菜单-->
    <nut-menu>
      <nut-menu-item
        title="筛选">
        <div style="display: flex; flex: 1; justify-content: space-between; align-items: center">
          <nut-checkboxgroup
            v-model="menu.filterCheckboxGroup"
            ref="filterGroup"
            @change="listRefresh"
            style="display: flex;flex-flow: wrap">
            <nut-checkbox
              v-for="item in menu.filterCheckboxSource"
              :key="item.label"
              :label="item.label"
              icon-size="24"
              style="display: flex; height: 6vh; width:25vw">{{ item.value }}
            </nut-checkbox>
          </nut-checkboxgroup>
          <div
            style="width: 60vw">
            <nut-button
              type="primary"
              @click="filterToggleAll(true)"
              style="width:30vw; height: 5vh;margin-top: 2vh">
              全选
            </nut-button>
            <nut-button
              plain type="primary"
              @click="filterToggleAll(false)"
              style="width:30vw; height: 5vh;">
              全不选
            </nut-button>
            <nut-button
              plain type="default"
              @click="filterReverse"
              style="width:30vw; height: 5vh;">
              反选
            </nut-button>
          </div>

        </div>
      </nut-menu-item>
      <nut-menu-item
        v-model="menu.value"
        @change="listRefresh"
        :options="menu.options"/>
    </nut-menu>

    <!-- DDL列表 -->
    <scroll-view
      :refresher-triggered="state.refreshing"
      :scroll-y="true"
      style="height: 91vh;"
      @scrolltolower="listLower"
      @scroll="scroll"
      @refresherrefresh="listRefresh"
      refresherEnabled="true">

      <nut-swipe
        v-for="data in ddl_list"
        :key="data">
        <HomeDdlCard
          :ddlData="data"
          @onClick="state.ddlDetailData = data; state.showDetails = true"
          @onCompleteStatusChange="completeDdl"/>
        <template #right>
          <nut-button
            style="height:100%; border-radius: 10px"
            type="danger"
            @click="state.showDelete=true;state.deleteInfo=data">
            删除
          </nut-button>
        </template>
      </nut-swipe>

    </scroll-view>

    <!-- DDL 详情 -->
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
      <template #footer>
        <nut-button
          type="info"
          @click="state.showEdit = true">修改
        </nut-button>
      </template>
    </nut-dialog>

    <!-- 修改 DDL 的弹出层 -->
    <nut-popup
      position="bottom"
      style="height:80vh;"
      round
      safe-area-inset-bottom
      v-model:visible="state.showEdit">
      <nut-cell-group
        style="position:relative;top:2vh;width:90vw;left:5vw;box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1)">
        <!--TODO: 表单内容检验-->
        <nut-cell>
          <nut-input
            v-model="state.ddlDetailData.title"
            style="height: auto;font-size: 20px;padding-left: 0;"
            maxLength="32"
            :border="false"
          />
        </nut-cell>
        <nut-cell>
          <nut-input
            style="height: auto;font-size: 20px;padding-left: 0;"
            :border="false"
            disabled
            :placeholder="state.pickerDate.toLocaleString()"
            @click.stop="state.datePickerShow = true"
          />
        </nut-cell>
        <nut-cell>
          <nut-input
            v-model="state.ddlDetailData.content"
            style="height: auto;font-size: 20px;max-height: 40vh;padding-left: 0;padding-bottom: 0"
            type="textarea"
            show-word-limit
            rows=11
            maxLength="128"
            :border="false"
          />
        </nut-cell>
      </nut-cell-group>
      <nut-button
        type="info"
        plain
        style="height:8vh;width:40vw;left:6.6vw;position:fixed;bottom: 5vh;font-size: 20px"
        @click="state.showEdit = false">
        取消
      </nut-button>
      <nut-button
        type="info"
        style="height:8vh;width:40vw;right:6.6vw;position:fixed;bottom: 5vh;font-size: 20px"
        @click="editDdl(state.ddlDetailData)"
        :loading="state.ddlEditSubmitting">
        修改
      </nut-button>
    </nut-popup>

    <!-- 手动添加 DDL 的弹出层 -->
    <nut-popup
      position="bottom"
      style="height:80vh;"
      round
      safe-area-inset-bottom
      v-model:visible="state.showAdd">
      <nut-cell-group
        style="position:relative;top:2vh;width:90vw;left:5vw;box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1)">
        <!--TODO: 表单内容检验-->
        <nut-cell>
          <nut-input
            v-model="state.addInfo.title"
            style="height: auto;font-size: 20px;padding-left: 0;"
            maxLength="32"
            :border="false"
            placeholder="新建待办"
          />
        </nut-cell>
        <nut-cell>
          <nut-input
            style="height: auto;font-size: 20px;padding-left: 0;"
            :border="false"
            disabled
            :placeholder="state.pickerDate.toLocaleString()"
            @click.stop="state.datePickerShow = true"
          />
        </nut-cell>
        <nut-cell>
          <nut-input
            v-model="state.addInfo.content"
            style="height: auto;font-size: 20px;max-height: 40vh;padding-left: 0;padding-bottom: 0"
            type="textarea"
            show-word-limit
            :rows="Math.floor(state.addInfo.content.length/20)+2<11?Math.floor(state.addInfo.content.length/20)+2:11"
            maxLength="128"
            :border="false"
            placeholder="请输入待办详情"
          />
        </nut-cell>
      </nut-cell-group>
      <nut-button
        type="info"
        plain
        style="height:8vh;width:40vw;left:6.6vw;position:fixed;bottom: 5vh;font-size: 20px"
        @click="state.showAdd = false">
        取消
      </nut-button>
      <nut-button
        type="info"
        style="height:8vh;width:40vw;right:6.6vw;position:fixed;bottom: 5vh;font-size: 20px"
        @click="submitDdl"
        :loading="state.ddlAddSubmitting">
        添加
      </nut-button>
    </nut-popup>

    <!-- 选择 DDL 时间 -->
    <nut-datepicker
      v-model="state.pickerDate"
      type="datetime"
      title="Deadline 选择"
      v-model:visible="state.datePickerShow"
      @confirm="({selectedValue : t}) =>state.pickerDate = new Date(t[0], t[1] - 1, t[2], t[3], t[4])"
      :min-date="getMinDate()"
    />

    <!--  删除 DDL 相关  -->
    <nut-dialog
      title="删除 DDL"
      content="真的不需要这个 DDL 了吗？"
      close-on-click-overlay
      lock-scroll
      v-model:visible="state.showDelete">
      <template #footer>
        <nut-button
          plain type="danger"
          @click="state.showDelete = false">取消
        </nut-button>
        <nut-button
          type="danger"
          @click="deleteDdl(state.deleteInfo)">删除
        </nut-button>
      </template>
    </nut-dialog>

    <!-- Toast -->
    <nut-toast
      :msg="toastInfo.msg"
      v-model:visible="toastInfo.show"
      :type="toastInfo.type"
      @closed="toastInfo.onClosed"
      :cover="toastInfo.cover"/>

    <!-- 手动添加 ddl 的按钮 -->
    <nut-button
      type="primary"
      class="add_button"
      style="position: fixed;height: 8vh;width: 10vh;right: 30px;bottom: 30px;box-shadow: 0 4px 15px 0 rgba(237, 238, 241, 10)"
      icon="uploader"
      @click="state.showAdd = true"/>

  </view>
</template>

<script lang="ts">
import {reactive, ref, toRefs} from 'vue';
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
      "showDelete": false,
      "showEdit": false,
      "datePickerShow": false,
      "ddlAddSubmitting": false,
      "refreshing": false,
      "offset": 0,
      "more": true,
      "addInfo": {
        "title": "",
        // "date": new Date(),
        "content": ""
      },
      deleteInfo: {},
      "showDetails": false,
      "ddlDetailData": {},
      "pickerDate": new Date(),
      "ddlEditSubmitting": false,
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
      options: [
        {text: '由近至远', value: false},
        {text: '由远至近', value: true},
      ],
      value: false,
      filterCheckboxGroup: ['1', '3', '4', '5', '6'],
      filterCheckboxSource: [
        {label: '1', value: '未完成'},
        {label: '2', value: '已完成'},
        {label: '3', value: '未超时'},
        {label: '4', value: '已超时'},
        {label: '5', value: '宽松'},
        {label: '6', value: '紧急'},
      ]
    })

    const filterGroup = ref(null)

    const filterToggleAll = (f: boolean) => {
      (filterGroup.value as any).toggleAll(f)
    }

    const filterReverse = () => {
      menu.filterCheckboxGroup = ['1', '2', '3', '4', '5', '6'].filter((x) => {
        return menu.filterCheckboxGroup.indexOf(x) == -1
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

    // 添加 DDL 相关
    function submitDdl() {
      state.ddlAddSubmitting = true
      const r = request({
        "method": "POST",
        "path": "/ddl/add",
        "data": {
          "title": state.addInfo.title || "新建待办",
          "ddl_time": state.pickerDate.getTime(),
          "content": state.addInfo.content || "无详情"
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
      }).finally(() => {
        state.addInfo = {
          "title": "",
          "content": ""
        }
        state.pickerDate = new Date()
        state.showAdd = false
        state.ddlAddSubmitting = false
      })
    }

    //修改 DDL 相关
    function editDdl(ddlData) {
      state.ddlEditSubmitting = true
      const r = request({
        method: "POST",
        path: "/ddl/update",
        data: {
          "id": ddlData.id,
          "title": ddlData.title,
          "ddl_time": state.pickerDate.getTime(),
          "content": ddlData.content
        }
      })

      r.then((res) => {
        if (res.statusCode == 200 && res.data.code == 0) {
          openToast('success', "修改成功!")
        } else {
          throw JSON.stringify(res)
        }
      }).catch((reason) => {
        Taro.showModal({
          title: '错误',
          content: '修改代办出错: ' + JSON.stringify(reason),
          showCancel: false
        })
      }).finally(() => {
        listRefresh()
        state.pickerDate = new Date()
        state.showEdit = false
        state.ddlEditSubmitting = false
      })
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
            "is_not_completed": menu.filterCheckboxGroup.indexOf('1') != -1,
            "is_completed": menu.filterCheckboxGroup.indexOf('2') != -1,
            "is_not_overtime": menu.filterCheckboxGroup.indexOf('3') != -1,
            "is_overtime": menu.filterCheckboxGroup.indexOf('4') != -1
          },
          "sorter": {
            "reversed": menu.value
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

    // 删除 DDL
    function deleteDdl(ddlData) {
      console.log("删除 DDL ID: " + ddlData.id)
      ddlData.is_deleted = true
      const r = request({
        method: "POST",
        path: "/ddl/update",
        data: {
          "id": ddlData.id,
          "is_deleted": ddlData.is_deleted
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
      filterToggleAll,
      filterGroup,
      filterReverse,
      getMinDate,
      submitDdl,
      listRefresh,
      listLower,
      state,
      toastInfo,
      deleteDdl,
      completeDdl,
      editDdl
    }
  }
}
</script>

<style>
.home {
  background: #f9f9f9;
}

/*表单内行高设置*/
.nut-cell {
  line-height: normal;
}

.nut-picker-roller-item {
  user-select: none;
}

.nut-picker-item {
  visibility: hidden;
}
</style>
