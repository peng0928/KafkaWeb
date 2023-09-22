<template>
  <a-layout style="min-height: 100vh">
    <a-layout-sider collapsible>
      <div style="padding-top: 6%">
        <div @click="handleMouseOut('/')">
          <CrownTwoTone
            :style="{ fontSize: '23px' }"
            :two-tone-color="'#FFD700'"
          />
        </div>
      </div>
      <a-menu theme="dark" mode="inline" style="padding-top: 10%">
        <a-menu-item key="2">
          <div class="icon-wrapper" @click="TORoute('/consumer')">
            <ApartmentOutlined />
            <span>集群</span>
          </div>
        </a-menu-item>
        <a-menu-item key="3">
          <!-- <div class="icon-wrapper" @click="TORoute('/topic')">
            <GoldTwoTone />
            <span>Topic</span>
          </div> -->
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <!-- <a-layout-header style="background: #fff; padding: 0"></a-layout-header> -->
      <a-layout-header style="background: #fff; padding: 0">
        <a-row>
          <a-col :span="8">
            <a href="#/"><span class="km-header-logo">Kafka Web</span></a>
          </a-col>
          <a-col :span="8" :offset="8">
            <!-- <svg-icon type="mdi" :path="icons.mdiGithub" class="githubSvg"></svg-icon> -->
            <div class="kafka-icon">
              <a href="https://github.com/peng0928/KafkaWeb">
                <GithubOutlined :style="{ fontSize: '25px', color: '#08c' }" />
              </a>
            </div>
          </a-col>
        </a-row>
      </a-layout-header>

      <a-layout-content style="margin: 0 16px">
        <a-page-header
          style="border: 1px solid rgb(235, 237, 240); margin: 16px 0"
          :title="pageTitle"
          :sub-title="subTitle"
          @back="goBack"
        />
        <div
          :style="{
            padding: '24px',
            background: '#fff',
            minHeight: '360px',
            width: '100%',
          }"
        >
          <router-view></router-view>
        </div>
      </a-layout-content>
      <a-layout-footer style="text-align: center"> @Penr </a-layout-footer>
    </a-layout>
  </a-layout>
</template>

<script>
import router from "@/router"; // 导入 Vue Router 实例
import {
  ApartmentOutlined,
  GithubOutlined,
  CrownTwoTone,
  // GoldTwoTone,
} from "@ant-design/icons-vue";

export default {
  components: {
    ApartmentOutlined,
    GithubOutlined,
    CrownTwoTone,
    // GoldTwoTone,
  },
  name: "App",
  data() {
    return {};
  },
  methods: {
    goBack() {
      // 返回上一页
      this.$router.go(-1);
    },
    TORoute(e) {
      router.push(e); // 跳转到目标页面的路径
    },

    handleMouseOut(e) {
      this.TORoute(e);
    },
  },
  computed: {
    pageTitle() {
      return this.$route.meta.title;
    },
    subTitle() {
      return this.$route.meta.subtitle;
    },
  },
};
</script>

<style>
.my-divider {
  margin: 6px 0;
}

.icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-wrapper svg-icon {
  width: 1em;
  height: 1em;
  margin-right: 0.5em;
}

.km-header-logo {
  font-size: 18px;
  font-weight: 500;
  cursor: pointer;
  color: black;
}

menu .logo {
  margin: 16px;
}

.githubSvg:hover path {
  fill: black;
}
.kafka-icon:hover path {
  fill: green;
}
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: -8px -8px auto;
}
</style>
