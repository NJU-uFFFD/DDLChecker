<template>
  <nut-cell
    class="history-ddl-card"
    :title=ddlData.title
    @click="ddlCardClick">
    <template #icon>
      <img
        class="history-site-icon"
        :src="getPlatformInfo(ddlData.platform_uuid).icon"
      />
    </template>
    <template #link>
      <nut-icon
        style="position: absolute;right: 7vw"
        name="check-normal"
        size="24"
      />
      <nut-icon
        style="position: absolute;right:2vw;padding-top: 4vw;padding-bottom: 4vw;padding-left: 4vw;padding-right: 4vw;"
        :name="ddlData.is_completed?'Check':''"
        color="#2c68ff"
        size="28"/>
    </template>
  </nut-cell>
</template>

<script lang="ts">
import {defineComponent, ref} from 'vue'
import {DDLData} from "../../types/DDLData";
import {getPlatformInfo} from "../../util/ui"

export default {
  name: "HistoryDdlCard",
  props: {
    ddlData: Object as () => DDLData
  },
  emits: ['onClick', 'onCompleteStatusChange'],
  setup({ddlData}, {emit}) {
    if (ddlData === undefined) return;

    const ddlCardClick = () => {
      emit("onClick", ddlData)
    };

    return {
      ddlCardClick,
      getPlatformInfo
    };
  }
}
</script>

<style>

.history-ddl-card {
  margin-top: 6px;
  margin-bottom: 6px;
  align-items: center;
  height: 50px;
  border-radius: 10px;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.history-site-icon {
  width: 20px;
  height: 20px;
  margin-top: 0;
  margin-left: 0;
  margin-right: 20px;
}

</style>
