<!--
Programmer Name:    CHIAM ZHONG HAO
Program Name:       views/LandingPage.vue
Description:        It is the landing page of VAC. It will redirect the user to respective page based on user's selection.
First Written On:   01/01/2021
Edited On:          04/03/2021
-->
<template>
  <v-container fill-height fluid class="teal lighten-5 pa-0">
    <v-container>
      <!-- LOGO -->
      <v-row align="center" justify="center">
        <v-col align="center" cols="12">
          <v-img src="@/assets/VAC-logos_black.png" alt="" height="200" max-height="200" width="300" max-width="300"></v-img>
        </v-col>
      </v-row>
      <!-- TO VISITOR PAGE -->
      <v-row align="center" justify="center" class="my-1">
        <v-col align="center" cols="12">
          <v-btn @click="goToVisitor()" depressed :width="width" height="60" class="teal lighten-4">VISITOR</v-btn>
        </v-col>
      </v-row>
      <!-- TO SIGN IN PAGE (RESIDENT) -->
      <v-row align="center" justify="center" class="my-1">
        <v-col align="center" cols="12">
          <v-btn @click="goToSignInR()" depressed :width="width" height="60" class="teal lighten-2">RESIDENT</v-btn>
        </v-col>
      </v-row>
      <!-- TO SIGN IN PAGE (SMO) -->
      <v-row align="center" justify="center" class="my-1"> 
        <v-col align="center" cols="12">
          <v-btn @click="goToSignInS()" depressed :width="width" height="60" class="teal darken-1">SMO</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script>
import { getUser } from '../utils';

export default {
  name: 'LandingPage',
  computed: {
    width () {
      switch (this.$vuetify.breakpoint.name) { //adjust button width according to screen size
        case 'xs': return 300
        case 'sm': return 400
        case 'md': return 600
        case 'lg': return 800
        case 'xl': return 1000
      }
      return 1
    },
  },
  data() {
    return {
      resident: null,
    }
  },
  created() {
    let payload = getUser();
    if (payload != false) { //if got token, push user to smo/resident page
      this.resident = payload.resident;
      this.resident ? this.$router.push({ name: 'ResidentPage' }) : this.$router.push({ name: 'SMOPage' })
    }
  },
  methods: {
    goToVisitor() {
      this.$router.push({name: 'VisitorPage'});
    },
    goToSignInR() {
      this.$router.push({name: 'SignInPage', params: {identity: 'resident' }});
    },
    goToSignInS() {
      this.$router.push({name: 'SignInPage', params: {identity: 'smo' }});
    }
  }
}
</script>
