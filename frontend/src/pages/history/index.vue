<template>
  <view class="page">
    <scroll-view
      :scroll-y="true"
      style="height: 96vh;">
      <nut-cell-group
        title="Dashboard"/>
      <nut-grid
        :column-num="2"
        :gutter="10">
        <nut-grid-item>
          <nut-circleprogress
            :progress="completedRate"
            :radius="70"
            :strokeWidth="10"
            :clockwise="false"
            :color="{'0':'#2cffff','100%':'#2c68ff'}">
            <div>总完成率</div>
            <div>{{ completedRate }}%</div>
          </nut-circleprogress>
        </nut-grid-item>
        <nut-grid-item>
          <nut-circleprogress
            :progress="100"
            :radius="70"
            :strokeWidth="10"
            :color="{'0':'#96f85e','100%':'#72c03c'}">
            <div>已完成</div>
            <div>{{ completedNumber }}件</div>
          </nut-circleprogress>
        </nut-grid-item>
        <nut-grid-item>
          <nut-circleprogress
            :progress="100"
            :radius="70"
            :strokeWidth="10"
            :color="{'0':'#ffe277','100%':'#ffb40b'}">
            <div>剩余紧急</div>
            <div>{{ urgentNumber }}件</div>
          </nut-circleprogress>
        </nut-grid-item>
        <nut-grid-item>
          <nut-circleprogress
            :progress="100"
            :radius="70"
            :strokeWidth="10"
            :color="{'0':'#b82806','100%':'#ff0000'}">
            <div>已超时</div>
            <div>{{ overtimeNumber }}件</div>
          </nut-circleprogress>
        </nut-grid-item>
      </nut-grid>

      <nut-cell-group
        title="选择日期以查看当日 DDL"/>
      <!-- 下面这个双向绑定有bug,没法回收,最新测试版已经修了,就看什么时候发布正式版 -->
      <nut-collapse
        v-model:active="state.activeName"
        icon="down-arrow">
        <nut-collapse-item
          :title="getDateZhCNString()+' 的日程'"
          :name="1">
          <nut-calendar
            style="display: flex;left:2vw;width: 96%;height:50vh;overflow: hidden;border-radius: 10px"
            :poppable="false"
            :start-date="startDateStr"
            :end-date="endDateStr"
            :is-auto-back-fill="true"
            :show-title="false"
            :show-sub-title="false"
            @choose="chooseDate"
          />
        </nut-collapse-item>
      </nut-collapse>

      <nut-cell-group
        v-if="ddls.ddl_list!==undefined&&ddls.ddl_list.length!==0"
        :title="getDateZhCNString()+' 到期的DDL'"/>
      <HistoryDdlCard
        v-if="ddls.ddl_list!==undefined&&ddls.ddl_list.length!==0"
        v-for="data in ddls.ddl_list" :key="data"
        :ddlData="data"
        @onClick="state.ddlDetailData = data; state.showDetails = true"
      />

      <nut-cell-group
        v-if="ddls.complete_list!==undefined&&ddls.complete_list.length!==0"
        :title="getDateZhCNString()+' 完成的DDL'"/>
      <HistoryDdlCard
        v-if="ddls.complete_list!==undefined&&ddls.complete_list.length!==0"
        v-for="data in ddls.complete_list" :key="data"
        :ddlData="data"
        @onClick="state.ddlDetailData = data; state.showDetails = true"
      />

      <nut-cell-group
        v-if="ddls.create_list!==undefined&&ddls.create_list.length!==0"
        :title="getDateZhCNString()+' 创建的DDL'"/>
      <HistoryDdlCard
        v-if="ddls.create_list!==undefined&&ddls.create_list.length!==0"
        v-for="data in ddls.create_list" :key="data"
        :ddlData="data"
        @onClick="state.ddlDetailData = data; state.showDetails = true"
      />

      <nut-divider>没有更多 DDL 了捏</nut-divider>

    </scroll-view>

    <nut-dialog
      :title=state.ddlDetailData.title
      close-on-click-overlay
      lock-scroll
      v-model:visible="state.showDetails"
      no-footer>
      <nut-countdown
        #default
        style="display: flex;justify-content: center"
        :end-time="state.ddlDetailData.ddl_time"
        format="还剩 DD 天 HH 时 mm 分 ss 秒"
      />
      <nut-cell
        style="box-shadow: 0 0 0 0"
        :title="state.ddlDetailData.content"/>
    </nut-dialog>
  </view>
</template>

<script lang="ts">
import {reactive, ref} from 'vue'
import Taro, {getCurrentInstance} from "@tarojs/taro"
import {request} from "../../util/request";
import {DDLData} from "../../types/DDLData";
import HistoryDdlCard from "../../components/card/HistoryDdlCard.vue";

