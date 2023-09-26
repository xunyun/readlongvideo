import Vue from 'vue';
import TDesign from 'tdesign-vue';
import App from './App.vue';  // 导入 App.vue

// 引入样式文件
import 'tdesign-vue/es/style/index.css';

// 使用 TDesign 插件
Vue.use(TDesign);

// 创建一个新的 Vue 实例
new Vue({
  render: h => h(App),
}).$mount('#app');  // 挂载到 id 为 "app" 的元素上