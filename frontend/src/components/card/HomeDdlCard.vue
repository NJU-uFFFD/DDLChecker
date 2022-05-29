<template>
  <nut-cell
    class="home-ddl-card"
    :style="{color:(ddlData.ddl_time<now.valueOf()&&!ddlData.is_completed)?'#cd0f0f':(ddlData.tag==='紧急'&&!ddlData.is_completed)?'#ffb12a':'#676767'}"
    :title=ddlData.title
    :sub-title=ddlTime
    @click="ddlCardClick">
    <template #icon>
      <img
        class="home-site-icon"
        :src="getPlatformInfo(ddlData.platform_uuid).icon"
      />
    </template>
    <template #link>
      <nut-icon
        style="position: absolute;right: 7vw"
        name="check-normal"
        size="28"
      />
      <nut-icon
        style="position: absolute;right:2vw;padding-top: 4vw;padding-bottom: 4vw;padding-left: 4vw;padding-right: 4vw;"
        :name="ddlData.is_completed?'Check':''"
        color="#2c68ff"
        size="32"
        @click.stop="completeDdl"/>
    </template>
  </nut-cell>

</template>

<script lang="ts">
import {defineComponent, ref} from 'vue'
import {DDLData} from "../../types/DDLData";
import {formatTime, getPlatformInfo} from "../../util/ui"

export default defineComponent({
  name: "HomeDdlCard",
  props: {
    ddlData: Object as () => DDLData
  },
  emits: ['onClick', 'onCompleteStatusChange'],
  setup({ddlData}, {emit}) {
    if (ddlData === undefined) return;

    const now = new Date()

    const ddlCardClick = () => {
      emit("onClick", ddlData)
    };

    const ddlTime = formatTime(ddlData.ddl_time)

    function completeDdl() {
      if (ddlData === undefined) return;
      ddlData.is_completed = !ddlData.is_completed
      emit("onCompleteStatusChange", ddlData)
    }

    return {
      now,
      ddlCardClick,
      ddlTime,
      getPlatformInfo,
      completeDdl
    };
  }
})
</script>

<style>

.home-ddl-card {
  margin-top: 10px;
  margin-bottom: 6px;
  align-items: center;
  margin-left: 2vw;
  color: #676767;
  width: 96vw;
  height: 70px;
  border-radius: 10px;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.home-site-icon {
  width: 30px;
  height: 30px;
  margin-right: 20px;
}

/*以下样式对于有副标题的 Cell 没有作用*/
.nut-cell__title {
  width: 64vw;
  flex: inherit;
}
</style>
