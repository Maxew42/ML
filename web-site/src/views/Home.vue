<template>
  <div class="container">
    <div class="text_container">
      <div class="stat_box" id="stat1">
        <div class="stat_number">{{ nbe_dechets }}</div>
        <div class="stat_text">déchets detectés cette semaine</div>
      </div>
      <div class="stat_box" id="stat2">
        <div class="stat_number">{{ pire_departement }}</div>
        <div class="stat_text">
          est le département dont les cours d'eau sont les plus sales
        </div>
      </div>
      <div class="stat_box" id="stat3">
        <div class="stat_number">3</div>
        <div class="stat_text">
          opérations ramassage organisées par Surfrider ce mois-ci !
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "Home",
  data() {
    return {
      nbe_dechets: 0,
      pire_departement: "",
    };
  },
  async mounted() {
    const res = await axios.get("http://localhost:5000/getstats");
    console.log(res.data);
    this.nbe_dechets = res.data["nbe_dechets"][0];
    this.pire_departement = res.data["pire_departement"][0];
  },
};
</script>
<style scoped>
.container {
  margin: 3%;
  margin-top: 0%;
  padding: 5%;
  padding-top: 2%;
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 100%; /*new for extend*/
  overflow: hidden; /*new for extend*/
  bottom: 0px;
}
.html {
  margin-bottom: 0px;
  padding-bottom: 0px;
}
.body {
  height: 100%;
  bottom: 0px;
  display: flex;
  flex-grow: 1;
}
.text_container {
  margin-top: 3%;
}
.stat_box {
  margin: 2%;
  text-shadow: 1px 1px 2px black;
}
.stat_text {
  font-size: 2.1em;
  font-weight: bold;
  margin-top: 0px;
}

.stat_number {
  font-size: 5.3em;
  font-weight: bold;
}
</style>
