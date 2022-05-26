<template>
  <nut-cell
    class="profile-profile-card"
    :title=nickname>
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
  name: "ProfileProfileCard",
  props: {
    nickname: String,
    avatarUrl: String
  }
})
</script>

<style>
.profile-profile-card {
  align-items: center;
  border-radius: 0;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.profile-avatar {
  margin-right: 20px;
}

</style>
