<template>
  <a-row style="padding-bottom: 3%">
    <div>
      <a-col>
        <a-tag color="red"> topic {{ totalCount }}</a-tag>
      </a-col>
    </div>
    <div>
      <a-col>
        <a-tag color="red"> {{ topic }}</a-tag>
      </a-col>
    </div>
    <div style="padding-left: 3%">
      <a-tag color="green"> 定时刷新</a-tag>
    </div>
    <div>
      <a-switch
        v-model:checked="checked3"
        checked-children="开"
        un-checked-children="关"
      />
    </div>
    <div style="padding-left: 3%">
      <a-col>
        <a-space>
          <a-button type="primary" @click="GeTtopicData">
            <ReloadOutlined />
          </a-button>
        </a-space>
      </a-col>
    </div>
    <div style="padding-left: 3%">
      <a-col>
        <a-input-search
          v-model:value="searchValue"
          placeholder="筛选value"
          style="width: 200px"
          @search="onSearch"
        />
      </a-col>
    </div>

    <div style="padding-left: 3%; padding-top: 0.3%">
      <a-tag color="red"> 数量</a-tag>
    </div>
    <div>
      <a-input-number
        v-model:value="topicNum"
        :min="10"
        :max="10000"
        :step="10"
      />
    </div>
    <div style="padding-left: 3%">
      <a-col>
        <a-space>
          <a-button type="primary" @click="GeTtask">
            <ClockCircleTwoTone />
          </a-button>
        </a-space>
      </a-col>
    </div>
  </a-row>
  <a-table
    :data-source="data"
    @change="handleTableChange"
    :pagination="paginationConfig"
    :size="small"
  >
    <a-table-column title="序号" fixed="left">
      <template v-slot="{ text, index }">
        <a-tag type="default" :title="text">{{ startIndex + index + 1 }}</a-tag>
      </template>
    </a-table-column>
    <a-table-column title="partition" data-index="partition" fixed="left">
      <template v-slot="{ text }">
        <a-tag color="green" :title="text">{{ text }}</a-tag>
      </template>
    </a-table-column>
    <a-table-column key="offset" title="offset" data-index="offset">
      <template v-slot="{ text }">
        <a-tag color="blue" :title="text">{{ text }}</a-tag>
      </template>
    </a-table-column>
    <a-table-column key="key" title="key" data-index="key">
      <template v-slot="{ text }">
        <a-tag color="red" :title="text">{{ text }}</a-tag>
      </template>
    </a-table-column>
    <a-table-column key="value" title="value" data-index="value">
      <template #customRender="{ record }">
        <a-tooltip :title="record.value" color="purple">
          <a-tag
            @click="handlein(record)"
            color="green"
            :style="{
              width: '30vw',
              overflow: 'hidden',
            }"
            :title="text"
            >{{ record.value }}
          </a-tag>
        </a-tooltip>
      </template>
    </a-table-column>
    <a-table-column
      key="timestamp"
      title="timestamp"
      data-index="timestamp"
      :sorter="customSorter"
    >
      <template v-slot="{ text }">
        <a-tag color="blue" :title="text">{{ text }}</a-tag>
      </template>
    </a-table-column>
  </a-table>
  <a-spin v-if="loading" size="large" />

  <!-- 模态框 -->
  <a-modal
    v-model:open="Modalopen"
    title="Value Data"
    width="80%"
    wrap-class-name="full-modal"
    @ok="handleout"
  >
    <div class="scrollable-div">
      <json-viewer :value="jsonData" copyable boxed sort></json-viewer>
      <div style="padding-bottom: 10%">
        <div class="splide">
          <a-spin v-if="loadingModel" size="large" class="spin" />
        </div>
      </div>
    </div>
  </a-modal>

  <!-- 左侧态框 -->

  <a-drawer
    title="任务列表"
    :placement="placement"
    :closable="false"
    :open="leftDrawer"
    @close="onClose"
    :width="450"
  >
    <a-list :data-source="taskdata">
      <template #renderItem="{ item, index }">
        <a-list-item>
          <a-tag>{{ index + 1 }}</a-tag>
          <a-tag color="green">时间: {{ item.datetime }}</a-tag>
          <a-tag color="pink">数量: {{ item.topic_num }}</a-tag>
          <a-tag color="orange">进行中</a-tag>
        </a-list-item>
      </template>
    </a-list>
  </a-drawer>
