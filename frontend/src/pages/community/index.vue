<template>
  <view class="page">
    <nut-searchbar
      style="position: relative; z-index: 1; box-shadow: 0 4px 16px 0 rgba(237, 238, 241, 1)"
      v-model="state.searchValue"
      placeholder="请输入社区课程及DDL"
      clearable
      max-length="32"
      @search="searchCourseOrDdl">
      <template
        v-slot:leftin>
        <nut-icon
          size="14"
          name="search2"/>
      </template>
    </nut-searchbar>

    <scroll-view
      :scroll-y="true"
      style="height: 100vh;">
      <nut-cell-group
        title="大家的课程"/>
      <nut-cell/>
      <nut-cell-group
        title="大家的 DDL"/>
      <nut-cell/>
    </scroll-view>
  </view>
</template>

<script lang="ts">
import {reactive, ref} from 'vue'
import Taro from "@tarojs/taro";

export default {
  name: "community",
  setup() {
    const state = reactive({
      searchValue: "",
      searching: false
    })

    const searchCourseOrDdl = () => {
      console.log("search " + state.searchValue)
    }

    return {
      state,
      searchCourseOrDdl
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


</style>
