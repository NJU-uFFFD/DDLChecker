<template>
  <view class="page">
    <!-- 搜索栏 -->
    <nut-searchbar
      style="position: relative; z-index: 200; "
      v-model="searchValue"
      placeholder="请输入社区课程名称或关键词"
      clearable
      max-length="32"
      @change="listRefresh"
      @blur="listRefresh"
      @search="listRefresh"
      @clear="listRefresh">
      <template
        #leftin>
        <nut-icon
          size="14"
          name="search2"/>
      </template>
    </nut-searchbar>

    <!-- 筛选菜单 -->
    <nut-menu
      style="position: relative; z-index: 100;box-shadow: 0 4px 16px 0 rgba(237, 238, 241, 1)">
      <nut-menu-item title="筛选平台">
        <div style="display: flex; flex: 1; justify-content: space-between; align-items: center">
          <nut-checkboxgroup
            v-model="menu.filterCheckboxGroup"
            ref="filterGroup"
            @change="listRefresh">
            <nut-checkbox
              v-for="item in menu.filterCheckboxSource"
              :key="item.label"
              :label="item.label"
              icon-size="24"
              style="display: flex; height: 6vh; width:50vw">{{ item.value }}
            </nut-checkbox>
          </nut-checkboxgroup>
        </div>
      </nut-menu-item>
      <nut-menu-item
        v-model="menu.value"
        @change="listRefresh"
        :options="menu.options"/>
    </nut-menu>


    <scroll-view
      :refresher-triggered="refreshing"
      :scroll-y="true"
      style="height: 85vh;"
      @scrolltolower="listLower"
      @refresherrefresh="listRefresh"
      refresherEnabled="true"
      enableBackToTop="true">
      <nut-swipe v-for="course in courses" :key="course">
        <CommunityCourseCard
          :course="course"
          @onClick="openCourse(course)"
          @onSubscribeStatusChange="subscribe"/>
        <template #right>
          <nut-button
            style="height:100%; border-radius: 10px"
            type="danger"
            @click="showDelete=true;deleteInfo=course">
            删除
          </nut-button>
        </template>
      </nut-swipe>
      <nut-divider style="margin: 30px 0" v-if="!more">没有更多课程了捏</nut-divider>
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
      showDelete: false,
      refreshing: false,
      menu: {
        options: [
          {text: '全部', value: false},
          {text: '已订阅', value: true},
        ],
        value: false,
        filterCheckboxGroup: ['1', '2', '3', '4'],
        filterCheckboxSource: [
          {label: '1', value: '教学立方'},
          {label: '2', value: '南大SPOC'},
          {label: '3', value: '中国大学MOOC'},
          {label: '4', value: '手动添加'},
        ]
      },
      filterGroup: null
    }
  },

  methods: {
    fetchCourses(page, size, searchValue, callback) {
      let filter = {}
      if (this.menu.value) filter["is_subscribed"] = true

      let platform_uuids = []
      if (this.menu.filterCheckboxGroup.indexOf('1') === -1)
        platform_uuids.push('f15684f5-d870-4a9d-b859-e7eec3c6e3b5')
      if (this.menu.filterCheckboxGroup.indexOf('2') === -1)
        platform_uuids.push('68dc1014-7bfe-4ea3-a000-5734303d9f59')
      if (this.menu.filterCheckboxGroup.indexOf('3') === -1)
        platform_uuids.push('69921ef9-fe15-4731-930d-b60a644da254')
      if (this.menu.filterCheckboxGroup.indexOf('4') === -1)
        platform_uuids.push('00000000-0000-0000-0000-000000000000')

      let data = {
        page: this.page,
        size: size,
        filter: filter,
        platform_uuids: platform_uuids
      }

      if (this.searchValue !== '')
        data["key_word"] = this.searchValue

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
      }).finally(() => {
        this.refreshing = false
      })
    },
    listLower() {
      if (!this.more) {
        return
      }

      if (this.refreshing) {
        return
      }

      this.fetchCourses(this.page, 10, this.searchValue, (data) => {
        this.courses.push.apply(this.courses, data)
        this.page += 1
      })
    },
    listRefresh() {
      if (this.refreshing) return
      this.refreshing = true
      this.page = 1
      this.more = true
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
