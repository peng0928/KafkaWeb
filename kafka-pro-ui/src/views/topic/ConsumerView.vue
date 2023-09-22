<template>
  <a-row style="padding-bottom: 2%">
    <a-col :span="1">
      <a-tag color="red"> 集群 {{ totalCount }}</a-tag>
    </a-col>
    <div style="padding-left: 50%">
      <a-col>
        <a-input-search
          v-model:value="searchValue"
          placeholder="input search text"
          style="width: 200px"
          @search="onSearch"
        />
      </a-col>
    </div>

    <div style="padding-left: 3%">
      <a-col>
        <a-space>
          <a-button type="primary" @click="GeTconData">
            <ReloadOutlined />
          </a-button>
        </a-space>
      </a-col>
    </div>

    <div style="padding-left: 1%">
      <a-col>
        <a-space>
          <a-button type="primary" @click="showModal">
            <PlusOutlined />
          </a-button>
        </a-space>
      </a-col>
    </div>
  </a-row>
  <div>
    <a-table :data-source="data">
      <a-table-column key="index" title="序号" data-index="index" />
      <a-table-column key="kafkaName" title="名称" data-index="kafkaName">
        <template v-slot="{ text }">
          <a-tag color="red" :title="text">{{ text }}</a-tag>
        </template>
      </a-table-column>
      <a-table-column key="kafkaServe" title="集群地址" data-index="kafkaServe">
        <template v-slot="{ text }">
          <a-tag color="yellow" :title="text">{{ text }}</a-tag>
        </template>
      </a-table-column>
      <a-table-column key="address" title="Topic" data-index="topic">
        <template v-slot="{ text }">
          <a-tag color="blue" :title="text">{{ text }}</a-tag>
        </template>
      </a-table-column>
      <a-table-column key="datetime" title="创建时间" data-index="datetime">
        <template v-slot="{ text }">
          <a-tag color="green" :title="text">{{ text }}</a-tag>
        </template>
      </a-table-column>
      <a-table-column key="action" title="Action" data-index="kafkaServe">
        <template v-slot="{ record }">
          <a-space>
            <a-button type="link" :title="record" @click="handleRoute(record)"
              >查看
            </a-button>
            <a-button type="link" @click="editClick(record)">编辑 </a-button>
            <a-button :title="record" @click="handleRowClick(record)"
              >测试
            </a-button>
            <a-button
              type="primary"
              danger
              ghost
              :title="record"
              @click="showDeleteModal(record)"
              >删除
            </a-button>
          </a-space>
        </template>
      </a-table-column>
    </a-table>
    <a-spin v-if="loading" size="large" />
  </div>

  <a-modal v-model:visible="modalVisible" title="创建集群" :footer="null">
    <a-form
      :model="formState"
      name="basic"
      :label-col="{ span: 6 }"
      :wrapper-col="{ span: 16 }"
      autocomplete="off"
      @finish="onFinish"
      @finish-failed="onFinishFailed"
    >
      <a-form-item
        label="名称"
        name="kafkaName"
        :rules="[{ required: true, message: 'Please input your kafkaName!' }]"
      >
        <a-input v-model:value="formState.kafkaName" />
      </a-form-item>

      <a-form-item
        label="集群地址"
        name="kafkaServe"
        :rules="[{ required: true, message: 'Please input your kafkaServe!' }]"
      >
        <a-input v-model:value="formState.kafkaServe" />
      </a-form-item>

      <a-form-item :wrapper-col="{ offset: 10, span: 16 }">
        <a-button type="primary" html-type="submit">Submit</a-button>
      </a-form-item>
    </a-form>
  </a-modal>

  <a-modal v-model:visible="modalVisibleEdit" title="编辑集群" :footer="null">
    <a-form
      :model="formState"
      name="basic"
      :label-col="{ span: 6 }"
      :wrapper-col="{ span: 16 }"
      autocomplete="off"
      @finish="onFinishEdit"
      @finish-failed="onFinishFailed"
    >
      <a-form-item
        label="名称"
        name="kafkaName"
        :rules="[{ required: true, message: 'Please input your kafkaName!' }]"
      >
        <a-input v-model:value="formState.kafkaName" />
      </a-form-item>

      <a-form-item
        label="集群地址"
        name="kafkaServe"
        :rules="[{ required: true, message: 'Please input your kafkaServe!' }]"
      >
        <a-input v-model:value="formState.kafkaServe" />
      </a-form-item>

      <a-form-item :wrapper-col="{ offset: 10, span: 16 }">
        <a-button type="primary" html-type="submit">Submit</a-button>
      </a-form-item>
    </a-form>
  </a-modal>

  <a-modal
    v-model:visible="deleteModalVisible"
    title="删除"
    @ok="confirmDelete"
  >
    <a-alert message="确认删除吗?" type="warning" show-icon />
  </a-modal>
</template>

<script>
import { ReloadOutlined, PlusOutlined } from "@ant-design/icons-vue";
import { reactive } from "vue";
import axios from "axios";
import { message } from "ant-design-vue";

