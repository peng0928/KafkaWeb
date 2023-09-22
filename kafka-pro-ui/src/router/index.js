import {
  createRouter,
  createWebHistory
} from "vue-router";
import HomeView from "../views/HomeView.vue";
import AboutView from "../views/AboutView.vue";
import TopictView from "../views/topic/TopicView";
import TopicContent from "../views/topic/TopicContent";
import ConsumerView from "../views/topic/ConsumerView";
const routes = [{
    path: "/",
    name: "home",
    component: HomeView,
    meta: {
      title: "首页",
    },
  },
  {
    path: "/about",
    name: "about",
    component: AboutView,
    meta: {
      title: "aobut",
      subtitle: "测试",
    },
  }, {
    path: "/consumer",
    name: "Consumer",
    component: ConsumerView,
    meta: {
      title: "集群",
      subtitle: "",
    },
  }, {
    path: "/topic/:itemName",
    name: "topic",
    component: TopictView,
    meta: {
      title: "topic",
      subtitle: "",
    },
  },
  {
    path: '/topic/data/:itemName',
    name: 'TopicData',
    meta: {
      breadcrumb: '',
      title: 'Topic',
    },
    component: TopicContent
  },

];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});
router.afterEach((to) => {
  document.title = to.meta.title;
});
export default router;