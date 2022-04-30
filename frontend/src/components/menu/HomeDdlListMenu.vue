<template>
  <nut-menu>
    <nut-menu-item
      v-model="value1"
      :options="options1"/>
    <nut-menu-item
      v-model="value2"
      @change="changeSort"
      :options="options2"/>
  </nut-menu>
</template>

<script>
import {reactive, toRefs, defineComponent} from 'vue';

export default defineComponent({
  name: "HomeDdlListMenu",
  setup(props, {emit}) {
    const state = reactive({
      options1: [
        {text: '全部DDL', value: 0},
        {text: '紧急DDL', value: 1},
        {text: '宽松DDL', value: 2}
      ],
      options2: [
        {text: '由近至远', value: "a"},
        {text: '由远至近', value: "b"},
        {text: '按ID排序', value: "c"},
        {text: '工作量排序', value: "d"},
      ],
      value1: 0,
      value2: "a"
    });

    //这个给父组件传值的函数真的太坑了, debug了好久
    const changeSort = val => {
      emit('sortMode', val)
    }

    return {
      ...toRefs(state),
      changeSort
    };
  }
})
</script>

<style>

</style>
