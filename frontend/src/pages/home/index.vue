<template>
  <view class="home">
    <ddl_list_menu/>
    <view v-for="item in ddl_list">
      <ddl_card :ddl_item="item"/>
    </view>
  </view>
</template>

<script lang="ts">
import {reactive, ref, toRefs} from 'vue';
import ddl_card from "../../components/card/ddl_card.vue";
import ddl_list_menu from "../../components/menu/ddl_list_menu.vue";
import {DDL_List} from "../../types/DDL_List";

export default {
  name: 'home',
  components: {
    ddl_card,
    ddl_list_menu
  },
  setup() {
    const msg = ref('Hello world')
    const ddls = reactive<{ ddl_list: DDL_List [] }>({
      ddl_list:
        [{id: 1, title: "第一个DDL", ddl_time: "2022/04/30 23:59", from: "/assets/images/jxlf.png"},
          {id: 2, title: "第二个DDL", ddl_time: "2022/05/06 23:59", from: "/assets/images/spoc.png"},
          {id: 3, title: "第三个DDL", ddl_time: "2022/06/10 23:59", from: "/assets/images/mooc.png"},
          {id: 4, title: "第四个DDL", ddl_time: "2022/04/30 23:59", from: "/assets/images/jxlf.png"},
          {id: 5, title: "第五个DDL", ddl_time: "2022/05/06 23:59", from: "/assets/images/spoc.png"},
          {id: 6, title: "第六个DDL", ddl_time: "2022/06/10 23:59", from: "/assets/images/mooc.png"},
          {id: 7, title: "第七个DDL", ddl_time: "2022/04/30 23:59", from: "/assets/images/jxlf.png"},
          {id: 8, title: "第八个DDL", ddl_time: "2022/05/06 23:59", from: "/assets/images/spoc.png"},
          {id: 9, title: "第九个DDL", ddl_time: "2022/06/10 23:59", from: "/assets/images/mooc.png"},]
    })
    return {
      msg,
      ...toRefs(ddls)
    }
  }
}
</script>

<style scoped>
.home {
  background: #f9f9f9;
}
</style>
