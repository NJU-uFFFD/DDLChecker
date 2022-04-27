<template>
  <nut-cell
    class="home-ddl-card"
    :title=ddlData.title
    :sub-title=ddlData.ddl_time.toLocaleString()
    desc="查看详情"
    @click="testClick">
    <template
      #icon>
      <img
        class="home-site-icon"
        :src=ddlData.from
      />
    </template>
  </nut-cell>
</template>

<script lang="ts">
import {ref} from 'vue';
import {Toast} from '@nutui/nutui-taro';
import {DDLData} from "../../types/DDLData";

export default {
  props: {
    ddlData: Object as () => DDLData
  },
  setup() {
    const switchChecked = ref(true);
    const testClick = (event) => {
      Toast.text('点击事件');
    };
    return {
      testClick,
      switchChecked,
    };
  }
}
</script>

<style>

.home-ddl-card {
  margin-top: 12px;
  margin-bottom: 10px;
  align-items: center;
  margin-left: 10px;
  width: 95%;
  height: 88px;
  border-radius: 20px;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.home-site-icon {
  width: 30px;
  height: 30px;
  margin-top: 0;
  margin-left: 0;
  margin-right: 20px;
}

</style>
