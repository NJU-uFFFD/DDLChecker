<template>
  <nut-cell-group title="DDL">
    <nut-cell
      class="ddl-card"
      title="第一个ddl"
      sub-title="ddl时间"
      desc="查看详情">
      <template v-slot:icon>
        <img
          class="site-icon"
          src="../../assets/images/mooc.png"
        />
      </template>
    </nut-cell>
  </nut-cell-group>
</template>

<script>
import {ref} from 'vue';
import {Toast} from '@nutui/nutui-taro';

export default {
  name: "ddl_card",
  setup() {
    const switchChecked = ref(true);
    const testClick = (event) => {
      Toast.text('点击事件');
    };
    return {
      testClick,
      switchChecked
    };
  }
}
</script>

<style>
.ddl-card {
}

.site-icon {
  width: 40px;
  height: 40px;
}

</style>
