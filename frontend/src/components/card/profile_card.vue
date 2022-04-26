<template>
  <nut-cell
    class="profile-card"
    :title=nickname
    sub-title="查看详情">
    <template v-slot:icon>
      <nut-avatar
        class="avatar"
        size="large"
        :icon="avatar_url"/>
    </template>
  </nut-cell>
</template>

<script>
export default {
  name: "profile_card",
  props: {
    nickname: String,
    avatar_url: String
  }
}
</script>

<style>
.profile-card {
  margin-top: 20px;
  margin-bottom: 0;
  align-items: center;
  border-radius: 0;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.avatar {
  margin-right: 20px;
}

</style>
