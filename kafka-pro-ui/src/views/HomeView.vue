<template>
  <div>
    <a-row :gutter="16" type="flex" justify="center" class="title">
      <a-col :span="24">
        <h2>Kafka Web</h2>
      </a-col>
    </a-row>

    <a-row :gutter="16" type="flex" justify="center" class="features">
      <a-col :span="24">
        <a-list bordered>
          <a-list-item>实时监控和统计数据</a-list-item>
          <a-list-item>创建、管理和查看主题</a-list-item>
        </a-list>
      </a-col>
    </a-row>

    <a-row :gutter="16" type="flex" justify="center" class="cta">
      <a-col :span="24">
        <p>体验 Kafka Web 带来的便捷和效率！</p>
        <a-button type="primary" @click="TORoute('consumer')">开始</a-button>
      </a-col>
    </a-row>
  </div>
</template>
<script>
import router from "@/router"; // 导入 Vue Router 实例

export default {
  data() {
    return {};
  },
  methods: {
    TORoute(e) {
      router.push(e); // 跳转到目标页面的路径
    },
  },
};
</script>

<style>
.title {
  font-size: 20px;
  font-weight: 500;
  cursor: pointer;
  color: rgb(9, 33, 12);
  font-style: italic;
}
</style>
