<template>
  <nut-cell
    v-for="ddl in ddls"
    :key="ddl"
    :title=ddl.title
    :sub-title=formatTime(ddl.ddl_time)
    @click="ddlCardClick">


    <template #icon>
      <img
        class="home-site-icon"
        :src="getPlatformInfo(ddl.platform_uuid).icon"
      />
    </template>

    <template #link>
      <nut-button type="info" plain :disabled="ddl.added">
        添加
      </nut-button>
    </template>


  </nut-cell>
</template>

<script>

import Taro, {getCurrentInstance} from "@tarojs/taro";
import {formatTime, getPlatformInfo} from "../../util/ui";
import {request} from "../../util/request";
import {DDLData} from "../../types/DDLData";

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
      ddls: []
    }
  },
  methods: {},
  created() {
    let course_uuid = getCurrentInstance().router.params['course_uuid']
    console.log(course_uuid)
    const r = request({
      method: "POST",
      path: "/community/ddl/list",
      data: {
        page: 1,
        size: 10,
        course_uuid: course_uuid
      }
    })

    r.then((res) => {
      this.ddls = res.data.data.source_ddls
    }).catch((reason) => {
      console.log(reason)
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
