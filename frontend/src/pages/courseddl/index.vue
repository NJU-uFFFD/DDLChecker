<template>
  <view class="page">
    <scroll-view
      :scroll-y="true"
      @scrolltolower="listLower"
      style="height: 96vh;">
      <nut-cell-group
        :title="course_title"/>
      <nut-cell
        class="add-ddl-card"
        title="添加 DDL 到此门课程"
        @click="showAdd = true">
        <template #icon>
          <img
            class="course-ddl-site-icon"
            src="/assets/images/add.png"
          />
        </template>
      </nut-cell>

      <nut-swipe v-for="ddl in ddls" :key="ddl">
        <nut-cell
          class="course-ddl-card"
          :style="{color:(ddl.ddl_time<now.valueOf())?'#ee1919':'#676767'}"
          :title="ddl.title.substring(0, 30) + (ddl.title.length > 30 ? '...' : '')"
          :sub-title=formatTime(ddl.ddl_time)
          @click="showDetail(ddl)">
          <template #icon>
            <img
              class="course-ddl-site-icon"
              :src="getPlatformInfo(ddl.platform_uuid).icon"/>
          </template>

          <template #link>
            <nut-button
              type="info"
              :plain="ddl.added"
              :disabled="ddl.added"
              @click.stop="fetchDdl(ddl)">
              {{ ddl.added ? "已添加" : "添加" }}
            </nut-button>
          </template>
        </nut-cell>

        <template #right>
          <nut-button
            style="height:100%; border-radius: 10px"
            type="danger"
            @click="showDelete=true;deleteInfo=ddl">
            删除
          </nut-button>
        </template>
      </nut-swipe>

      <nut-divider v-if="!more">没有更多 DDL 了捏</nut-divider>
    </scroll-view>


    <nut-dialog
      :title="ddlDetailData.title"
      close-on-click-overlay
      lock-scroll
      v-model:visible="showDetails">
      <nut-countdown
        #default
        :style="{display: 'flex',justifyContent:'center',color:(ddlDetailData.ddl_time<now.valueOf()&&!ddlDetailData.is_completed)?'#ee1919':'#676767'}"
        :end-time="ddlDetailData.ddl_time"
        :format="ddlDetailData.ddl_time>now.valueOf()?'还剩 DD 天 HH 时 mm 分 ss 秒':'已超时'"
      />
      <nut-cell
        style="box-shadow: 0 0 0 0"
        :title="ddlDetailData.content"/>
      <template #footer>
        <div style="color: #676767">
          {{ detailUsername === "" ? "该 DDL 由系统自动获取" : "该 DDL 由用户 `" + detailUsername + "` 创建" }}
        </div>
      </template>
    </nut-dialog>

    <!-- 删除 ddl 弹窗  -->
    <nut-dialog
      title="删除 DDL"
      content="真的要从社区中删除这个 DDL 吗?"
      close-on-click-overlay
      lock-scroll
      v-model:visible="showDelete">
      <template #footer>
        <nut-button plain type="danger" @click="showDelete = false">取消</nut-button>
        <nut-button type="danger" @click="deleteCourseDdl(deleteInfo)">删除</nut-button>
      </template>
    </nut-dialog>

    <!-- 手动添加 DDL 的弹出层 -->
    <nut-popup
      position="bottom"
      style="height:80vh;"
      round
      safe-area-inset-bottom
      v-model:visible="showAdd">
      <nut-cell-group
        style="position:relative;top:2vh;width:90vw;left:5vw;box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1)">
        <nut-cell>
          <nut-input
            v-model="addInfo.title"
            style="height: auto;font-size: 20px;padding-left: 0;"
            maxLength="32"
            :border="false"
            placeholder="新建待办"
          />
        </nut-cell>
        <nut-cell>
          <nut-input
            style="height: auto;font-size: 20px;padding-left: 0;"
            :border="false"
            disabled
            :placeholder="addInfo.pickerDate.toLocaleString()"
            @click.stop="addInfo.datePickerShow = true"
          />
        </nut-cell>
        <nut-cell>
          <nut-input
            v-model="addInfo.content"
            style="height: auto;font-size: 20px;max-height: 40vh;padding-left: 0;padding-bottom: 0"
            type="textarea"
            show-word-limit
            :rows="Math.floor(addInfo.content.length/20)+2<11?Math.floor(addInfo.content.length/20)+2:11"
            maxLength="128"
            :border="false"
            placeholder="请输入待办详情"
          />
        </nut-cell>
      </nut-cell-group>
      <nut-button
        type="info"
        plain
        style="height:8vh;width:40vw;left:6.6vw;position:fixed;bottom: 5vh;font-size: 20px"
        @click="showAdd = false">
        取消
      </nut-button>
      <nut-button
        type="info"
        style="height:8vh;width:40vw;right:6.6vw;position:fixed;bottom: 5vh;font-size: 20px"
        @click="submitCourseDdl"
        :loading="ddlAddSubmitting">
        添加
      </nut-button>
    </nut-popup>

    <nut-datepicker
      v-model="addInfo.pickerDate"
      type="datetime"
      title="Deadline 选择"
      v-model:visible="addInfo.datePickerShow"
      @confirm="({selectedValue : t}) => addInfo.pickerDate = new Date(t[0], t[1] - 1, t[2], t[3], t[4])"
      :min-date="getMinDate()"
    />

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

