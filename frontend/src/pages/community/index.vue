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
      <nut-swipe v-for="course in courses" :key="course">
        <CommunityCourseCard
          :course="course"
          @onClick="openCourse(course)"
          @onSubscribeStatusChange="subscribe"/>
        <template #right>
          <nut-button
            style="height:100%; border-radius: 10px;margin-right: 5px"
            type="danger"
            @click="showDelete=true;deleteInfo=course">
            删除
          </nut-button>
        </template>
      </nut-swipe>
      <nut-divider v-if="!more">没有更多课程了捏</nut-divider>
    </scroll-view>


    <!-- 手动添加课程的弹出层 -->
    <nut-popup
      position="bottom"
      style="height:40vh;"
      round
      safe-area-inset-bottom
      v-model:visible="showAdd">
      <nut-cell-group style="position:relative;top:2vh;width:90vw;left:5vw;box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1)">
        <nut-cell>
          <nut-input
            v-model="addInfo.title"
            style="height: auto;font-size: 20px;padding-left: 0;"
            maxLength="32"
            :border="false"
            placeholder="新建课程"
          />
        </nut-cell>
      </nut-cell-group>
      <nut-button
        type="info"
        plain
        style="height:8vh;width:40vw;left:6.6vw;position:fixed;bottom: 5vh;font-size: 20px"
        @click="showAdd = false;">
        取消
      </nut-button>
      <nut-button
        type="info"
        style="height:8vh;width:40vw;right:6.6vw;position:fixed;bottom: 5vh;font-size: 20px"
        @click="submitCourse"
        :loading="courseAddSubmitting">
        添加
      </nut-button>
    </nut-popup>

    <!--  删除课程相关  -->
    <nut-dialog
      title="删除课程"
      content="无法删除非本人创建的课程哦~"
      close-on-click-overlay
      lock-scroll
      v-model:visible="showDelete">
      <template #footer>
        <nut-button plain type="danger" @click="showDelete = false">取消</nut-button>
        <nut-button type="danger" @click="deleteCourse(deleteInfo)">删除</nut-button>
      </template>
    </nut-dialog>


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

    <!-- 手动添加课程的按钮 -->
    <nut-button
      type="primary"
      class="add_button"
      style="position: fixed;height: 8vh;width: 8vh;right: 30px;bottom: 30px;border-radius:4vh;box-shadow: 0 4px 15px 0 rgba(237, 238, 241, 10)"
      icon="uploader"
      @click="showAdd = true"/>

  </view>
</template>

<script>
import {reactive, ref} from 'vue'
import Taro from "@tarojs/taro";
import {request} from "../../util/request";
import CommunityCourseCard from "../../components/card/CommunityCourseCard.vue";
import {DDLData} from "../../types/DDLData";

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
      addInfo: {
        title: ''
      },
      searchValue: '',
      searching: false,
      showAdd: false,
      courseAddSubmitting: false,
      deleteInfo: '',
      showDelete: false
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
      this.more = false
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
    },
    submitCourse() {
      if (this.addInfo.title.length === 0) {
        Taro.showModal({
          title: '提示',
          content: '添加的课程不得为空.',
          showCancel: false
        })
        return
      }
      if (this.addInfo.title.length > 32) {
        openToast('fail', "课程标题过长!")
        return
      }
      this.courseAddSubmitting = true
      const r = request({
        "method": "POST",
        "path": "/community/course/add",
        "data": {
          "course_name": this.addInfo.title,
          "platform_uuid": '00000000-0000-0000-0000-000000000000'
        }
      })

      r.then((res) => {
        if (res.statusCode === 200 && res.data.code === 0) {
          this.showAdd = false
          this.openToast('success', "添加成功!")
        } else {
          throw JSON.stringify(res)
        }
      }).catch((reason) => {
        Taro.showModal({
          title: '错误',
          content: '添加课程出错: ' + JSON.stringify(reason),
          showCancel: false
        })
      }).finally(() => {
        this.addInfo = {
          "title": "",
        }
        this.showAdd = false
        this.courseAddSubmitting = false
        this.page = 1
        this.searchValue = ''
        this.more = true
        this.fetchCourses(this.page, 10, this.searchValue, (d) => {
          this.courses = d
          this.page += 1
        })
      })
    },
    deleteCourse(course) {
      this.showDelete = false
      console.log("删除课程: " + course.course_name)
      const r = request({
        method: "POST",
        path: "/community/course/delete",
        data: {
          "course_uuid": course.course_uuid
        }
      })

      r.then((res) => {
        if (res.statusCode === 200 && res.data.code === 0) {
          this.openToast('success', "删除成功!")
        } else {
          throw JSON.stringify(res)
        }
      }).catch((reason) => {
        Taro.showModal({
          title: '错误',
          content: '删除课程出错: ' + JSON.stringify(reason),
          showCancel: false
        })
      }).finally(() => {
        this.page = 1
        this.searchValue = ''
        this.fetchCourses(this.page, 10, this.searchValue, (d) => {
          this.courses = d
          this.page += 1
        })
      })
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
