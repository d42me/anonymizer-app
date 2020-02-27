import Vue from 'vue';
import App from './App.vue';
import './registerServiceWorker';
import router from './router/router';
import store from './store/store';

Vue.config.productionTip = false;

import BootstrapVue from 'bootstrap-vue';
Vue.use(BootstrapVue);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
