<template>
  <nut-cell
    class="home-ddl-card"
    :title=ddlData.title
    :sub-title=ddlTime
    desc="查看详情"
    @click="ddlCardClick">
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
import {defineComponent, ref} from 'vue';
import {Dialog, Toast} from '@nutui/nutui-taro';
import {DDLData} from "../../types/DDLData";

export default defineComponent({
  name: "HomeDdlCard",
  props: {
    ddlData: Object as () => DDLData
  },
  emits: ['onClick'],
  setup({ddlData}, {emit}) {
    if (ddlData === undefined) return;
    const ddlCardClick = () => {
      emit("onClick", ddlData)
    };

    // const ddlTime = (new Intl.DateTimeFormat("zh-CN", {year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hour12: false}).format)(props.ddlData?.ddl_time);
    // 上述用法会出现上午12:40或者24:40这种离谱的情况,太难受啦!!

    const t = new Date(ddlData.ddl_time);
    const ddlTime = String(`${t.getFullYear()}年${t.getMonth() + 1}月${t.getDate()}日
    ${t.getHours() > 9 ? t.getHours() : "0" + t.getHours()}:
    ${t.getMinutes() > 9 ? t.getMinutes() : "0" + t.getMinutes()}`);

    return {
      ddlCardClick,
      ddlTime,
    };
  }
})
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