export default {
  components: {
    ReloadOutlined,
    PlusOutlined,
  },
  data() {
    return {
      searchValue: "",
      deleteModalVisible: false,
      data: [],
      modalVisible: false,
      modalVisibleEdit: false,
      formState: reactive({
        kafkaServe: "",
        kafkaName: "",
      }),
      loading: false,
      kafkaNum: 0,
      editold: {},
      editnew: {},
      totalCount: 0,
      selectedRecord: "",
    };
  },
  methods: {
    onSearch() {
      if (this.searchValue.trim() === "") {
        // 如果搜索关键字为空，则显示全部数据
        this.GeTconData();
      } else {
        // 使用筛选条件过滤数据
        const regex = new RegExp(this.searchValue, "i");
        this.data = this.data.filter((item) => {
          return regex.test(item.kafkaName);
        });
        this.addIndexToData(); // 更新索引
      }
    },
    showDeleteModal(e) {
      this.selectedRecord = e;
      this.deleteModalVisible = true;
    },
    confirmDelete() {
      // 执行删除逻辑
      // ...
      this.delClick(this.selectedRecord);
    },
    showModal() {
      console.log(this.modalVisible);
      this.modalVisible = true;
    },
    onFinish(values) {
      this.loading = true; // 开始加载，显示 loading 效果
      console.log(values);
      axios
        .post("/api/consumer/add", {
          kafkaServe: values.kafkaServe,
          kafkaName: values.kafkaName,
        })
        .then((response) => {
          const msg = response.data.msg;
          const status = response.data.status;
          if (status) {
            this.loading = false; // 数据加载完成，隐藏 loading 效果
            this.modalVisible = false;
            values = {};
            this.GeTconData();
          }
          message.info(msg);
          this.loading = false; // 数据加载出错，隐藏 loading 效果
        })
        .catch((error) => {
          message.info(error.response.data.msg);
          this.loading = false; // 数据加载出错，隐藏 loading 效果
        });
    },
    onFinishEdit() {
      this.loading = true; // 开始加载，显示 loading 效果
      axios
        .post("/api/consumer/edit", {
          old: this.editold,
        })
        .then((response) => {
          const msg = response.data.msg;
          const status = response.data.status;
          if (status) {
            this.loading = false; // 数据加载完成，隐藏 loading 效果
            this.modalVisibleEdit = false;
            this.GeTconData();
          }
          message.info(msg);
          this.loading = false; // 数据加载出错，隐藏 loading 效果
        })
        .catch((error) => {
          message.info(error.response.data.msg);
          this.loading = false; // 数据加载出错，隐藏 loading 效果
        });
    },

    onFinishFailed(errorInfo) {
      console.log("Failed:", errorInfo);
    },
    addIndexToData() {
      this.data.forEach((item, index) => {
        item.index = index + 1;
      });
    },
    GeTconData() {
      this.loading = true; // 开始加载，显示 loading 效果
      this.data = [];
      axios
        .post("/api/consumer/data", {})
        .then((response) => {
          this.data = response.data.data;
          const msg = response.data.msg;
          this.addIndexToData();
          this.loading = false; // 数据加载完成，隐藏 loading 效果
          message.info(msg);
          this.totalCount = this.data.length;
        })
        .catch((error) => {
          message.info(error.response.data.msg);
          this.loading = false; // 数据加载出错，隐藏 loading 效果
        });
    },
    handleRowClick(record) {
      this.loading = true; // 开始加载，显示 loading 效果
      axios
        .post("/api/consumer/test", record)
        .then((response) => {
          const msg = response.data.msg;
          this.addIndexToData();
          this.loading = false; // 数据加载完成，隐藏 loading 效果
          message.info(msg);
          this.GeTconData();
        })
        .catch((error) => {
          message.info(error.response.data.msg);
          this.loading = false; // 数据加载出错，隐藏 loading 效果
        });
    },
    delClick(record) {
      this.loading = true; // 开始加载，显示 loading 效果
      axios
        .post("/api/consumer/del", record)
        .then((response) => {
          const msg = response.data.msg;
          this.addIndexToData();
          this.loading = false; // 数据加载完成，隐藏 loading 效果
          message.info(msg);
          this.GeTconData();
          this.deleteModalVisible = false;
        })
        .catch((error) => {
          message.info(error.response.data.msg);
          this.loading = false; // 数据加载出错，隐藏 loading 效果
          this.deleteModalVisible = false;
        });
    },

    handleRoute(record) {
      // 处理点击事件，使用 Vue Router 进行路由导航
      const params =
        String(record.kafkaName) + "|||" + String(record.kafkaServe);
      console.log(params);
      this.$router.push("/topic/" + encodeURIComponent(params));
    },
    editClick(record) {
      this.modalVisibleEdit = true;
      this.formState = record;
      this.editold = record;
    },
  },
  created() {
    this.GeTconData();
  },
};
</script>

<style>
.right-align {
  text-align: right;
}
</style>
