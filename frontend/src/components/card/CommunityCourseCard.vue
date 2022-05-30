<template>
  <nut-cell
    class="community-course-card"
    :title=course.course_name
    @click="courseCardClick">
    <template #icon>
      <img
        class="community-site-icon"
        :src="getPlatformInfo(course.platform_uuid).icon"
      />
    </template>
    <template #link>
      <nut-icon
        style="position: absolute;right: 7vw"
        name="follow"
        size="24"
      />
      <nut-icon
        style="position: absolute;right:2vw;padding-top: 4vw;padding-bottom: 4vw;padding-left: 4vw;padding-right: 4vw;"
        :name="course.subscribed?'heart-fill':''"
        color="#ff4e4e"
        size="32"
        @click.stop="subscribeCourse"/>
    </template>
  </nut-cell>

</template>

<script lang="ts">
import {defineComponent, ref} from 'vue'
import {getPlatformInfo} from "../../util/ui"

export default defineComponent({
  name: "HomeDdlCard",
  props: {
    course: Object
  },
  emits: ['onClick', 'onSubscribeStatusChange'],
  setup({course}, {emit}) {
    if (course === undefined) return;
    const courseCardClick = () => {
      emit("onClick", course)
    };

    const subscribeCourse = () => {
      if (course === undefined) return;
      course.subscribed = !course.subscribed
      emit("onSubscribeStatusChange", course)
    }

    return {
      courseCardClick,
      subscribeCourse,
      getPlatformInfo,
    };
  }
})
</script>

<style>

.community-course-card {
  margin-top: 10px;
  margin-bottom: 6px;
  align-items: center;
  margin-left: 2vw;
  width: 96vw;
  height: 90px;
  border-radius: 10px;
  font-size: 18px;
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.community-site-icon {
  width: 36px;
  height: 36px;
  margin-right: 16px;
}

.nut-cell__title {
  width: 64vw;
  flex: inherit;
}

</style>