import Taro, {getCurrentInstance} from "@tarojs/taro";
import {formatTime, getPlatformInfo} from "../../util/ui";
import {request} from "../../util/request";
import Toast from "@nutui/nutui-taro";
import {reactive} from "vue/dist/vue";

export default {
  name: "index",
  setup() {

    return {
      getPlatformInfo,
      formatTime
    }
  },

  data() {
    return {
      ddls: [],
      page: 1,
      more: true,
      course_uuid: "",
      course_title: "",
      ddlDetailData: {},
      showDetails: false,
      detailUsername: "",
      showAdd: false,
      addInfo: {
        title: "",
        content: "",
        pickerDate: new Date(),
        datePickerShow: false
      },
      ddlAddSubmitting: false,
      toastInfo: {
        msg: 'toast',
        type: 'text',
        show: false,
        cover: false,
        title: '',
        bottom: '',
        center: true,
      },
      showDelete: false,
      deleteInfo: {},
      now: new Date
    }
  },
  methods: {
    listDdls(cid, page, size, callback) {
      const r = request({
        method: "POST",
        path: "/community/ddl/list",
        data: {
          page: this.page,
          size: 10,
          course_uuid: cid
        }
      })

      r.then((res) => {
        if (res.statusCode === 200 && res.data.code === 0) {
          if (page >= res.data.data.total_pages) {
            this.more = false
          }
          callback(res.data.data.source_ddls)
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

      this.listDdls(this.course_uuid, this.page, 10, (l) => {
        this.ddls.push.apply(this.ddls, l)
        this.page += 1
      })
    },

    fetchDdl(data) {
      const r = request({
        method: "POST",
        path: "/community/ddl/fetch",
        data: {
          id: data.id
        }
      })

      r.then((res) => {
        if (res.statusCode === 200 && res.data.code === 0) {
          for (let i = 0; i < this.ddls.length; i++) {
            if (this.ddls[i].id === data.id) {
              this.ddls[i].added = true
            }
          }
        } else {
          console.error(res)
        }
      }).catch((reason) => {
        console.error(reason)
      })
    },

    showDetail(ddl) {
      this.showDetails = true;
      this.ddlDetailData = ddl;

      console.log(ddl)

      if (ddl.creator_id !== null) {
        const r = request({
          method: "POST",
          path: "/user/username",
          data: {
            id: ddl.creator_id
          }
        })

        r.then((res) => {
          if (res.statusCode === 200 && res.data.code === 0) {
            this.detailUsername = res.data.data.username
          } else {
            console.error(res)
          }
        }).catch((reason) => {
          console.error(reason)
        })
      } else {
        this.detailUsername = ""
      }
    },
    submitCourseDdl() {
      console.log(this.addInfo)
      if (this.addInfo.content.length === 0 || this.addInfo.title.length === 0) {
        Taro.showModal({
          title: '提示',
          content: '添加的 DDL 标题和内容不得为空.',
          showCancel: false
        })
        return
      }
      this.ddlAddSubmitting = true
      const r = request({
        method: "POST",
        path: "/community/ddl/add",
        data: {
          course_uuid: this.course_uuid,
          title: this.addInfo.title,
          content: this.addInfo.content,
          ddl_time: this.addInfo.pickerDate.getTime()
        }
      })

      r.then((res) => {
        if (res.statusCode === 200 && res.data.code === 0) {
          this.showAdd = false
          this.openToast('success', "添加成功!")
          this.addInfo = {
            title: "",
            content: "",
            pickerDate: new Date(),
            datePickerShow: false
          }
          this.refreshList()
        } else {
          throw JSON.stringify(res)
        }
      }).catch((reason) => {
        Taro.showModal({
          title: '错误',
          content: '添加代办出错: ' + JSON.stringify(reason),
          showCancel: false
        })
      }).finally(() => {
        this.ddlAddSubmitting = false
      })
    },
    // 获取 DDL 时间下限
    getMinDate() {
      let now = new Date()
      return new Date(now.setDate(now.getDate() - 30))
    },
    openToast(type, msg, cover = false, title = "", bottom = "", center = true) {
      this.toastInfo.show = true
      this.toastInfo.msg = msg
      this.toastInfo.type = type
      this.toastInfo.cover = cover
      this.toastInfo.title = title
      this.toastInfo.bottom = bottom
      this.toastInfo.center = center
    },
    deleteCourseDdl(ddl) {
      this.showDelete = false

      const r = request({
        method: "POST",
        path: "/community/ddl/delete",
        data: {
          id: ddl.id
        }
      })

      r.then((res) => {
        if (res.statusCode !== 200) {
          console.error(res)
          return
        }

        if (res.data.code !== 0) {
          Taro.showModal({
            title: '提示',
            content: "删除失败: " + res.data.msg,
            showCancel: false
          })
          return
        }

        this.openToast("success", "删除成功!")
        this.refreshList()
      }).catch((reason) => {
        console.error(reason)
      })
    },
    refreshList() {
      this.page = 1
      this.more = true
      this.ddls = []
      this.listDdls(this.course_uuid, this.page, 10, (l) => {
        this.ddls.push.apply(this.ddls, l)
        this.page += 1
      })
    }
  },
  created() {
    this.course_uuid = getCurrentInstance().router.params['course_uuid']
    this.course_title = getCurrentInstance().router.params['course_title']
    console.log(this.course_uuid)
    this.listDdls(this.course_uuid, this.page, 10, (l) => {
      this.ddls.push.apply(this.ddls, l)
      this.page += 1
    })
  }
}

</script>

<style>
.page {
  background: #f9f9f9;
}

.course-ddl-card {
  margin-top: 6px;
  margin-bottom: 6px;
  align-items: center;
  margin-left: 2vw;
  width: 96vw;
  height: 80px;
  border-radius: 10px;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.course-ddl-site-icon {
  width: 30px;
  height: 30px;
  margin-right: 20px;
}

.add-ddl-card {
  align-items: center;
  margin-left: 2vw;
  margin-top: 0;
  margin-bottom: 8px;
  height: 50px;
  width: 96%;
  border-radius: 10px;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.nut-cell__title {
  width: 64vw;
  flex: inherit;
  line-height: 20px;
}

.nut-cell-group__title {
  margin-top: 15px;
}

.nut-cell-group {
  height: 30px;
}
</style>
