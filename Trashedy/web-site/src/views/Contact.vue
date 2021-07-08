<template>
  <div class="container">
    <h1>
      La Fondation Surfrider est dévouée à la protection des océans du monde
      entier, des plages et des vagues, pour tous, à travers un réseau actif de
      bénévoles.
    </h1>

    <div class="conteneur_goal">
      <div class="goal">
        <h2>Pollution plastique</h2>
        <p>
          Réduire l’impact du plastique dans les environnements marins qui nous
          entourent.
        </p>
      </div>
      <div class="goal">
        <h2>Protection des océans</h2>
        <p>
          Défendre nos océans face aux défis qui menacent la vitalité de
          l’écosystème.
        </p>
      </div>
      <div class="goal">
        <h2>Accès aux plages</h2>
        <p>Assurer un accès total et équitable des plages.</p>
      </div>
      <div class="goal">
        <h2>Préservation cotière</h2>
        <p>
          Prendre à corps des problèmes qui mettent en danger nos plages et nos
          côtes.
        </p>
      </div>
      <div class="goal">
        <h2>Nettoyage des océans</h2>
        <p>
          Assurer la santé e t la durabilité des ressources les plus précieuses
          de notre planète.
        </p>
      </div>
    </div>
    <div class="conteneur_perso">
      <div class="perso">
        <h3>Camélia</h3>
        <img class="perso_img" src="@/images/cam_photo.png" />
        <p>
          Créative et consciencieuse, j’aime apporter une brise de fraîcheur au
          sein du groupe. Que ce soit autour du design, des livrables ou des
          maquettes, je m’applique à faire briller le groupe. En tant que chef
          de projet, je veille à ce que le travail se déroule dans les
          meilleures conditions.
        </p>
      </div>
      <div class="perso">
        <h3>Benoit</h3>
        <img class="perso_img" src="@/images/ben_photo.jpg" />
        <p>
          Dynamique et fonceur, j’aime pousser mon équipe à se surpasser afin de
          remplir tous nos objectives ! Je fais de mon mieux pour associer au
          mieux la motivation de chacun et la bonne entente du groupe. Je fais
          aussi preuve de discernement et envisage toutes les options lors du
          déroulement du projet !
        </p>
      </div>
      <div class="perso">
        <h3>Maximilien</h3>
        <img class="perso_img" src="@/images/max_photo.png" />
        <p>
          Concepteur et expert, je propose des routes innovantes pour réaliser
          le projet. Je suis responsable de l’architecture globale et de
          l’implémentation en détail des solutions techniques.
        </p>
      </div>
      <div class="perso">
        <h3>Amélie</h3>
        <img class="perso_img" src="@/images/ame_photo.jpg" />
        <p>
          Je suis toujours fiable et organisée dans mon travail, j'aime suivre
          une méthode de travail stricte et cohérente pour le projet. J'ai
          également un certain attrait pour la perfection, j'aime rendre un
          travail abouti et complet, fidèle à notre cahier des charges
        </p>
      </div>
      <div class="perso">
        <h3>Rémi</h3>
        <img class="perso_img" src="@/images/remi_photo.png" />
        <p>
          Je suis une personne toujours à l'écoute des membres des groupes pour
          les accompagner jusqu'à la réussite du projet et être un soutien pour
          l'équipe ! J'apprécie également être le promoteur de l'équipe, c'est à
          dire communiquer avec tous les membres de l'équipe et faire la
          passerelle avec d'éventuels autres personnes nous accompagnant sur le
          projet.
        </p>
      </div>
      <div class="perso">
        <h3>Luc</h3>
        <img class="perso_img" src="@/images/luc_photo.jpg" />
        <p>
          En tant que développeur de l’équipe, il est pour moi primordial de
          mettre mes différentes connaissances spécifiques au service du projet.
          J’accorde une place importante à la bonne entente au sein du groupe.
        </p>
      </div>
    </div>
  </div>
</template>
<script>
module.exports = {
  props: {},
  data() {
    return {
      a: 1,
    };
  },

  methods: {},
};
</script>
<style scoped>
.container {
  background-color: rgba(250, 235, 215, 0.6);
  padding: 2%;
}
h1 {
  margin: 9%;
  padding: 1%;
  text-align: center;
}

.conteneur_goal {
  display: flex;
  margin: 1%;
  padding: 1rem;
  justify-content: space-around;
  flex-wrap: wrap;
}

.goal {
  width: 10%;
  border: 0.1mm ridge rgba(43, 43, 43, 0.9);
  padding: 2rem;
  margin: 1%;
  text-align: center;
  background-color: rgba(250, 245, 235, 0.6);
}

.conteneur_perso {
  display: flex;
  flex-direction: column;
  margin: 3%;
}

.perso {
  display: flex;
  margin: 4em 0;
  background-color: rgba(250, 235, 215, 0.6);
  padding: 1em;
  border-radius: 2em;
  border: 0.1mm ridge rgba(43, 43, 43, 0.9);
}

.perso p {
  font-style: italic;
  text-align: center;
  padding-top: 5%;
}

.perso h3 {
  padding: 2em 2em 0 2em;
}

.perso_img {
  width: 12em;
  border-radius: 2em;
}
</style>
