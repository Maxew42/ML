<template>
  <div class="container1">
    <div class="container2" v-if="!data_sent">
      <div class="upload_box">
        <input
          v-if="!results_loaded"
          type="file"
          id="file"
          ref="file"
          v-on:change="onChangeFileUpload()"
        />
        <button v-if="!results_loaded" v-on:click="submitForm()">Upload</button>
        <div v-if="results_loaded" v-html="map" class="map"></div>
      </div>
      <div class="prediction_box" v-if="file === ''">
        Aucune image detectée
      </div>
      <div class="imgHolder">
        <div
          class="bounding-box-container"
          v-if="results_loaded"
          v-for="row in bounding"
          :key="row.id"
        >
          <div v-bind:style="bounding_style[row.id]"></div>
          <div v-bind:style="bounding_text_style[row.id]">
            {{ row.classes }}
          </div>
        </div>
      </div>
    </div>
    <div v-if="results_loaded && !data_sent" class="footer_map">
      <div class="champ_texte_box">
        <div class="champ_texte_title">Date</div>
        <input
          class="champ_texte"
          id="date"
          v-model="date"
          placeholder="year-month-day"
        />
      </div>
      <div class="champ_texte_box">
        <div class="champ_texte_title">Latitude</div>
        <input class="champ_texte" v-model="latitude" placeholder="Latitude" />
      </div>
      <div class="champ_texte_box">
        <div class="champ_texte_title">Longitude</div>
        <input
          class="champ_texte"
          v-model="longitude"
          placeholder="Longitude"
        />
      </div>
      <div class="champ_texte_box">
        <div class="champ_texte_title">Nom du cours d'eau</div>
        <input class="champ_texte" v-model="river" placeholder="Nom" />
      </div>
      <button class="button_send" v-on:click="send_data()">{{ "Ajouter " + bounding.length + " déchets"}}</button>
    </div>
    <div v-if="data_sent" class="validation_message">
      Hop là, tout est bon ! Merci pour votre aide ;)
    </div>
    <div v-if="error_sending" class="error_message">
      Une erreur est survenue, vérifiez les informations entrées !
    </div>
  </div>
</template>

