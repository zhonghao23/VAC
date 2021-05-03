<!--
Programmer Name:    CHIAM ZHONG HAO
Program Name:       views/SignInPage.vue
Description:        It is the sign in page of VAC. It will validate the username and password, redirect the user to the corresponding main page.
First Written On:   01/01/2021
Edited On:          04/03/2021
-->
<template>
  <v-container fill-height fluid class="teal lighten-5 pa-0">
<!-- LOGIN -->
    <v-container>
      <!-- BACK BUTTON -->
      <v-row align="start" justify="start">
        <v-col align="start" cols="2" sm="1">
          <v-icon x-large @click="goToLanding()">mdi-arrow-left-circle</v-icon>
        </v-col>
      </v-row>
      <v-row align="center" justify="center">
        <!-- LOGO -->
        <v-col align="center" cols="12" class="py-0 mb-n3">
          <v-img src="@/assets/VAC-logos_black.png" alt="" height="200" max-height="200" width="300" max-width="300"></v-img>
        </v-col>
        <!-- WELCOME BACK! -->
        <v-col align="center" cols="12" class="pt-0 mt-n3">
          <h2>Welcome Back!</h2>
        </v-col>
        <!-- RESIDENT -->
        <v-col align="center" cols="6" class="pr-1">
          <v-btn v-if="resident == true" @click="resident = true" block depressed class="teal darken-1">RESIDENT</v-btn>
          <v-btn v-else-if="resident == false" @click="resident = true" block depressed class="teal lighten-4">RESIDENT</v-btn>
        </v-col>
        <!-- SMO -->
        <v-col align="center" cols="6" class="pl-1">
          <v-btn v-if="resident == true" @click="resident = false" block depressed class="teal lighten-4">SMO</v-btn>
          <v-btn v-else-if="resident == false" @click="resident = false" block depressed class="teal darken-1">SMO</v-btn>
        </v-col>
      </v-row>
      <!-- SIGN IN FORM -->
      <ValidationObserver ref="signinForm">
        <form>
          <v-row align="center" justify="center">
            <!-- USERNAME -->
            <v-col cols="12" align="center" justify="center">
              <ValidationProvider name="Username" rules="required3|alpha_num|minMax2:8,15" v-slot="{ errors }">
                <v-text-field
                  v-model="username"
                  label="Username"
                  outlined rounded dense clearable hide-details
                  color="teal darken-3"
                  autocomplete="off"
                  maxlength="15"
                  >
                </v-text-field>
                <ul class="text-left teal--text teal--darken-4 caption font-italic font-weight-bold">
                  <li v-for="(error, index) in errors" :key="index">
                    <span>{{ error }}</span>
                  </li>
                </ul>
              </ValidationProvider>
            </v-col>
            <!-- PASSWORD -->
            <v-col cols="12" align="center" justify="center">
              <ValidationProvider name="Password" rules="required3|minMax2:8,15|customPassword" v-slot="{ errors }">
                <v-text-field
                  v-model="password"
                  label="Password"
                  :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="show ? 'text' : 'password'"
                  @click:append="show = !show"
                  outlined rounded dense clearable hide-details
                  color="teal darken-3"
                  autocomplete="off"
                  maxlength="15"
                  >
                </v-text-field>
                <ul class="text-left teal--text teal--darken-4 caption font-italic font-weight-bold">
                  <li v-for="(error, index) in errors" :key="index">
                    <span>{{ error }}</span>
                  </li>
                </ul>
              </ValidationProvider>
            </v-col>
            <!-- SIGN IN BUTTON -->
            <v-col cols="12" align="center" justify="center">
              <v-btn @click="signIn()" depressed :width="widthSignInButton" class="teal lighten-2">SIGN IN</v-btn>
            </v-col>
          </v-row>
        </form>
      </ValidationObserver>
    </v-container>
    <!-- POP UP MESSAGE -->
    <v-dialog v-model="dialogLogin" max-width="400">
      <v-card>
        <v-card-title class="teal lighten-2">
          {{ dialog_msg_header }}
        </v-card-title>
        <v-card-text class="subtitle-1 font-weight-bold mt-2">
          {{ dialog_msg }}
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialogLogin = false" text color="primary">
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ValidationProvider, extend, ValidationObserver } from "vee-validate";
import { required, alpha_num } from 'vee-validate/dist/rules';
import axios from 'axios';
import { getUser } from '../utils'

