import { createApp } from 'vue'
window.axios = require('axios');
import VueAxios from 'vue-axios'
import App from './App.vue'
import router from './router'
import ECharts from 'vue-echarts'
import { use } from "echarts/core"

import {
    CanvasRenderer
  } from 'echarts/renderers'
  import {
    BarChart
  } from 'echarts/charts'
  import {
    GridComponent,
    TooltipComponent
  } from 'echarts/components'
  
  use([
    CanvasRenderer,
    BarChart,
    GridComponent,
    TooltipComponent
  ])
const app = createApp(App)
app.component('v-chart', ECharts)
app.use(router,VueAxios)
app.mount('#app')