<template>
  <view class="home">
    <DdlListMenu/>
    <view
      v-for="data in ddlList"
      :key="data.ddl_time">
      <DdlCard :ddlData="data"/>
    </view>
  </view>
</template>

<script lang="ts">
import {reactive, ref, toRefs} from 'vue';
import DdlCard from "../../components/card/HomeDdlCard.vue";
import DdlListMenu from "../../components/menu/HomeDdlListMenu.vue";
import {DDLData} from "../../types/DDLData";

export default {
  name: 'home',
  components: {
    DdlCard,
    DdlListMenu
  },
  setup() {
    const ddls = reactive<{ ddlList: DDLData [] }>({
      ddlList:
        [{ddl_id: 1, title: "第一个DDL", ddl_time: new Date(1656453270035), from: "/assets/images/jxlf.png", content: "", tag: ""},
          {ddl_id: 2, title: "第二个DDL", ddl_time: new Date(1656453270035), from: "/assets/images/spoc.png", content: "", tag: ""},
          {ddl_id: 3, title: "第三个DDL", ddl_time: new Date(1656453270035), from: "/assets/images/mooc.png", content: "", tag: ""},
          {ddl_id: 4, title: "第四个DDL", ddl_time: new Date(1656453270035), from: "/assets/images/jxlf.png", content: "", tag: ""},
          {ddl_id: 5, title: "第五个DDL", ddl_time: new Date(1656453270035), from: "/assets/images/spoc.png", content: "", tag: ""},
          {ddl_id: 6, title: "第六个DDL", ddl_time: new Date(1656453270035), from: "/assets/images/mooc.png", content: "", tag: ""},
          {ddl_id: 7, title: "第七个DDL", ddl_time: new Date(1656453270035), from: "/assets/images/jxlf.png", content: "", tag: ""},
          {ddl_id: 8, title: "第八个DDL", ddl_time: new Date(1656453270035), from: "/assets/images/spoc.png", content: "", tag: ""},
          {ddl_id: 9, title: "第九个DDL", ddl_time: new Date(1656453270035), from: "/assets/images/mooc.png", content: "", tag: ""},]
    })
    return {
      ...toRefs(ddls)
    }
  }
}
</script>

<style>
.home {
  background: #f9f9f9;
}
</style>
