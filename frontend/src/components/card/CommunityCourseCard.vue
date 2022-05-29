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
  emits: ['onClick', 'onCompleteStatusChange'],
  setup({course}, {emit}) {
    if (course === undefined) return;
    const courseCardClick = () => {
      emit("onClick", course)
    };

    return {
      courseCardClick,
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
  box-shadow: 0 3px 14px 0 rgba(237, 238, 241, 1);
}

.community-site-icon {
  width: 36px;
  height: 36px;
  margin-right: 16px;
}

</style>
