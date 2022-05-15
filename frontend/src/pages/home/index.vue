<template>
  <view class="home">
    <HomeDdlListMenu
      @sortMode="sortDdlList"/>
    <view
      v-for="data in ddlList"
      :key="data">
      <HomeDdlCard :ddlData="data"/>
    </view>

    <!-- 手动添加 ddl 的弹出层 -->
    <view>
      <nut-overlay v-model:visible="state.showAdd" :close-on-click-overlay=false :z-index="200">
        <nut-form>
          <nut-form-item label="代办事项标题">
            <input class="nut-input-text" placeholder="请输入代办事项标题" type="text"/>
          </nut-form-item>
          <nut-form-item label="Deadline">

            <nut-cell title="显示中文" :desc="state.addInfo.date" @click="state.datePickerShow = true"></nut-cell>

            <nut-datepicker
              v-model="state.addInfo.date"
              v-model:visible="state.datePickerShow"
              :is-show-chinese="true"
            ></nut-datepicker>
          </nut-form-item>
          <nut-form-item label="详细说明">
            <input class="nut-input-text" placeholder="请输入详细说明" type="text"/>
          </nut-form-item>
          <nut-form-item label="地址">
            <input class="nut-input-text" placeholder="请输入地址" type="text"/>
          </nut-form-item>
          <nut-form-item label="备注">
            <nut-textarea placeholder="请输入备注" type="text"/>
          </nut-form-item>
        </nut-form>
      </nut-overlay>
    </view>

    <!-- 手动添加 ddl 的按钮 -->
    <nut-button type="primary" id="add_button" @click="addDdl">+</nut-button>
  </view>
</template>

<script lang="ts">
import {reactive, toRefs} from 'vue';
import HomeDdlCard from "../../components/card/HomeDdlCard.vue";
import HomeDdlListMenu from "../../components/menu/HomeDdlListMenu.vue";
import {DDLData} from "../../types/DDLData";
import Taro from "@tarojs/taro";
import {request} from "../../util/request"

export default {
  name: 'home',
  components: {
    HomeDdlCard,
    HomeDdlListMenu
  },
  setup() {
    const ddls = reactive<{ ddlList: DDLData [] }>({
      ddlList:
        [{
          id: 1,
          title: "第一个DDL",
          ddl_time: new Date(1656454270035),
          from: "/assets/images/jxlf.png",
          content: "",
          tag: ""
        },
          {
            id: 2,
            title: "第二个DDL",
            ddl_time: new Date(1655453250035),
            from: "/assets/images/spoc.png",
            content: "",
            tag: ""
          },
          {
            id: 3,
            title: "第三个DDL",
            ddl_time: new Date(1656453270035),
            from: "/assets/images/mooc.png",
            content: "",
            tag: ""
          },
          {
            id: 6,
            title: "第四个DDL",
            ddl_time: new Date(1656452440035),
            from: "/assets/images/jxlf.png",
            content: "",
            tag: ""
          },
          {
            id: 5,
            title: "第五个DDL",
            ddl_time: new Date(1656456270035),
            from: "/assets/images/spoc.png",
            content: "",
            tag: ""
          },
          {
            id: 4,
            title: "第六个DDL",
            ddl_time: new Date(1656463270435),
            from: "/assets/images/mooc.png",
            content: "",
            tag: ""
          },
          {
            id: 7,
            title: "第七个DDL",
            ddl_time: new Date(1652323272435),
            from: "/assets/images/jxlf.png",
            content: "",
            tag: ""
          },
          {
            id: 8,
            title: "第八个DDL",
            ddl_time: new Date(1656453270235),
            from: "/assets/images/spoc.png",
            content: "",
            tag: ""
          },
          {
            id: 9,
            title: "第九个DDL",
            ddl_time: new Date(1656434458035),
            from: "/assets/images/mooc.png",
            content: "",
            tag: ""
          },]
          .sort((o1, o2) => o1.ddl_time.valueOf() - o2.ddl_time.valueOf())
      //初始以由近至远排序
    })

    let state = reactive({
      "showAdd": false,
      "datePickerShow": false,
      "addInfo": {
        "title": "",
        "date": new Date()
      }
    })

    function sortDdlList(mode: string) {
      ddls.ddlList = ddls.ddlList.sort((o1, o2) => {
        switch (mode) {
          case "a":
            return o1.ddl_time.valueOf() - o2.ddl_time.valueOf()
          case "b":
            return o2.ddl_time.valueOf() - o1.ddl_time.valueOf()
          case "c":
            return o1.id - o2.id
          default:
            return o2.id - o1.id
        }
      })
    }

    function addDdl() {
      state.showAdd = true

    }

    // function fetchDdls() {
    //   const r = request({
    //     path: "/ddl/list",
    //     method: "POST",
    //     data: {}
    //   })
    //   console.log(r)
    //
    //   r.then((res) => {
    //     console.log(res.data.data.ddl_list)
    //   })
    // }
    //
    // fetchDdls()

    return {
      ...toRefs(ddls),
      sortDdlList,
      addDdl,
      state
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
</style>
