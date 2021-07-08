<template>
        <div id="container">
            <div v-if = "!connected">
            <form id = "formulaire">
                <h5>Inscription</h5>
                <div id = "champTexte">
                <label><b>Pseudonyme</b></label>
                <input class = "texte"  placeholder="Votre adresse email" v-model = "nickname" required>
                <label><b>Email</b></label>
                <input class = "texte" type="email" placeholder="Votre adresse email" v-model = "email" required>

                <label><b>Mot de passe</b></label>
                <input class = "texte" type="password" placeholder="Votre mot de passe" v-model = "password" required>
                </div>
                <button id='submit' @click = "register()">INSCRIPTION</button>
            </form>
            </div>
            <div v-else>
                <p> Vous etes deja connecte ! </p>
            </div>
            <div v-if = "nicknameError" class="error">Votre pseudonyme doit faire entre 3 et 18 caracteres  </div>
            <div v-if = "passwordError" class="error"> Votre mot de passe doit faire au moins 6 caracteres </div>
            <div v-if = "error" class="error"> L'inscription a echoue, peut etre que cette adresse mail est deja utilisé ? </div>
        </div>
</template>
<script>
module.exports = {
    props : {
        connected :{type: Boolean},
    },
    data() {
    return {
        email : "",
        password :"",
        nickname: "",
        nicknameError : false,
        passwordError : false,
        error : false,
    };
    },
    watch : {
    connected : function() { //Si l'inscription a réussit le statut connected va changer, on veut donc attraper cela pour rediriger l'utilisateur
        if(this.connected){
            this.$router.push({name:'home'})
        }
    }
},
    methods : {
        async register(){
            if(this.nickname.length <= 3 || this.nickname.length >  18){ //On verifie que le format est honnete (NB : par manque de temps on ne le fait pas cote serveur)
                this.nicknameError = true
            }
            else if(this.password.length < 6){
                this.passwordError = true
            }
            else{
                registerInfos = {nickname : this.nickname,email : this.email, password : this.password}
                await this.$emit("register",registerInfos)
                await setTimeout(() => {}, 4000)
                this.error = true
            }
        },
    },
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
.error{
    font: 1em "Fira Sans", sans-serif;
    margin-left : auto;
    margin-right : auto;
    color : red;
    text-shadow: 1px 1px 1px rgb(20,20,20);
}
</style>