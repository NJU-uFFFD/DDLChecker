<template>
  <nut-cell
    class="profile-setting-card"
    :title="settingTitle">
    <template #link>
      <nut-switch disable/>
    </template>
  </nut-cell>
</template>

<script lang="ts">
import {Toast} from '@nutui/nutui-taro';
import {AccountData} from "../../types/AccountData";
import {defineComponent} from "vue";
import {getPlatformInfo} from "../../util/ui";


export default defineComponent({
  name: "ProfileSettingCard",
  props: {
    settingTitle: String
  }
})
</script>

<style>
.profile-setting-card {
  align-items: center;
  margin-left: 10px;
  margin-top: 0;
  margin-bottom: 8px;
  height: 50px;
  width: 95%;
  border-radius: 10px;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

</style>
