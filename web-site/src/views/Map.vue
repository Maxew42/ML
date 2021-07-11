<template>
  <div class="container">
    <div class = "interactive_map_container">
      <div class = "opts_container"> 
        <div> FILTRES </div>
        <button v-on:click="switch_show_usine()" class = "bouton">Afficher les usines</button>
        <button v-on:click="submitForm()" class = "bouton">Afficher les centres de recyclage</button> 
        <button v-on:click="switch_to_fleuve()" class = "bouton">Accéder à la liste des cours d'eau</button> 
      </div>
      <div v-html="map" class = "map"></div>
    </div>
  </div>
</template>
  
<script>
  export default {
    data(){
      return {
        map: '',
        loaded : false,
        show_usine_recyclage: 0,
        show_usine : 0,
      }
    },
    async mounted() {
         const res = await axios.get('http://localhost:5000/getmap', { params: { usine_recyclage : this.show_usine_recyclage, usine: this.show_usine } })
         console.log(res)
         this.map = res.data
         this.loaded = true
    },
    watch:{
      show_usine: async function() {
            const res = await axios.get('http://localhost:5000/getmap', { params: { usine_recyclage : this.show_usine_recyclage, usine: this.show_usine } }).then()
                  if(res.status === 200){
                      console.log(res)
                      this.map = res.data
                  }
      },
    },
    methods: {
          switch_show_usine(){
            this.show_usine = (this.show_usine+1)%2
            console.log(this.show_usine)
            },
          switch_to_fleuve(){
            this.$router.push({name:'Rivers'})
            }
    }
  }
</script>
<style scoped>
.interactive_map_container{
  display : flex;
  flex-direction: row;
  margin-top : 5%;
}
.opts_container{
  background-color: rgba(250, 235, 225, 0.850);
  margin: 1%;
  border: 0.1mm ridge rgba(43, 43, 43, .9);
  text-align : center;
  display : flex;
  flex-direction : column;
}
.bouton{
  margin : 3%;
  padding : 2%;
}
.map{
  border: 0.1mm ridge rgba(43, 43, 43, .9);
  height : 50%;
  width : 80%;
  flex-grow : 1;
  text-align : center;
  margin: auto auto;
}
</style>