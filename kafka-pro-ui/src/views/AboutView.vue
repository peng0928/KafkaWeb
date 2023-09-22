<template>
  <a-row style="padding-bottom: 1%;">
    <a-col :span="1">集群</a-col>
    <a-col :span="5" :push="12">
      <a-input-search v-model:value="value" placeholder="input search text" style="width: 200px" @search="onSearch" />
    </a-col>
    <a-col :span="1" :push="12">
      <a-space>
        <a-button type="primary">
          <ReloadOutlined />
        </a-button>
      </a-space>
    </a-col>
    <a-col :span="1" :push="12">
      <a-space>
        <a-button type="primary">
          <PlusOutlined />
        </a-button>
      </a-space>
    </a-col>
  </a-row>

  <div>
    <a-table :data-source="data">
      <a-table-column key="lastName" title="序号" data-index="firstName" />
      <a-table-column key="lastName" title="名称" data-index="lastName" />
      <a-table-column key="age" title="集群地址" data-index="age" />
      <a-table-column key="address" title="Topic" data-index="address" />
      <a-table-column key="tags" title="Broker" data-index="tags">
        <template #default="{ text: tags }">
          <span>
            <a-tag v-for="tag in tags" :key="tag" color="blue">{{ tag }}</a-tag>
          </span>
        </template>
      </a-table-column>
      <a-table-column key="action" title="Action">
        <template #default="{ record }">
          <span>
            <a>Action 一 {{ record.firstName }}</a>
            <a-divider type="vertical" />
            <a>Delete</a>
          </span>
        </template>
      </a-table-column>
    </a-table>
  </div>
</template>
<script>
import { ReloadOutlined, PlusOutlined } from '@ant-design/icons-vue';
export default {
  components: {
    ReloadOutlined, PlusOutlined
  },
  data() {
    return {
      data: [
        {
          key: '1',
          firstName: 'John',
          lastName: 'Brown',
          age: 32,
          address: 'New York No. 1 Lake Park',
          tags: ['nice', 'developer'],
        },
        {
          key: '2',
          firstName: 'Jim',
          lastName: 'Green',
          age: 42,
          address: 'London No. 1 Lake Park',
          tags: ['loser'],
        },
        {
          key: '3',
          firstName: 'Joe',
          lastName: 'Black',
          age: 32,
          address: 'Sidney No. 1 Lake Park',
          tags: ['cool', 'teacher'],
        },
      ],
    }
  }
}
</script>

<style >
.right-align {
  text-align: right;
}
</style>