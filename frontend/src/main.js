import Vue from "vue";

import Vuetify from "vuetify";
import VueYouTubeEmbed from "vue-youtube-embed";

import App from "@/App";
import store from "@/store";
import router from "@/router";

import "vuetify/dist/vuetify.min.css";
import "./styles/main.scss";

Vue.use(Vuetify);
Vue.use(VueYouTubeEmbed);

new Vue({
  el: "#app",
  render: h => h(App),
  router,
  store
});
