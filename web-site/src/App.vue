<template>
  <div>
    <header>
      <div class="nav_">
        <img class="header_img" src="@/images/logo.png" />
        <div class="btn_nav">
          <router-link class="test" to="/">Accueil</router-link>

          <router-link class="test" to="/Contact">Contact</router-link>

          <router-link class="test" to="/Map">Carte</router-link>

          <router-link class="test" to="/Upload"
            >Uploader des images</router-link
          >
        </div>
        <div class="btn_log">
          <input
            class="bouton_log"
            type="button"
            value="Surfrider"
            onclick="window.location.href ='https://surfrider.eu/'"
          />
        </div>
      </div>
    </header>
    <router-view />
  </div>
</template>
<script>
export default {
  name: "app",
};
</script>

<style>
body {
  margin: 0;
  font-family: sans-serif;
  background: url("images/tortue.jpeg") no-repeat center center fixed;
  box-shadow: inset 0 0 0 1000px rgba(0, 0, 0, 0.1);
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
  bottom: 0;
}

header {
  background-color: hsla(160, 40%, 61%, 0.911);
  padding: 3.2em;
  margin: 0;
}
header {
  max-height: 3em;
}

.nav_ {
  display: flex;
  justify-content: space-between;
}

.btn_nav {
  display: flex;
  flex-grow: 2;
  justify-content: space-around;
  max-width: 60%;
  color: black;
}
.test {
  display: flex;
  flex-grow: 2;
  justify-content: space-around;
  max-width: 60%;
  color: rgba(43, 43, 43, 1);
  text-decoration: none;
  font-size: 1.6em;
}
.test:hover {
  text-shadow: 1px 1px 2px black;
}
header input {
  border: none;
  border-radius: 2em;
  font-weight: bold;
  height: min-content;
  width: max-content;
}

header input:hover {
  cursor: pointer;
  background-color: hsla(160, 40%, 61%, 0.911);
  border: solid black;
}
.header_img {
  width: 12%;
}

/* <div id="nav">
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </div>
  <router-view/> */
</style>
