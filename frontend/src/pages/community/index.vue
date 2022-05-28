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
      style="height: 93vh;"
      @scrolltolower="listLower"
      enableBackToTop="true">

      <nut-cell v-for="course in courses" :key="course" @click="openCourse(course)">
        {{ JSON.stringify(course) }}
      </nut-cell>

    </scroll-view>
  </view>
</template>

<script>
import {reactive, ref} from 'vue'
import Taro from "@tarojs/taro";
import {request} from "../../util/request";

export default {
  name: "community",

  data() {
    return {
      courses: [],
      page: 1
    }
  },

  methods: {
    listLower() {

    },
    openCourse(data) {
      Taro.navigateTo({
        url: '/pages/courseddl/index?course_uuid=' + data.course_uuid
      })
    }
  },
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
  },
  onTabItemTap() {
    // 更新内容
    this.page = 1

    const r = request({
      method: "POST",
      path: "/community/course/list",
      data: {
        page: this.page,
        size: 10
      }
    })

    r.then((res) => {
      this.courses = res.data.data.courses
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


</style>
