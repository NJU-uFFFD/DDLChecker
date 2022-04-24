<template>
  <nut-menu>
    <nut-menu-item
      v-model="state.value1"
      :options="state.options1"/>
    <nut-menu-item
      v-model="state.value2"
      @change="handleChange"
      :options="state.options2"/>
  </nut-menu>
</template>

<script>
import {reactive, ref} from 'vue';

export default {
  setup() {
    const state = reactive({
      options1: [
        {text: '全部DDL', value: 0},
        {text: '紧急DDL', value: 1},
        {text: '宽松DDL', value: 2}
      ],
      options2: [
        {text: '由近至远', value: 'a'},
        {text: '由远至近', value: 'b'},
        {text: '分类排序', value: 'c'},
        {text: '工作量排序', value: 'd'},
      ],
      value1: 0,
      value2: 'a'
    });

    const handleChange = val => {
      console.log('val', val);
    }

    return {
      state,
      handleChange
    };
  }
}
</script>

<style>

</style>
