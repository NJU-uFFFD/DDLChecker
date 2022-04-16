<template>
  <cover-view class="tab-bar">
    <cover-view class="tab-bar-border"></cover-view>
    <cover-view v-for="(item, index) in list" :key="index" class="tab-bar-item" @tap="switchTab(index, item.pagePath)">
      <cover-image :src="selected === index ? item.selectedIconPath : item.iconPath"/>
      <cover-view :style="{ color: selected === index ? selectedColor : color }">{{ item.text }}</cover-view>
    </cover-view>
  </cover-view>
</template>

<script setup>
import Taro from '@tarojs/taro'
import {computed} from 'vue'
import {useStore} from 'vuex'
import './index.scss'

const store = useStore()
const selected = computed(() => store.getters.getSelected)

const color = '#000000'
const selectedColor = '#6190E8'
const list = [
  {
    pagePath: '/pages/index/index',
    selectedIconPath: '../images/home.png',
    iconPath: '../images/home-outline.png',
    text: '首页'
  },
  {
    pagePath: '/pages/favo/index',
    selectedIconPath: '../images/heart.png',
    iconPath: '../images/heart-outline.png',
    text: '喜欢'
  },
  {
    pagePath: '/pages/my/index',
    selectedIconPath: '../images/accessibility.png',
    iconPath: '../images/accessibility-outline.png',
    text: '个人'
  }
]

function switchTab(index, url) {
  setSelected(index)
  Taro.switchTab({url})
}

function setSelected(index) {
  store.dispatch('setSelected', index)
}
</script>

