<template>
  <nut-cell
    class="profile-profile-card"
    :title=nickname
    sub-title="查看详情">
    <template
      #icon>
      <nut-avatar
        class="profile-avatar"
        size="large"
        :icon="avatarUrl"/>
    </template>
  </nut-cell>
</template>

<script>
import {defineComponent} from "vue";

export default defineComponent({
  props: {
    nickname: String,
    avatarUrl: String
  }
})
</script>

<style>
.profile-profile-card {
  margin-top: 20px;
  margin-bottom: 0;
  align-items: center;
  border-radius: 0;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.profile-avatar {
  margin-right: 20px;
}

</style>
