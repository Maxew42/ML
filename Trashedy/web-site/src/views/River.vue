<template>
    <div class = "container3">
        <div class = "title"> {{"Résumé du cours d'eau : " + $route.params.id}} </div>
        <div class = "content_box">
            <div class = "stats_box">
                <v-chart class="chart" :option="option2"/>
                <v-chart class="chart" :option="option"/>
            </div>
            <div v-html="map" class = "map"></div>
        </div>
    </div>
</template>

<script>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart } from "echarts/charts";
import { LineChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { ref, defineComponent } from "vue";

use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  LineChart
]);

export default defineComponent({
  name: "HelloWorld",
  components: {
    VChart
  },
  provide: {
    [THEME_KEY]: "light"
  },
  data(){
      return {
        map: '',
        option2: {
    title: {
        text: "Nombre de déchets ajoutés cette semaine",
        left: "center"
      },
    xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
        type: 'value'
    },
    series: [{
        data: [150, 230, 224, 218, 135, 147, 260],
        type: 'line',
        smooth: true
        }]
        }
      }
    },
  async mounted(){
        const res = await axios.get('http://localhost:5000/get_river', { params: { river_name : this.$route.params.id} })
         this.map = res.data
  },
  setup() {
    const option = ref({
      title: {
        text: "Types de déchets",
        left: "center"
      },
      tooltip: {
        trigger: "item",
        formatter: "{a} <br/>{b} : {c} ({d}%)"
      },
      legend: {
        orient: "vertical",
        left: "left",
        data: ["Other","Plastic Bags","PET"]
      },
      series: [
        {
          name: "Type de déchet",
          type: "pie",
          radius: "55%",
          center: ["50%", "50%"],
          data: [
            { value: 105, name: "Other" },
            { value: 42, name: "Plastic Bags" },
            { value: 76, name: "PET" },
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: "rgba(0, 0, 0, 0.5)"
            }
          }
        }
      ]
    });

    return { option };
  }
});
</script>

<style scoped>
.container3{
    display : flex;
    flex-direction : column;
    margin : 3%;
    padding : 3%;
    margin-top : 10%;
    background-color: rgba(250, 235, 215, 0.60);
}
.title{
    text-align : center;
    margin-bottom : 2%;
    font-weight: bold;
    font-size : 1.5em;
}
.content_box{
    display : flex;
}
.stats_box {
  display : flex;
  flex-direction: column;
  flex : 2;
  flex-grow :1;
}
.chart{
  padding : 4;
  height: 18vh;
  flex: 1 1 auto;
  overflow: auto;
  flex-grow :1;
}
.map{
    flex :1;
    flex-grow :1;
    border: 0.1mm ridge rgba(43, 43, 43, .9);
}
body {
}
</style>