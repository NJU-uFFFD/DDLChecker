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
          <custom-wrapper>
            <nut-circleprogress
              :progress="completedRate"
              radius="70"
              strokeWidth="10"
              :clockwise="false"
              color="#2e6aff">
              <div style="color:#2e6aff">
                <div class="number_title">{{ completedRate }}</div>
                %
                <div>总完成率</div>
              </div>
            </nut-circleprogress>
          </custom-wrapper>
        </nut-grid-item>
        <nut-grid-item>
          <custom-wrapper>
            <nut-circleprogress
              progress="100"
              radius="70"
              strokeWidth="10"
              color="#29b877">
              <div style="color:#29b877">
                <div class="number_title">{{ completedNumber }}</div>
                件
                <div>已完成</div>
              </div>
            </nut-circleprogress>
          </custom-wrapper>
        </nut-grid-item>
        <nut-grid-item>
          <custom-wrapper>
            <nut-circleprogress
              progress="100"
              radius="70"
              strokeWidth="10"
              color="#e7a231">
              <div style="color:#e7a231">
                <div class="number_title">{{ urgentNumber }}</div>
                件
                <div>剩余紧急</div>
              </div>
            </nut-circleprogress>
          </custom-wrapper>
        </nut-grid-item>
        <nut-grid-item>
          <custom-wrapper>
            <nut-circleprogress
              progress="100"
              radius="70"
              strokeWidth="10"
              color="#cd0f0f">
              <div style="color:#cd0f0f">
                <div class="number_title">{{ overtimeNumber }}</div>
                件
                <div>已超时</div>
              </div>
            </nut-circleprogress>
          </custom-wrapper>
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
        "filter": {
          'is_deleted': false
        }
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

@font-face {
  font-family: 'REEJI-TaikoMagicGB-Flash';
  src: url('data:font/ttf;charset=utf-8;base64,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sgEBBUMQFBPtsDYcsRcDQ2SwBkNkUHmyFQUCQ7AAQ7ABFUhDsAdDsANDYEgcsQIFQ7ABQ7ABFUhDsARDsAZDYEgtAAAAtgIJAAooBQJCQkIrtUYHBwEGQEKIQkOwI1OwB0OwQFFaebAJuBAAsggIIIhCQ1R5sTAGuAEAQhywCbkEIEAAsAi4GGCIQmOwCENUebEUBrgBQEIcsAe5DCBAAGOwCENUebAGuAEAQrY2QAYFBQEGQ0RCQ1R5sS4FQ7AFUHmzBwkJBUNFQkOwXVB5sgoJQEIcsQkJQ7AGYWlCuP/MswUBBQVDsAlDRENgQhyxLAZDsEBSebEkBUOwBVB5uP/WtwUBBQUKCgoFQ0VCQ7AGQ2NpsAZDYkJDsApDRENgQhxLuBAAY2W4OphguBkAYrAKI0KxAApDUliwABuwCkNZHbANGgAAAAAAAAAAAAAAAAAAAAAAADICXgABAAAAAAAAADYAAAABAAAAAAABABgANgABAAAAAAACAAcATgABAAAAAAADACQAVQABAAAAAAAEABgANgABAAAAAAAFAFkAeQABAAAAAAAGABgANgABAAAAAAAHADoA0gABAAAAAAAIACwBDAABAAAAAAAJAA0BOAABAAAAAAALAA0BOAABAAAAAAAMAA0BOAABAAAAAAANAA0BOAABAAAAAAAOAA0BOAABAAAAAAAQABgANgABAAAAAAARAAQBRQABAAAAAAASABgANgADAAEECQAAAGwBSQADAAEECQABADABtQADAAEECQACAA4B5QADAAEECQADAEgB8wADAAEECQAEADABtQADAAEECQAFALICOwADAAEECQAGADABtQADAAEECQAHAHQC7QADAAEECQAIAFgDYQADAAEECQAJABoDuQADAAEECQALABoDuQADAAEECQAMABoDuQADAAEECQANABoDuQADAAEECQAOABoDuQADAAEECQAQADABtQADAAEECQARAAgD0wADAAEECQASADABtQADAAEIBAAAACAD2wADAAEIBAABABYD+wADAAEIBAACAA4B5QADAAEIBAADAEgB8wADAAEIBAAEABYD+wADAAEIBAAFAGYEEQADAAEIBAAHAEAEdwADAAEIBAAIABgEtwADAAEIBAAJABoDuQADAAEIBAALABoDuQADAAEIBAAMABoDuQADAAEIBAANABoDuQAD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') format('truetype');
  font-weight: bold;
  font-style: normal;
  font-display: swap;
}

.number_title {
  font-family: 'REEJI-TaikoMagicGB-Flash', serif;
  font-size: 28px;
  display: inline-block
}

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
  font-size: 14px;
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
