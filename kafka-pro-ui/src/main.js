import {
  createApp
} from 'vue'
import App from './App.vue'
import router from './router'
import Antd from 'ant-design-vue';
import JsonViewer from "vue-json-viewer"

const app = createApp(App)

app.use(Antd)
app.use(router)
app.use(JsonViewer)

app.config.warnHandler = function () {
  // 禁用警告信息，不执行任何操作
}

app.mount('#app')