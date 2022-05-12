<template>
  <view class="home">
    <HomeDdlListMenu
      @sortMode="sortDdlList"/>
    <view
      v-for="data in ddlList"
      :key="data">
      <HomeDdlCard :ddlData="data"/>
    </view>
  </view>

  <nut-button type="primary" id="add_button">+</nut-button>

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
    // const ddls = reactive<{ ddlList: DDLData [] }>({
    //   ddlList:
    //     [{ddl_id: 1, title: "第一个DDL", ddl_time: new Date(1656454270035), from: "/assets/images/jxlf.png", content: "", tag: ""},
    //       {ddl_id: 2, title: "第二个DDL", ddl_time: new Date(1655453250035), from: "/assets/images/spoc.png", content: "", tag: ""},
    //       {ddl_id: 3, title: "第三个DDL", ddl_time: new Date(1656453270035), from: "/assets/images/mooc.png", content: "", tag: ""},
    //       {ddl_id: 6, title: "第四个DDL", ddl_time: new Date(1656452440035), from: "/assets/images/jxlf.png", content: "", tag: ""},
    //       {ddl_id: 5, title: "第五个DDL", ddl_time: new Date(1656456270035), from: "/assets/images/spoc.png", content: "", tag: ""},
    //       {ddl_id: 4, title: "第六个DDL", ddl_time: new Date(1656463270435), from: "/assets/images/mooc.png", content: "", tag: ""},
    //       {ddl_id: 7, title: "第七个DDL", ddl_time: new Date(1652323272435), from: "/assets/images/jxlf.png", content: "", tag: ""},
    //       {ddl_id: 8, title: "第八个DDL", ddl_time: new Date(1656453270235), from: "/assets/images/spoc.png", content: "", tag: ""},
    //       {ddl_id: 9, title: "第九个DDL", ddl_time: new Date(1656434458035), from: "/assets/images/mooc.png", content: "", tag: ""},]
    //       .sort((o1, o2) => o1.ddl_time.valueOf() - o2.ddl_time.valueOf())
    //   //初始以由近至远排序
    // })

    const ddls = {ddlList: []};

    function sortDdlList(mode: string) {
      ddls.ddlList = ddls.ddlList.sort((o1, o2) => {
        switch (mode) {
          case "a":
            return o1.ddl_time.valueOf() - o2.ddl_time.valueOf()
          case "b":
            return o2.ddl_time.valueOf() - o1.ddl_time.valueOf()
          case "c":
            return o1.ddl_id - o2.ddl_id
          default:
            return o2.ddl_id - o1.ddl_id
        }
      })
    }

    function fetchDdls() {
      const r = request({
        path: "/ddl/list",
        method: "POST",
        data: {}
      })
      console.log(r)

      r.then((res) => {
        console.log(res.data.data.ddl_list)
      })
    }

    fetchDdls()

    return {
      ...toRefs(ddls),
      sortDdlList,
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