var errorMessage = " must include 1 lower-case, 1 upper-case, 1 number and special character ($@$!%*#?&)";
extend('required3', {
  ...required,
  message: 'Fill in to Sign In'
})
extend('customPassword', {
  message: field => "The " + `${field}` + errorMessage,
  validate: value => {
    var notTheseChars = /["'?/<>\s\\#()_+=[\]{}|:;,.`~]/;
    var mustContainTheseChars = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!@#$%^&*-]).{8,}$/;

    var containsForbiddenChars = notTheseChars.test(value);
    var containsRequiredChars = mustContainTheseChars.test(value);

    if (containsRequiredChars && !containsForbiddenChars) {
      return true;
    } else {
      if (containsForbiddenChars) {
        errorMessage = ' cannot contain characters: " ' + " ' ? # / \\ < > ( ) _ + = [ ] { } | : ; , . ` ~ or space";
      } else {
        errorMessage = " must include 1 lower-case, 1 upper-case, 1 number and special character (!@$%^&*-)";
      }
      return false;
    }
  }
})
extend('minMax2', {
  validate(value, { min, max}) {
    return value.length >= min && value.length <= max;
  },
  params: ['min', 'max'],
  message: '{_field_} must be only between {min} to {max} numbers'
})
extend('alpha_num', {
  ...alpha_num,
  message: 'Must be only alphabetic characters or numbers'
})


export default {
  name: 'SignInPage',
  computed: {
    widthSignInButton () {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return 200
        case 'sm': return 400
        case 'md': return 600
        case 'lg': return 800
        case 'xl': return 1000
      }
      return 1
    },
  },
  data() {
    return{
      resident: true,
      username: '',
      password: '',
      show: false,
      identity: '',
      dialogLogin: false,
      dialog_msg_header: '',
      dialog_msg: '',
    }
  },
  created() {
    let payload = getUser();
    if (payload != false) { //if got token, push user to smo/resident page
      this.resident = payload.resident;
      this.resident ? this.$router.push({ name: 'ResidentPage' }) : this.$router.push({ name: 'SMOPage' })
    }else {
      this.identity = this.$route.params.identity
      if (this.identity == "resident") {
        this.resident = true;
      }else if (this.identity == "smo") {
        this.resident = false;
      }
    }
  },  
  methods:
  {
    signIn() { //sign in
      this.$refs.signinForm.validate().then(success => {
        if (!success) {
          return;
        }
        let hostname = window.location.hostname;
        let API_URL = `http://${hostname}:5000/signin`;
        const payload = {
          username: this.username,
          password: this.password,
          resident: this.resident
        }
        axios.post(API_URL, payload)
        .then((res) => {
          if (res.data.token) {
            localStorage.setItem('user', JSON.stringify(res.data));
            this.resident ? this.$router.push({ name: 'ResidentPage' }) : this.$router.push({ name: 'SMOPage' })
          } 
          else {
            this.dialog_msg_header = 'Unsuccessful Sign In';
            this.dialog_msg = res.data;
            this.dialogLogin = true;
          }
        })
        .catch((error) => {
          alert("You are offline! Please connect to internet and try again.")
          console.log(error)
        })       
      })
    },
    goToLanding() {
      this.$router.push({name: 'LandingPage'});
    }
  },
  components:{
    ValidationProvider,
    ValidationObserver
  },
}
</script>