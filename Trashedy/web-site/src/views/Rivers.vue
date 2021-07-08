<template>
  <div class="container">
      <div class = "entete">
          <div class = "name_river"> Nom du cours d'eau</div>
          <div class = "length_river" > Taille du cours d'eau </div>
          <div class = "waste_number" > Nombre de déchets signalés</div>
      </div>
     <article
        class="rivers"
        v-for="river in rivers"
        :key="river.nom_fleuve"
        @click="redirect_to_river(river.nom_fleuve)"
      >
      <div class = "river ">
          <div class = "name_river"> {{river.nom_fleuve}} </div>
          <div class = "length_river" > {{river.longueur + " km"}} </div>
          <div class = "waste_number" >  {{river.nbe_dechets + " déchets signalés" }} </div>
      </div>

      </article>
  </div>
</template>
  
<script>
  export default {
    data(){
      return {
        rivers : [],
        loaded : false,
        show_usine_recyclage: 0,
        show_usine : 1,
      }
    },
    async mounted() {
         const res = await axios.get('http://localhost:5000/get_rivers')
         console.log(res.data)
         this.rivers = res.data
    },
    methods: {
          switch_show_usine(){
            this.show_usine = (this.show_usine+1)%2
            console.log(this.show_usine)
            },
        redirect_to_river(river_name){
            this.$router.push('/river/' + river_name) 
            },
    }
  }
</script>
<style scoped>
.container{
    margin-top : 9%;
}
.entete{
    background-color: rgba(152, 219, 196, 0.850);
    border-radius: 0.1em;
    border: 0.5mm ridge rgba(43, 43, 43, .9);
    padding : 6px;
    margin : 0.2%;
    display : flex;
    box-shadow: 1px 1px rgba(55, 55, 55, 0.2);
    flex-direction : row;
    font-weight: bold;
}
.river{
    background-color: rgba(250, 235, 225, 0.850);
    border-radius: 0.1em;
    border: 0.1mm ridge rgba(43, 43, 43, .9);
    padding : 6px;
    margin : 0.2%;
    display : flex;
    box-shadow: 1px 1px rgba(55, 55, 55, 0.2);
    flex-direction : row;
}
.river:hover{
  cursor: pointer;
  background-color: rgba(240,230,215,0.9));
  box-shadow: 2px 2px rgba(55, 55, 55, 0.4);
  border: 1px solid black;
}
.length_river{
    flex : 1;
    flex-grow : 1;
}
.name_river{
    flex : 1;
    flex-grow : 1;
}
.waste_number{
    flex : 1;
    flex-grow : 1;
}
</style>