import Vue from 'vue'
import App from './App.vue'
import './../node_modules/foundation-sites/dist/css/foundation.min.css';

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
