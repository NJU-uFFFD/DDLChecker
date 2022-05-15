<template>
  <view class="home">
    <HomeDdlListMenu
      @sortMode="sortDdlList"/>
    <view
      v-for="data in ddlList"
      :key="data">
      <HomeDdlCard :ddlData="data"/>
    </view>

    <!-- 手动添加 ddl 的弹出层 -->
    <view>
      <nut-overlay v-model:visible="state.showAdd" :close-on-click-overlay=false :z-index="200">
        <nut-form>

<!--          TODO: 表单内容检验-->

          <nut-form-item label="代办事项标题">
            <input v-model="state.addInfo.title" class="nut-input-text" placeholder="请输入代办事项标题" type="text"/>
          </nut-form-item>

          <nut-form-item label="Deadline">
            <input :value="state.addInfo.date.toLocaleString()" placeholder="选择时间" readonly="true" disabled="true"
                   @click="state.datePickerShow = true">

            <nut-datepicker catchMove
                            v-model="state.addInfo.date"
                            class="datepicker"
                            type="datetime"
                            title="Deadline 选择"
                            v-model:visible="state.datePickerShow"
                            @confirm="datePickerConfirm"
                            :min-date="getMinDate()"
                            :is-show-chinese="true"
                            :lock-scroll="true"
            ></nut-datepicker>
          </nut-form-item>

          <nut-form-item label="详细说明">
            <input v-model="state.addInfo.detail" class="nut-input-text" placeholder="请输入详细说明" type="text"/>
          </nut-form-item>

        </nut-form>

        <nut-button size="large" type="danger" @click="state.showAdd = false">关闭</nut-button>
        <nut-button size="large" type="success" @click="submitDdl()" :loading="state.ddlSubmitting">添加</nut-button>

      </nut-overlay>
    </view>

    <!-- Toast -->
    <nut-toast :msg="toastInfo.msg" v-model:visible="toastInfo.show" :type="toastInfo.type"
               @closed="toastInfo.onClosed" :cover="toastInfo.cover"/>

    <!-- 手动添加 ddl 的按钮 -->
    <nut-button type="primary" id="add_button" @click="addDdl">+</nut-button>
  </view>
</template>

<script lang="ts">
import {reactive, toRefs} from 'vue';
import HomeDdlCard from "../../components/card/HomeDdlCard.vue";
import HomeDdlListMenu from "../../components/menu/HomeDdlListMenu.vue";
import {DDLData} from "../../types/DDLData";
import {request} from "../../util/request"
import Taro from "@tarojs/taro";

