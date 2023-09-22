<template>
  <a-row style="padding-bottom: 1%">
    <div>
      <a-col
        ><a-tag color="red"> {{ topic }}</a-tag></a-col
      >
    </div>
    <a-col :span="1">
      <a-tag color="red"> topic {{ totalCount }}</a-tag></a-col
    >
    <a-col :span="5" :push="12">
      <a-input-search
        v-model:value="searchValue"
        placeholder="搜索名称"
        style="width: 200px"
        @search="onSearch"
      />
    </a-col>
    <a-col :span="1" :push="12">
      <a-space>
        <a-button type="primary" @click="Reload">
          <ReloadOutlined />
        </a-button>
      </a-space>
    </a-col>
  </a-row>

  <div>
    <a-table :data-source="data">
      <a-table-column title="序号" data-index="index" fixed="left">
        <template v-slot="{ text }">
          <a-tag type="default" :title="text">{{ text }}</a-tag>
        </template>
      </a-table-column>
      <a-table-column key="lastName" title="名称" data-index="topic">
        <template v-slot="{ text }">
          <a-tag color="green" :title="text">{{ text }}</a-tag>
        </template>
      </a-table-column>
      <a-table-column key="tags" title="操作" fixed="right">
        <template #customRender="{ record }">
          <a-tag color="red" :title="text" @click="handleClick(record.topic)">
            查看
          </a-tag>
        </template>
      </a-table-column>
    </a-table>
  </div>
</template>
<script>
import { ReloadOutlined } from "@ant-design/icons-vue";
import axios from "axios";
import { useRoute } from "vue-router";
import { message } from "ant-design-vue";

export default {
  components: {
    ReloadOutlined,
  },
  data() {
    return {
      data: [],
      searchValue: "",
      route: useRoute().params.itemName,
      topic: "",
      services: "",
    };
  },
  methods: {
    Reload() {
      this.GeTtopicList();
      this.searchValue = "";
    },
    GeTtopicList() {
      axios
        .post("/api/topic/list", { servers: this.services }) // 发送GET请求到后端API
        .then((response) => {
          this.data = response.data.data;
          const msg = response.data.msg;
          this.addIndexToData();
          message.info(msg);
        })
        .catch((error) => {
          // 处理请求错误
          console.log(error.response.data.msg);
        });
    },
    addIndexToData() {
      this.data.forEach((item, index) => {
        item.index = index + 1;
      });
    },
    onSearch() {
      if (this.searchValue.trim() === "") {
        // 如果搜索关键字为空，则显示全部数据
        this.GeTtopicList();
      } else {
        // 使用筛选条件过滤数据
        const regex = new RegExp(this.searchValue, "i");
        this.data = this.data.filter((item) => {
          return regex.test(item.topic);
        });
        this.addIndexToData(); // 更新索引
      }
    },
    handleClick(topic) {
      // 处理点击事件，使用 Vue Router 进行路由导航
      this.$router.push(
        "/topic/data/" + encodeURIComponent(topic + "|||" + this.services)
      );
    },
  },
  created() {
    this.topic = decodeURIComponent(this.route).split("|||")[0];
    this.services = decodeURIComponent(this.route).split("|||")[1];
    console.log(this.topic);
    this.GeTtopicList();
  },
  computed: {
    totalCount() {
      return this.data.length;
    },
  },
};
</script>

<style>
.right-align {
  text-align: right;
}
</style>
