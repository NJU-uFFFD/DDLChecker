<template>
  <view class="page">
    <nut-searchbar
      style="position: relative; z-index: 1; box-shadow: 0 4px 16px 0 rgba(237, 238, 241, 1)"
      v-model="searchValue"
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
      style="height: 94vh;"
      @scrolltolower="listLower"
      enableBackToTop="true">

      <!--      <nut-swipe v-for="course in courses" :key="course">-->
      <CommunityCourseCard
        v-for="course in courses"
        :key="course"
        :course="course"
        @onClick="openCourse(course)"
        @onSubscribeStatusChange="subscribe"/>
      <!--        <template #right>-->
      <!--          <nut-button-->
      <!--            style="height:100%; border-radius: 10px;margin-right: 5px"-->
      <!--            type="primary"-->
      <!--            @click="subscribe(course)">-->
      <!--            订阅-->
      <!--          </nut-button>-->
      <!--        </template>-->
      <!--      </nut-swipe>-->
      <nut-divider v-if="!more">没有更多课程了捏</nut-divider>
    </scroll-view>
    <!-- Toast -->
    <nut-toast
      :msg="toastInfo.msg"
      v-model:visible="toastInfo.show"
      :type="toastInfo.type"
      @closed="toastInfo.onClosed"
      :cover="toastInfo.cover"
      :duration="1000"
      bg-color="rgba(0, 0, 0, 0.5)"
      :center="false"
      bottom="16%"
    />

  </view>
</template>

<script>
import {reactive, ref} from 'vue'
import Taro from "@tarojs/taro";
import {request} from "../../util/request";
import CommunityCourseCard from "../../components/card/CommunityCourseCard.vue";

export default {
  name: "community",
  components: {
    CommunityCourseCard
  },
  data() {
    return {
      courses: [],
      page: 1,
      more: true,
      toastInfo: {
        msg: 'toast',
        type: 'text',
        show: false,
        cover: false,
      },
      searchValue: '',
      searching: false
    }
  },

  methods: {
    fetchCourses(page, size, searchValue, callback) {
      const data = {
        page: this.page,
        size: size,
      }
      if (searchValue !== '')
        data["key_word"] = searchValue
      const r = request({
        method: "POST",
        path: "/community/course/list",
        data: data
      })

      r.then((res) => {
        if (res.statusCode === 200 && res.data.code === 0) {
          if (page >= res.data.data.total_pages) {
            this.more = false
          }
          callback(res.data.data.courses)
        } else {
          console.error(res)
        }
      }).catch((reason) => {
        console.error(reason)
      })
    },
    listLower() {
      if (!this.more) {
        return
      }

      this.fetchCourses(this.page, 10, this.searchValue, (data) => {
        this.courses.push.apply(this.courses, data)
        this.page += 1
      })
    },
    searchCourseOrDdl() {
      this.page = 1
      this.fetchCourses(this.page, 10, this.searchValue, (d) => {
        this.courses = d
        this.page += 1
      })
    },
    openCourse(data) {
      Taro.navigateTo({
        url: '/pages/courseddl/index?course_uuid=' + data.course_uuid + "&course_title=" + data.course_name
      })
    },
    subscribe(data) {
      console.log((data.subscribed === true ? "订阅课程 ID: " : "撤销订阅课程 ID: ") + data.course_uuid + " 并更新")
      const sPath = data.subscribed === true ? "/community/course/subscribe" : "/community/course/unsubscribe"
      const r = request({
        method: "POST",
        path: sPath,
        data: {
          "course_uuid": data.course_uuid,
        }
      })

      r.then((res) => {
        if (res.statusCode === 200 && res.data.code === 0) {
          this.openToast('success', data.subscribed === true ? "订阅课程成功!" : "撤销订阅成功!")
        } else {
          throw JSON.stringify(res)
        }
      }).catch((reason) => {
        Taro.showModal({
          title: '错误',
          content: (data.subscribed === true ? '订阅课程出错: ' : '撤销订阅出错: ') + JSON.stringify(reason),
          showCancel: false
        })
      })
    },
    openToast(type, msg) {
      this.toastInfo.show = true
      this.toastInfo.msg = msg
      this.toastInfo.type = type
    }
  },
  setup() {
  },
  onTabItemTap() {
    // 更新内容
    this.page = 1
    this.more = true
    this.courses = []
    this.searchValue = ''

    this.fetchCourses(1, 10, this.searchValue, (d) => {
      this.courses = d
      this.page += 1
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