export default {
  name: "history",
  components: {
    HistoryDdlCard
  },
  data() {
    return {
      completedRate: 0,
      completedNumber: 0,
      urgentNumber: 0,
      overtimeNumber: 0,
      startDateStr: "2012-1-1",
      endDateStr: "2032-12-31"
    }
  },
  setup() {

    console.log(getCurrentInstance())
    const state = reactive({
      "activeName": [],
      "calendarDate": new Date(),
      "showDetails": false,
      "ddlDetailData": {},
    })


    let ddls = reactive<{ ddl_list: DDLData [], create_list: DDLData[], complete_list: DDLData[] }>({
      ddl_list: [],
      create_list: [],
      complete_list: []
    });

    state.calendarDate.setHours(0)
    state.calendarDate.setMinutes(0)
    state.calendarDate.setSeconds(0)
    state.calendarDate.setMilliseconds(0)
    fetchDdls(state.calendarDate, "ddl")
    fetchDdls(state.calendarDate, "create")
    fetchDdls(state.calendarDate, "complete")

    const chooseDate = (param) => {
      state.calendarDate = new Date(param[0], param[1] - 1, param[2])
      state.activeName = []
      fetchDdls(state.calendarDate, "ddl")
      fetchDdls(state.calendarDate, "create")
      fetchDdls(state.calendarDate, "complete")
    }

    const weekdayZhCN = {"0": "日", "1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六"}

    const getDateZhCNString = () => {
      const d = state.calendarDate
      return String(`${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日 星期${weekdayZhCN[d.getDay()]}`);
    }

    // 获取 DDL 相关
    function fetchDdls(chooseDate: Date, mode: string) {
      let data = {
        "page": 1,
        "size": 50,
      }
      switch (mode) {
        case "ddl":
          data['ddl_time_range'] = {
            start: chooseDate.valueOf(),
            end: chooseDate.valueOf() + 86400000
          }
          break
        case "create":
          data['create_time_range'] = {
            start: chooseDate.valueOf(),
            end: chooseDate.valueOf() + 86400000
          }
          break
        case "complete":
          data['complete_time_range'] = {
            start: chooseDate.valueOf(),
            end: chooseDate.valueOf() + 86400000
          }
          break
      }

      const r = request({
        path: "/ddl/list",
        method: "POST",
        data: data
      })

      r.then((res) => {
        switch (mode) {
          case "ddl":
            ddls.ddl_list = res.data.data.ddl_list
            break
          case "create":
            ddls.create_list = res.data.data.ddl_list
            break
          case "complete":
            ddls.complete_list = res.data.data.ddl_list
            break
        }
      }).catch((reason) => {
        console.error("DDL fetch error: " + JSON.stringify(reason))
      }).finally(() => {
      })
    }

    return {
      state,
      ddls,
      chooseDate,
      getDateZhCNString
    }
  },
  onTabItemTap() {
    const getDateFormatString = (date: Date) => {
      console.log(String(date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate()))
      return String(date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate())
    }

    const r = request({
      path: "/history/stat",
      method: "POST",
    })
    r.then((res) => {
      this.completedRate = Math.round((res.data.data.completed_rate) * 1000) / 10
      this.completedNumber = res.data.data.completed_count
      this.urgentNumber = res.data.data.urgent_count
      this.overtimeNumber = res.data.data.overtime_count
      this.startDateStr = getDateFormatString(new Date(res.data.data.first_time))
      this.endDateStr = getDateFormatString(new Date(res.data.data.last_time))
    }).catch((reason) => {
      console.error("History fetch error: " + JSON.stringify(reason))
    }).finally(() => {
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

.nut-grid-item__content--surround {
  border-radius: 20px;
}

.nut-circleprogress-text {
  font-size: 22px;
}

.nut-collapse-item .collapse-wrapper .collapse-content, .nut-collapse-item .collapse-wrapper .collapse-extraRender, .nut-collapse-item .collapse-extraWrapper .collapse-content, .nut-collapse-item .collapse-extraWrapper .collapse-extraRender {
  background-color: #f9f9f9;
}

.nut-collapse-item .collapse-wrapper .collapse-content, .nut-collapse-item .collapse-wrapper .collapse-extraRender, .nut-collapse-item .collapse-extraWrapper .collapse-content, .nut-collapse-item .collapse-extraWrapper .collapse-extraRender {
  padding: 8px 10px;
}

.nut-calendar .nut-calendar-content .calendar-months-panel .calendar-month-con .calendar-month-day-active {
  border-radius: 12px;
}

.nut-calendar .nut-calendar-content .calendar-months-panel .calendar-month-con .calendar-month-day {
  height: 50px;
}

.nut-calendar .nut-calendar-content .calendar-months-panel .calendar-month-con .calendar-month-day .calendar-curr-tip-curr {
  bottom: 0;
}

</style>
