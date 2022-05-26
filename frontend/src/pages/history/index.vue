<template>
  <view class="page">
    <scroll-view
      :scroll-y="true"
      style="height: 100vh;">
      <nut-cell-group
        title="Dashboard"/>
      <nut-grid
        :column-num="2"
        :gutter="10">
        <nut-grid-item>
          <nut-circleprogress
            :progress="state.completedRate"
            :radius="75"
            :strokeWidth="10"
            :clockwise="false"
            :color="{'0':'#2cffff','100%':'#2c68ff'}">
            <div>总完成率</div>
            <div>{{ state.completedRate }}%</div>
          </nut-circleprogress>
        </nut-grid-item>
        <nut-grid-item>
          <nut-circleprogress
            :progress="100"
            :radius="75"
            :strokeWidth="10"
            :color="{'0':'#96f85e','100%':'#72c03c'}">
            <div>已完成</div>
            <div>{{ state.completedNumber }}件</div>
          </nut-circleprogress>
        </nut-grid-item>
        <nut-grid-item>
          <nut-circleprogress
            :progress="100"
            :radius="75"
            :strokeWidth="10"
            :color="{'0':'#ffe277','100%':'#ffb40b'}">
            <div>剩余紧急</div>
            <div>{{ state.urgeNumber }}件</div>
          </nut-circleprogress>
        </nut-grid-item>
        <nut-grid-item>
          <nut-circleprogress
            :progress="100"
            :radius="75"
            :strokeWidth="10"
            :color="{'0':'#b82806','100%':'#ff0000'}">
            <div>已超时</div>
            <div>{{ state.overtimeNumber }}件</div>
          </nut-circleprogress>
        </nut-grid-item>
      </nut-grid>

      <nut-cell-group
        title="日历视图"/>
      <!-- 下面这个双向绑定有bug,没法回收,最新测试版已经修了,就看什么时候发布正式版 -->
      <nut-collapse
        v-model:active="state.activeName"
        icon="down-arrow">
        <nut-collapse-item
          title="选择日期以查看当日 DDL"
          :name="1">
          <!-- 下面这个滚动有警告bug,还在拖着没修 -->
          <nut-calendar
            style="display: flex;left:2vw;width: 96%;height:60vh;overflow: hidden;border-radius: 10px"
            :poppable="false"
            :start-date="getDateFormatString(state.startDate)"
            :end-date="getDateFormatString(state.endDate)"
            :is-auto-back-fill="true"
            :show-title="false"
            :show-sub-title="false"
            @choose="chooseDate"
          />
        </nut-collapse-item>
      </nut-collapse>
      <nut-cell-group
        :title="getDateZhCNString()+'的日程'"/>
      <nut-cell/>
      <!-- 展示当日新添加的／完成的／超时的／删除的 -->
    </scroll-view>
  </view>
</template>

<script lang="ts">
import {reactive, ref} from 'vue'
import Taro from "@tarojs/taro"

export default {
  name: "history",
  setup() {
    const state = reactive({
      "completedRate": 50,
      "completedNumber": 60,
      "urgeNumber": 5,
      "overtimeNumber": 12,
      "activeName": [],
      "calendarDate": new Date(),
      "startDate": new Date(),
      "endDate": new Date()
    })

    //应由后端传入
    const now = new Date()
    state.startDate = new Date(now.setDate(now.getDate() - 30))
    state.endDate = new Date(now.setDate(now.getDate() + 120))

    const getDateFormatString = (date: Date) => {
      return String(date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate())
    }

    const chooseDate = (param) => {
      state.calendarDate = new Date(param[0], param[1] - 1, param[2])
      state.activeName = []
    }

    const weekdayZhCN = {"0": "日", "1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六"}

    const getDateZhCNString = () => {
      const d = state.calendarDate
      return String(`${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日 星期${weekdayZhCN[d.getDay()]}`);
    }

    return {
      state,
      getDateFormatString,
      chooseDate,
      getDateZhCNString
    }
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

.nut-grid-item__content--surround {
  border-radius: 20px;
}

.nut-circleprogress-text {
  font-size: 22px;
}

</style>