<script>
export default {
  //    <canvas v-else id="canvas" ref="canvas" v-insert-box="{ image: file }">    </canvas>
  //<img :src="file_2" alt="">     <div class="box" :style="{top: 50 + 'px', left: 12 + 'px', width: 50 + 'px', height: 12 + 'px'}"></div>
  data() {
    return {
      height_image: 420,
      file: "",
      file_2: "",
      results: "",
      results_loaded: false,
      bounding: [],
      heigth: 0,
      width: 0,
      bounding_style: [],
      date: "",
      latitude: "",
      longitude: "",
      proc_exif_alert: false,
      map: "",
      data_sent: false,
      river: "",
      error_sending: false,
      bounding_text_style: {},
    };
  },
  methods: {
    async submitForm() {
      let formData = new FormData();
      formData.append("file", this.file);

      const res = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      this.bounding = this.process_results(res.data);
      this.bounding_style = this.get_style_from_bounding(this.bounding)[0];
      this.bounding_text_style = this.get_style_from_bounding(this.bounding)[1];
      this.results_loaded = true;
    },
    get_style_from_bounding(bound) {
      let style_liste = [];
      let text_style_liste = [];
      let row = {};
      for (var i in bound) {
        row = bound[i];
        style_liste.push({
          position: "absolute",
          top: row.ymin + "px",
          left: row.xmin + "px",
          width: row.xmax - row.xmin + "px",
          height: row.ymax - row.ymin + "px",
          border: "0.6mm ridge rgba(190, 43, 43, 0.9)",
        });
        text_style_liste.push({
          position: "absolute",
          top: row.ymin + 4 + "px",
          left: row.xmin + 4 + "px",
          color: "red",
        });
      }
      return [style_liste, text_style_liste];
    },
    process_results(results) {
      let image = document.querySelector(".uploaded_img");
      let data = results.results;
      this.height = results.height;
      this.width = results.width;
      this.latitude = results.latitude;
      this.longitude = results.longitude;
      this.date = results.date;
      this.map = results.map;
      if (this.date === "" || this.longitude === "") {
        this.proc_exif_alert = true;
      }
      let new_bound = [];
      let cpt = 0;
      let image_width = (this.height_image * this.width) / this.height;
      console.log(this.width);
      let xminp = 0;
      let xmaxp = 0;
      let yminp = 0;
      let ymaxp = 0;
      let row = {};
      for (var i in data) {
        row = data[i];
        xminp = (row.xmin * image_width) / this.width;
        xmaxp = (row.xmax * image_width) / this.width;
        yminp = (row.ymin * this.height_image) / this.height;
        ymaxp = (row.ymax * this.height_image) / this.height;
        new_bound.push({
          id: cpt,
          classes: row.classes,
          scores: row.scores,
          xmin: xminp,
          xmax: xmaxp,
          ymin: yminp,
          ymax: ymaxp,
        });
        cpt = cpt + 1;
      }
      console.log(new_bound);
      return new_bound;
    },
    async send_data() {
      try {
        let data = {
          waste_info: this.bounding,
          latitude: this.latitude,
          longitude: this.longitude,
          date: this.date,
          river: this.river,
        };
        this.error_sending = false;

        const res = await axios.post(
          "http://localhost:5000/send_result",
          data,
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        this.data_sent = true;
      } catch (err) {
        this.error_sending = true;
        alert("Attention les données ne sont pas valides");
      }
    },
    onChangeFileUpload() {
      this.file = this.$refs.file.files[0];
      this.file_2 = URL.createObjectURL(this.file);
      var image = document.createElement("img");
      let imgHolder = document.querySelector(".imgHolder");
      imgHolder.appendChild(image);
      image.src = URL.createObjectURL(this.file);
      image.className = "uploaded_img";
      image.style.height = this.height_image + "px";
    },
  },
  directives: {
    insertBox(canvasElement, binding) {
      var ctx = canvasElement.getContext("2d");

      // var img = document.getElementById('img')

      image.onload = () => {
        var imgwidth = image.offsetWidth;
        var imgheight = image.offsetHeight;
        ctx.drawImage(image, 0, 0);
        ctx.beginPath();
        ctx.rect(0, 0, 100, 100);
        ctx.lineWidth = 2;
        ctx.strokeStyle = "yellow";
        ctx.stroke();
      };
    },
  },
};
</script>
<style scoped>
.error_message {
  color: red;
  text-align: center;
  font-size: 1.2em;
}
.validation_message {
  padding: 4%;
  font-weight: bold;
  font-size: 2em;
  text-align: center;
}
.map {
  height: 420;
}
.champ_texte_box {
  display: flex;
  flex-direction: column;
}
.champ_texte_title {
  text-align: center;
  font-weight: bold;
}
.footer_map {
  display: flex;
  flex-direction: row;
}
.champ_texte {
  margin: 3%;
  padding: 3px;
}
.imgHolder {
  position: relative;
  width: auto;
}
.uploaded_img {
  max-width: 0px;
  height: 0px;
}
.container1 {
  margin: 9%;
  margin-right: 5%;
  margin-left: 5%;
  background-color: rgba(250, 235, 215, 0.6);
  padding: 5%;
  display: flex;
  flex-direction: column;
}
.container2 {
  border: 0.1mm ridge rgba(43, 43, 43, 0.9);
  display: flex;
  flex-direction: row;
}
.canvas {
  flex: 4;
}
.upload_box {
  background-color: rgba(250, 235, 225, 0.85);
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 2%;
}
.prediction_box {
  border: 0.3mm ridge rgba(43, 43, 43, 0.9);
  display: flex;
  background-color: rgba(250, 240, 240, 0.85);
  flex-grow: 1;
  text-align: center;
  margin: 0 0;
  flex: 1;
  justify-content: center;
  align-items: center;
}
.button_send {
  padding: 3px;
  margin: 3%;
}
button {
  margin: 2%;
  background-color: hsla(160, 40%, 61%, 0.911);
  padding: 3%;
}
</style>
