<template>

  <scroll-view
    :scroll-y="true"
    @scrolltolower="listLower"
    style="height: 96vh;">
    <nut-cell
      v-for="ddl in ddls"
      :key="ddl"
      :title=ddl.title
      :sub-title=formatTime(ddl.ddl_time)
    >
      <template #icon>
        <img
          class="home-site-icon"
          :src="getPlatformInfo(ddl.platform_uuid).icon"
        />
      </template>

      <template #link>
        <nut-button type="info" plain :disabled="ddl.added" @click="fetchDdl(ddl)">
          {{ ddl.added ? "已添加" : "添加" }}
        </nut-button>
      </template>

    </nut-cell>

    <nut-divider v-if="!more">没有更多 DDL 了捏</nut-divider>
  </scroll-view>

</template>

<script>

import Taro, {getCurrentInstance} from "@tarojs/taro";
import {formatTime, getPlatformInfo} from "../../util/ui";
import {request} from "../../util/request";

export default {
  name: "index",

  props: {
    course_data: Object
  },

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
      course_uuid: ""
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
    }
  },
  created() {
    this.course_uuid = getCurrentInstance().router.params['course_uuid']
    console.log(this.course_uuid)
    this.listDdls(this.course_uuid, this.page, 10, (l) => {
      this.ddls.push.apply(this.ddls, l)
      this.page += 1
    })
  }
}

</script>

<style>

.home-ddl-card {
  margin-top: 6px;
  margin-bottom: 6px;
  align-items: center;
  margin-left: 2vw;
  width: 96vw;
  height: 70px;
  border-radius: 10px;
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