</template>

<script>
import axios from "axios";
import { useRoute } from "vue-router";
import { ReloadOutlined, ClockCircleTwoTone } from "@ant-design/icons-vue";

export default {
  components: {
    ReloadOutlined,
    ClockCircleTwoTone,
  },
  data() {
    return {
      subTitle: "",
      placement: "left",
      leftDrawer: false,
      jsonproData: { name: "John", age: 30, city: "New York" },
      Modalopen: false,
      startIndex: 0,
      jsonData: [],
      topicNum: 10,
      data: [],
      sortOrder: null,
      sortField: null,
      loading: false,
      loadingModel: false,
      checked3: false,
      paginationConfig: {
        // 分页配置
        showSizeChanger: true, // 显示数据条数选择器
        pageSizeOptions: ["10", "20", "50"], // 数据条数选择器选项
        pageSize: 10, // 每页展示的条数
        current: 1, // 当前页码
        total: 0, // 总条数
      },
      route: useRoute().params.itemName,
      sortedData: [], // 排序后的数组
      topic: "",
      servers: "",
      searchValue: "",
      taskdata: [],
    };
  },
  methods: {
    updateStartIndex() {
      this.startIndex =
        (this.paginationConfig.current - 1) * this.paginationConfig.pageSize;
    },
    isJSON(str) {
      const initText = str;
      if (typeof str == "string") {
        try {
          var obj = JSON.parse(str);
          if (typeof obj == "object" && obj) {
            this.jsonData = obj;
            return true;
          } else {
            this.jsonData = {
              文本: initText,
            };
            return false;
          }
        } catch (e) {
          try {
            str = str.replace(/\\"/g, '"');
            str = str.replace(/"{/g, "{");
            str = str.replace(/}"/g, "}");
            str = str.replace(/\\/g, "");
            const obj = JSON.parse(str);
            if (typeof obj == "object" && obj) {
              this.jsonData = obj;
              return true;
            } else {
              this.jsonData = {
                文本: initText,
              };
              return false;
            }
          } catch {
            console.log("error：" + str + "!!!" + e);
            this.jsonData = {
              文本: initText,
            };
            return false;
          }
        }
      } else {
        const initText = String(str);
        this.jsonData = {
          文本: initText,
        };
      }
    },
    handlein(recode) {
      this.jsonData = [];
      this.loadingModel = true;
      this.Modalopen = true;

      axios
        .post("/api/topic/data/model", {
          id: recode.id,
        })
        .then((response) => {
          const value = response.data.data.value;
          this.isJSON(value);
          this.loadingModel = false;
        });
    },
    handleout() {
      this.Modalopen = false;
    },

    GeTtopicData() {
      axios.post("/api/topic/data/task", {
        topic: this.topic,
        servers: this.servers,
        topic_num: this.topicNum,
      });
      this.TopicData();
    },
    topicTask() {
      axios.post("/api/topic/data/task", {
        topic: this.topic,
        servers: this.servers,
        topic_num: this.topicNum,
      });
    },
    TopicData() {
      this.loading = true; // 开始加载，显示 loading 效果
      axios
        .post("/api/topic/data", {
          topic: this.topic,
          servers: this.servers,
          topic_num: this.topicNum,
        })
        .then((response) => {
          this.data = response.data.data;
          this.paginationConfig.total = this.data.length;
          this.addIndexToData();
          this.loading = false; // 数据加载完成，隐藏 loading 效果
        })
        .catch((error) => {
          console.log(error.response.data.msg);
          this.loading = false; // 数据加载出错，隐藏 loading 效果
        });
    },
    handleTableChange(pagination, filters, sorter) {
      this.paginationConfig = pagination;

      if (sorter.order !== this.sortOrder || sorter.field !== this.sortField) {
        this.sortOrder = sorter.order;
        this.sortField = sorter.field;
        // 执行排序逻辑

        this.sortData();
      }
      this.addIndexToData();
    },
    sorterFunc(a, b) {
      const field = this.sortField;
      const order = this.sortOrder;

      const aValue = a[field];
      const bValue = b[field];

      if (typeof aValue === "string") {
        return order === "ascend"
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue);
      } else {
        return order === "ascend" ? aValue - bValue : bValue - aValue;
      }
    },
    customSorter(a, b) {
      if (this.sortOrder === "ascend") {
        this.sortOrder = "descend";
        return new Date(a.timestamp) - new Date(b.timestamp);
      } else {
        this.sortOrder = "ascend";
        return new Date(a.timestamp) - new Date(b.timestamp);
      }
    },
    sortData() {
      const field = this.sortField;
      const order = this.sortOrder;

      if (field && order) {
        this.data = this.data.sort(this.sorterFunc);
        this.addIndexToData();
      }
      this.addIndexToData();
    },
    startTimer() {
      this.timer = setInterval(() => {
        // 定时器逻辑
        if (this.searchValue) {
          this.onSearch();
        } else {
          this.GeTtopicData();
        }
      }, 5000);
    },
    stopTimer() {
      clearInterval(this.timer); // 关闭定时器
    },
    addIndexToData() {
      this.data.forEach((item, index) => {
        item.index = index + 1;
        console.log(item, index);
      });
    },
    onSearch() {
      this.loading = true; // 开始加载，显示 loading 效果
      if (this.searchValue.trim() === "") {
        this.GeTtopicData();
      } else {
        this.topicTask();
        axios
          .post("/api/topic/data/search", {
            topic: this.topic,
            servers: this.servers,
            searchKey: this.searchValue,
          })
          .then((response) => {
            this.data = response.data.data;
            this.paginationConfig.total = this.data.length;
            this.addIndexToData();
            this.loading = false; // 数据加载完成，隐藏 loading 效果
          })
          .catch((error) => {
            console.log(error.response.data.msg);
            this.loading = false; // 数据加载出错，隐藏 loading 效果
          });
      }
    },
    stopTask() {
      // 关闭定时器
      clearInterval(this.tasktimer);
      this.leftDrawer = false;
    },
    startTask() {
      this.leftDrawer = true;
      this.tasktimer = setInterval(() => {
        // 定时器逻辑
        axios
          .post("/api/topic/task", {
            topic: this.topic,
            servers: this.servers,
          })
          .then((response) => {
            this.taskdata = response.data.data;
          });
      }, 1000);
    },
    GeTtask() {
      this.startTask();
    },
    onClose() {
      this.stopTask();
    },
  },
  watch: {
    checked3(value) {
      if (value) {
        // 当开关打开时，启动定时器
        this.startTimer();
      } else {
        // 当开关关闭时，关闭定时器
        this.stopTimer();
      }
    },
    "paginationConfig.current"() {
      this.updateStartIndex();
    },
  },
  created() {
    const params = decodeURIComponent(this.route).split("|||");
    console.log(params);
    this.topic = params[0];
    this.servers = params[1];
    this.GeTtopicData();
  },
  computed: {
    totalCount() {
      return this.data.length;
    },
  },
  beforeUnmount() {
    // 在页面退出之前关闭定时器
    clearInterval(this.timer);
    clearInterval(this.tasktimer);
  },
  onSearch() {
    console.log(this.searchValue);
    if (this.searchValue.trim() === "") {
      // 如果搜索关键字为空，则显示全部数据
      this.GeTtopicList();
    } else {
      // 使用筛选条件过滤数据
      const regex = new RegExp(this.searchValue, "i");
      this.data = this.data.filter((item) => {
        console.log(item);
        return regex.test(item.value);
      });
      this.addIndexToData(); // 更新索引
    }
  },
};
</script>
<style>
.column-content {
  max-width: 40vw;

  /* 设置最大宽度 */
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsi50;
}

.scrollable-div {
  overflow-y: auto;
  height: 60vh; /* 设置高度为适当的值 */
}

.splide {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