export default {
  name: 'home',
  components: {
    HomeDdlCard,
    HomeDdlListMenu
  },
  setup() {
    const ddls = reactive<{ ddlList: DDLData [] }>({
      ddlList:
        [{
          id: 1,
          title: "第一个DDL",
          ddl_time: new Date(1656454270035),
          from: "/assets/images/jxlf.png",
          content: "",
          tag: ""
        },
          {
            id: 2,
            title: "第二个DDL",
            ddl_time: new Date(1655453250035),
            from: "/assets/images/spoc.png",
            content: "",
            tag: ""
          },
          {
            id: 3,
            title: "第三个DDL",
            ddl_time: new Date(1656453270035),
            from: "/assets/images/mooc.png",
            content: "",
            tag: ""
          },
          {
            id: 6,
            title: "第四个DDL",
            ddl_time: new Date(1656452440035),
            from: "/assets/images/jxlf.png",
            content: "",
            tag: ""
          },
          {
            id: 5,
            title: "第五个DDL",
            ddl_time: new Date(1656456270035),
            from: "/assets/images/spoc.png",
            content: "",
            tag: ""
          },
          {
            id: 4,
            title: "第六个DDL",
            ddl_time: new Date(1656463270435),
            from: "/assets/images/mooc.png",
            content: "",
            tag: ""
          },
          {
            id: 7,
            title: "第七个DDL",
            ddl_time: new Date(1652323272435),
            from: "/assets/images/jxlf.png",
            content: "",
            tag: ""
          },
          {
            id: 8,
            title: "第八个DDL",
            ddl_time: new Date(1656453270235),
            from: "/assets/images/spoc.png",
            content: "",
            tag: ""
          },
          {
            id: 9,
            title: "第九个DDL",
            ddl_time: new Date(1656434458035),
            from: "/assets/images/mooc.png",
            content: "",
            tag: ""
          },]
          .sort((o1, o2) => o1.ddl_time.valueOf() - o2.ddl_time.valueOf())
      //初始以由近至远排序
    })

    let state = reactive({
      "showAdd": false,
      "datePickerShow": false,
      "ddlSubmitting": false,
      "showToast": false,
      "toastMessage": "",
      "addInfo": {
        "title": "",
        "date": new Date(),
        "detail": ""
      }
    })

    let toastInfo = reactive({
      msg: 'toast',
      type: 'text',
      show: false,
      cover: false,
      title: '',
      bottom: '',
      center: true,
    })

    function sortDdlList(mode: string) {
      ddls.ddlList = ddls.ddlList.sort((o1, o2) => {
        switch (mode) {
          case "a":
            return o1.ddl_time.valueOf() - o2.ddl_time.valueOf()
          case "b":
            return o2.ddl_time.valueOf() - o1.ddl_time.valueOf()
          case "c":
            return o1.id - o2.id
          default:
            return o2.id - o1.id
        }
      })
    }

    function addDdl() {
      state.addInfo = {
        "title": "",
        "date": new Date(),
        "detail": ""
      }
      state.ddlSubmitting = false
      state.showAdd = true
    }

    function datePickerConfirm({selectedValue}) {
      const date = selectedValue.slice(0, 3).join('-');
      const time = selectedValue.slice(3).join(':');
      state.addInfo.date = new Date(date + ' ' + time);
    }

    const openToast = (type: string, msg: string, cover: boolean = false, title: string = "", bottom: string = "", center: boolean = true) => {
      toastInfo.show = true
      toastInfo.msg = msg
      toastInfo.type = type
      toastInfo.cover = cover
      toastInfo.title = title
      toastInfo.bottom = bottom
      toastInfo.center = center
    }

    function submitDdl() {
      state.ddlSubmitting = true
      const r = request({
        "method": "POST",
        "path": "/ddl/add",
        "data": {
          "title": state.addInfo.title,
          "ddl_time": state.addInfo.date.getTime(),
          "content": state.addInfo.detail
        }
      })

      r.then((res) => {
        state.showAdd = false

        if (res.statusCode == 200 && res.data.code == 0) {
          openToast('success', "添加成功!")
        } else {
          throw JSON.stringify(res)
        }
      }).catch((reason) => {
        Taro.showModal({
          title: '错误',
          content: '添加代办出错: ' + JSON.stringify(reason),
          showCancel: false
        })
      })
    }

    // function fetchDdls() {
    //   const r = request({
    //     path: "/ddl/list",
    //     method: "POST",
    //     data: {}
    //   })
    //   console.log(r)
    //
    //   r.then((res) => {
    //     console.log(res.data.data.ddl_list)
    //   })
    // }
    //
    // fetchDdls()

    const getMinDate = (() => {
      let now = new Date()
      return new Date(now.setDate(now.getDate() - 30))
    })

    return {
      ...toRefs(ddls),
      sortDdlList,
      addDdl,
      datePickerConfirm,
      getMinDate,
      submitDdl,
      state,
      toastInfo
    }
  }
}
</script>

<style>
.home {
  background: #f9f9f9;
}

#add_button {
  position: fixed;
  right: 30px;
  bottom: 30px;
}

/* bug fix for datepicker */
.nut-picker-item {
  display: none;
}
</style>
