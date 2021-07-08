<template>
        <div id="container">
            <div v-if = "!connected">
            <form id = "formulaire">
                <h5>Connexion</h5>
                <div id = "champTexte">
                <label><b>Email</b></label>
                <input class = "texte" type="email" placeholder="Votre adresse email" v-model = "email" required>

                <label><b>Mot de passe</b></label>
                <input class = "texte" type="password" placeholder="Votre mot de passe" v-model = "password" required>
                </div>
                <button id='submit' @click= "sendData()" >SE CONNECTER</button>
                <router-link id = "registerLink" to='/register'> Pas encore inscrit ? </router-link>
            </form>
            </div>
            <div v-else>
                <p> Vous etes deja connecte ! </p>
            </div>
            <div v-if = "error" id="error"> Cette combinaison adresse mail/mot de passe est introuvable </div>
        </div>
</template>

<script> //Tout est très classique ici
module.exports = {
    props : {
        connected :{ type: Boolean },

    },
  data() {
    return {
        email : "",
        password :"",
        error : false,
    };
},
watch : {
    connected : function() {
        if(this.connected){
            this.$router.push({name:'home'})
        }
    }
},
methods : {
    async sendData(){

        let data = {email : this.email, password : this.password}
        await this.$emit("send-data",data)
        await setTimeout(() => {}, 4000)
        this.error = true
    },
}    
}
</script>

<style>
#container{
    margin:0 auto;
    display : flex;
    flex-direction : column;
    margin-top : 3px;
}
#formulaire{
    width: 40%;
    margin-left: auto;
    margin-right: auto;
    margin-top : 3px;
}
h5{
    margin : 1%;
    margin-left : auto;
    margin-right : auto;
    text-align: center;
    font: 3em "Fira Sans", sans-serif;
    text-shadow: 1px 1px 1px rgb(20,20,20);
}
#champTexte{
    display : flex;
    flex-direction : column;
}
.texte{
    margin :1%;
    padding : 7px;
}
#submit{
    background-color: #DAA520;
    color: white;
    padding: 18px 20px;
    margin: 8px 0;
    border: none;
    cursor: pointer;
    width: 100%;
}
#submit:hover {
    background-color: white;
    color: #DAA520;
    border: 1px solid #DAA520;
}
#registerLink{
    float : right;
}
#error{
    font: 1em "Fira Sans", sans-serif;
    margin-left : auto;
    margin-right : auto;
    color : red;
    text-shadow: 1px 1px 1px rgb(20,20,20);
}
</style>