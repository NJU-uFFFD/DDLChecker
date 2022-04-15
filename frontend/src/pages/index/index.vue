<template>
  <view>
    <AtTabBar
      :tabList="tabList1"
      @click="handleClick"
      :current="current1"
    />
    <AtTabBar
      fixed
      :tabList="[
    { title: '待办事项', iconType: 'bullet-list', text: 'new' },
    { title: '拍照', iconType: 'camera' },
    { title: '文件夹', iconType: 'folder', text: '100', max: 99 }
  ]"
      @click="handleClick"
      :current="current"
    />
  </view>
</template>

<script>
export default {
  name: 'TabBarPage',
  data() {
    return {
      current1: 0,
      tabList1: [
        {title: '待办事项', text: 8},
        {title: '拍照'},
        {title: '通讯录', dot: true}
      ],
    }
  },
  methods: {
    onClick(value) {
      this.current1 = value
    }
  },
}
</script>
