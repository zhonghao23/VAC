<!--
Programmer Name:    CHIAM ZHONG HAO
Program Name:       App.vue
Description:        It is the main file where the server will look into and instantiate the entire vue project.
First Written On:   01/01/2021
Edited On:          04/03/2021
-->
<template>
  <v-app>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
//import smtg and put into components

export default {
  name: 'App',
  components:{
  }
};
</script>
