<!--
Programmer Name:    CHIAM ZHONG HAO
Program Name:       views/SMOPage.vue
Description:        It is the security management office page of VAC. It provides all the functions for the security management office in this page.
First Written On:   01/01/2021
Edited On:          04/03/2021
-->
<template>
  <v-container fluid class="px-1">
    <!-- APP BAR -->
    <v-app-bar fixed app dense flat color="teal darken-1">
      <v-app-bar-nav-icon @click="nav_drawer = true" color="white"></v-app-bar-nav-icon>
      <v-toolbar-title v-if="btm_nav_bar == 'view_record' && view_own_profile == false" class="white--text">View Records & Info</v-toolbar-title>
      <v-toolbar-title v-else-if="btm_nav_bar == 'create_acc' && view_own_profile == false" class="white--text">Create Account (R)</v-toolbar-title>
      <v-toolbar-title v-else-if="btm_nav_bar == 'create_acc' && view_own_profile == true" class="white--text">View Profile</v-toolbar-title>
      <v-toolbar-title v-else-if="btm_nav_bar == 'view_record' && view_own_profile == true" class="white--text">View Profile</v-toolbar-title>
    </v-app-bar>
    <!-- NAVIGATION DRAWER -->
    <v-navigation-drawer v-model="nav_drawer" fixed temporary class="teal lighten-5" style="max-width:200px">
      <v-list nav dense>
        <v-list-item-group v-model="nav_group" class="teal lighten-5" active-class="teal-text text--accent-4">
          <v-list-item @click="viewOwnProfile()">
            <v-list-item-icon>
              <v-icon>mdi-account-circle</v-icon>
            </v-list-item-icon>
            <v-list-item-title class="body-1 teal--text text--darken-4">VIEW PROFILE</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
      <template v-slot:append>
        <div class="pa-2">
          <v-btn @click="signOut()" block color="teal lighten-1" class="white--text">
            LOGOUT
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
<!-- VIEW OWN PROFILE -->
    <v-container v-if="view_own_profile == true">
      <v-row align="start" justify="start">
        <v-col align="start" cols="2" sm="1" class="pb-0">
          <v-icon @click="view_own_profile = false" x-large>mdi-arrow-left-circle</v-icon>
        </v-col>
      </v-row>
      <v-container>
        <v-row dense>
          <v-col cols="12" align="center">
            <v-card color="#385F73" dark>
              <v-icon x-large class="pt-3">mdi-account-circle</v-icon>
              <v-card-title class="overline pb-0 justify-center">NAME<br>{{ own_name }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">USERNAME<br>{{ own_username }}</v-card-title>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-container>
<!-- VIEW RECORDS AND INFORMATION -->
    <v-container v-if="btm_nav_bar == 'view_record' && viewSpecificRes == false && viewSpecificVis == false && view_own_profile == false" class="overflow-hidden">
      <!-- VIEW RESIDENT BUTTON -->
      <v-row align="center" justify="center">
        <v-col cols="12">
          <v-btn @click="viewRecord(1)" block elevation="0" class="teal lighten-5">RESIDENT'S INFORMATION</v-btn>
        </v-col>
      </v-row>
      <!-- VIEW RESIDENT'S INFORMATION -->      
      <v-row v-if="viewRes == true" align="center" justify="center">
        <v-container v-for="resident in residents" :key="resident.res_id">
          <v-row dense>
            <v-col cols="12">
              <v-card color="#385F73" dark @click="viewSpecificR(resident)">
                <v-card-title class="overline pt-0 pb-0">Unit {{ resident.r_unitno }}</v-card-title>
                <v-card-title class="overline pt-0 pb-0">{{ resident.r_name }}</v-card-title>
                <v-card-subtitle class="overline pb-0">{{ resident.r_contactno }}</v-card-subtitle>
                <v-card-title v-if="resident.res_lp_string != ''" class="subtitle-1 pt-0 pb-0">{{ resident.res_lp_string }}</v-card-title>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
        <!-- PREVIOUS NEXT BUTTON -->
        <v-col cols="12" align="center">
          <v-btn @click="nextPrevRecord(-10, 1)" fab small class="mr-2" elevation="0">
            <v-icon>mdi-arrow-left-bold-outline</v-icon>
          </v-btn>
          <v-btn @click="nextPrevRecord(10, 1)" fab small class="ml-2" elevation="0">
            <v-icon>mdi-arrow-right-bold-outline</v-icon>
          </v-btn>
        </v-col>
      </v-row>
      <!-- VIEW VISITS BUTTON -->
      <v-row align="center" justify="center">
        <v-col cols="12">
          <v-btn @click="viewRecord(2)" block elevation="0" class="teal lighten-3">VISITS</v-btn>
        </v-col>     
      </v-row>
      <!-- VIEW VISITS RECORDS -->
      <v-row v-if="viewVisit == true" align="center" justify="center">
        <v-container v-for="visit in visits" :key="visit.visit_id">
          <v-row dense>
            <v-col cols="12">
              <v-card color="#385F73" dark @click="viewSpecificV(visit)">
                <v-card-title class="overline pt-0 pb-0">VISIT ON: {{ visit.visit_on }}</v-card-title>
                <v-card-title class="overline pb-0 pt-0">{{ visit.plate_number }}</v-card-title>
                <v-card-subtitle class="overline pb-0">{{ visit.v_name }}</v-card-subtitle>
                <v-card-title class="overline pb-0 pt-0">UNIT {{ visit.r_unitno }}</v-card-title>
                <v-card-subtitle v-if="visit.visit_status == 'APPROVED'" class="overline font-italic font-weight-black light-green--text text--accent-3 pb-0">{{ visit.visit_status }}</v-card-subtitle>
                <v-card-subtitle v-else-if="visit.visit_status == 'PENDING'" class="overline font-italic font-weight-black light-blue--text text--lighten-3 pb-0">{{ visit.visit_status }}</v-card-subtitle>
                <v-card-subtitle v-else-if="visit.visit_status == 'REJECTED'" class="overline font-italic font-weight-black deep-orange--text text--lighten-2 pb-0">{{ visit.visit_status }}</v-card-subtitle>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
        <!-- PREVIOUS NEXT BUTTON -->
        <v-col cols="12" align="center">
          <v-btn @click="nextPrevRecord(-10, 2)" fab small class="mr-2" elevation="0">
            <v-icon>mdi-arrow-left-bold-outline</v-icon>
          </v-btn>
          <v-btn @click="nextPrevRecord(10, 2)" fab small class="ml-2" elevation="0">
            <v-icon>mdi-arrow-right-bold-outline</v-icon>
          </v-btn>
        </v-col>
      </v-row>        
      <!-- VIEW ENTRYEXIT BUTTON -->
      <v-row align="center" justify="center">
        <v-col cols="12">
          <v-btn @click="viewRecord(3)" block elevation="0" class="teal lighten-1">VEHICLE'S ENTRY & EXIT</v-btn>
        </v-col> 
      </v-row>
      <!-- VIEW ENTRYEXIT RECORDS -->
      <v-row v-if="viewEE == true" align="center" justify="center">
        <v-container v-for="entryexit in ee" :key="entryexit.ee_id">
          <v-row dense>
            <v-col cols="12">
              <v-card color="#385F73" dark>
                <v-card-title class="overline pt-0 pb-0">LICENSE PLATE: {{ entryexit.plate_number }}</v-card-title>
                <v-card-title class="overline pt-0 pb-0">ENTRY: {{ entryexit.ee_entryon }}</v-card-title>
                <v-card-title class="overline pt-0 pb-0">EXIT: {{ entryexit.ee_exiton }}</v-card-title>
                <v-card-title class="overline pb-0 pt-0">{{ entryexit.name }}</v-card-title>
                <v-card-subtitle class="overline pb-0">{{ entryexit.contactno }}</v-card-subtitle>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
        <!-- PREVIOUS NEXT BUTTON -->
        <v-col cols="12" align="center">
          <v-btn @click="nextPrevRecord(-10, 3)" fab small class="mr-2" elevation="0">
            <v-icon>mdi-arrow-left-bold-outline</v-icon>
          </v-btn>
          <v-btn @click="nextPrevRecord(10, 3)" fab small class="ml-2" elevation="0">
            <v-icon>mdi-arrow-right-bold-outline</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
<!-- VIEW SPECIFIC RESIDENT INFORMATION -->
    <v-container v-else-if="btm_nav_bar == 'view_record' && viewSpecificRes == true" class="overflow-hidden">
      <v-row align="start" justify="start">
        <v-col align="start" cols="2" sm="1" class="pb-0">
          <v-icon @click="viewSpecificRes = false" x-large>mdi-arrow-left-circle</v-icon>
        </v-col>
      </v-row>
      <v-container>
        <v-row dense>
          <v-col cols="12" align="center">
            <v-card color="#385F73" dark>
              <v-icon x-large class="pt-3">mdi-account-circle</v-icon>
              <v-card-title class="overline pb-0 justify-center">UNIT<br>{{ specificRes.unitno }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">NAME<br>{{ specificRes.name }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">CONTACT NO<br>{{ specificRes.contactno }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">USERNAME<br>{{ specificRes.username }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">SECRET CODE<br>{{ specificRes.secretcode }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">ADDRESS<br>{{ specificRes.address }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">LICENSE PLATES (R)<br>{{ specificRes.res_lp }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">LICENSE PLATES (V)<br>{{ specificRes.vis_lp }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">LICENSE PLATES (BL)<br>{{ specificRes.vis_bl_lp }}</v-card-title>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-container>
<!-- VIEW SPECIFIC VISITS RECORD -->
    <v-container v-else-if="btm_nav_bar == 'view_record' && viewSpecificVis == true" class="overflow-hidden">
      <v-row align="start" justify="start">
        <v-col align="start" cols="2" sm="1" class="pb-0">
          <v-icon @click="viewSpecificVis = false" x-large>mdi-arrow-left-circle</v-icon>
        </v-col>
      </v-row>
      <v-container>
        <v-row dense>
          <v-col cols="12" align="center">
            <v-card color="#385F73" dark>
              <v-icon x-large class="pt-3">mdi-account-circle</v-icon>
              <v-card-title class="overline pb-0 justify-center font-weight-black">STATUS<br>{{ specificVis.visit_status }}</v-card-title>              
              <v-card-title class="overline pb-0 justify-center">LICENSE PLATE<br>{{ specificVis.plate_number }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">VISIT DATE<br>{{ specificVis.visit_on }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">VISIT PURPOSE<br>{{ specificVis.visit_purpose }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">UNIT <br>{{ specificVis.r_unitno }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">RESIDENT NAME<br>{{ specificVis.r_name }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">VISITOR NAME<br>{{ specificVis.v_name }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">VISITOR CONTACT NO<br>{{ specificVis.v_contactno }}</v-card-title>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-container>    
<!-- CREATE ACC FOR RESIDENT -->
    <v-container v-else-if="btm_nav_bar == 'create_acc' && view_own_profile == false">
      <!-- INPUT FORM -->
      <ValidationObserver ref="createAcc">
        <form>
          <v-row align="center" justify="center">
            <!-- RESIDENT NAME -->
            <v-col cols="12">
              <ValidationProvider name="ResidentName" rules="required|alpha_spaces" v-slot="{ errors }">
                <v-text-field 
                  v-model="resident_name"
                  label="Resident's Name"
                  outlined rounded dense clearable hide-details
                  color="teal darken-3"
                  placeholder="Chris Donovan"
                  autocomplete="off"
                  maxlength="30"
                  >
                </v-text-field>
                <ul class="text-left teal--text teal--darken-4 caption font-italic font-weight-bold">
                  <li v-for="(error, index) in errors" :key="index">
                    <span>{{ error }}</span>
                  </li>
                </ul>
              </ValidationProvider>
            </v-col>
            <!-- HOUSE UNIT NUMBER -->
            <v-col cols="12">
              <ValidationProvider name="UnitNumber" rules="required|alpha_num" v-slot="{ errors }">
                <v-text-field 
                  v-model="unit_number"
                  label="House Unit Number"
                  outlined rounded dense clearable hide-details
                  color="teal darken-3"
                  placeholder="B0109"
                  autocomplete="off"
                  maxlength="10"
                  >
                </v-text-field>
                <ul class="text-left teal--text teal--darken-4 caption font-italic font-weight-bold">
                  <li v-for="(error, index) in errors" :key="index">
                    <span>{{ error }}</span>
                  </li>
                </ul>
              </ValidationProvider>
            </v-col>
            <!-- ADDRESS -->
            <v-col cols="12">
              <ValidationProvider name="Address" rules="required" v-slot="{ errors }">
                <v-textarea 
                  v-model="resident_address"
                  label="Address"
                  outlined rounded dense clearable hide-details auto-grow rows="2"
                  color="teal darken-3"
                  placeholder="19, Jalan Alam Damai 7"
                  autocomplete="off"
                  maxlength="100"
                  >
                </v-textarea>
                <ul class="text-left teal--text teal--darken-4 caption font-italic font-weight-bold">
                  <li v-for="(error, index) in errors" :key="index">
                    <span>{{ error }}</span>
                  </li>
                </ul>
              </ValidationProvider>
            </v-col>
            <!-- CONTACT NUMBER -->
            <v-col cols="12">
              <ValidationProvider name="ContactNumber" rules="required|minMax:8,9" v-slot="{ errors }">
                <v-text-field 
                  v-model="contact_number"
                  label="Contact Number"
                  outlined rounded dense clearable hide-details
                  color="teal darken-3"
                  placeholder="23456789"
                  autocomplete="off"
                  maxlength="9"
                  prefix="+601"
                  >
                </v-text-field>
                <ul class="text-left teal--text teal--darken-4 caption font-italic font-weight-bold">
                  <li v-for="(error, index) in errors" :key="index">
                    <span>{{ error }}</span>
                  </li>
                </ul>
              </ValidationProvider>
            </v-col>
            <v-col cols="12" align="center" justify="center">
              <v-btn @click="createAcc()" depressed :width="widthRegisterButton" class="teal lighten-2">CREATE</v-btn>
            </v-col>
            <v-col cols="12" align="center" justify="center">
              <span class="body-1">The username, temporary password and secret code will be generated by the system automatically</span>
            </v-col>
          </v-row>
        </form>
      </ValidationObserver>
      <!-- POP UP MESSAGE -->
      <v-dialog v-model="dialogCreateAcc" max-width="400">
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
            <v-btn @click="dialogCreateAcc = false" text color="primary">
              OK
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
<!-- BOTTOM NAVIGATION BAR -->
    <v-bottom-navigation fixed app grow mandatory shift dark v-model="btm_nav_bar" background-color="teal darken-2">
      <v-btn value="view_record">
        <span>View Records & Info</span>
        <v-icon>mdi-account-box-multiple</v-icon>
      </v-btn>
      <v-btn value="create_acc">
        <span>Create Account</span>
        <v-icon>mdi-account-multiple-plus</v-icon>
      </v-btn>       
    </v-bottom-navigation>
  </v-container>
</template>

<script>
import { ValidationProvider, ValidationObserver } from "vee-validate";
import axios from 'axios';
import store from '../store';
import { getUser } from '../utils';
import authHeader from '../service/auth-header';

export default {
  name: 'SMOPage',
  computed: {
    widthRegisterButton () {
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
    return {
      resident: null,
      user_id: null,
      own_name: null,
      own_username: null,
      view_own_profile: false,
      nav_drawer: false,
      nav_group: null,
      btm_nav_bar: 'view_record',
      resident_name: '',
      unit_number: '',
      resident_address: '',
      contact_number: '',
      dialogCreateAcc: false,
      dialog_msg_header: '',
      dialog_msg: '',
      viewRes: false, //view all
      viewVisit: false, //view all
      viewEE: false, //view all
      viewSpecificRes: false, //view 1
      viewSpecificVis: false, //view 1
      allResidents: [], //load all
      residents: [], //load 10
      allVisits: [], //load all
      visits: [], //load 10
      allEE: [], //load all
      ee: [], //load 10
      load_amount_1: 10, //keep track of load
      load_amount_2: 10, //keep track of load
      load_amount_3: 10, //keep track of load
      specificRes: null, //load 1 
      specificVis: null, //load 1
    }
  },
  created() {
    let payload = getUser();
    if (payload != false) {
      this.user_id = payload.user_id;
      this.resident = payload.resident;
    }else{
      store.dispatch('auth/logout')
      .then(() => {
        alert("Session Expired. Please login again.")
        this.$router.push('/signin')
      },
      error => {
        console.log(error)
      })
    }
  },
  methods: {
    createAcc() { //create or reset account for resident
      this.$refs.createAcc.validate().then(success => {
        if (!success){
          return;
        }
        let name = this.resident_name.toUpperCase();
        let unit = this.unit_number.toUpperCase();
        let address = this.resident_address.toUpperCase();
        let hostname = window.location.hostname;
        let API_URL = `http://${hostname}:5000/smo/createacc`;
        const payload = {
          user_id: this.user_id,
          r_name: name,
          unit_number: unit,
          r_address: address,
          contact_number: this.contact_number,
        }
        axios.post(API_URL, payload, {
          headers: authHeader()
        })
        .then((res) => {
          if (res.data.authenticated == false) {
            store.dispatch('auth/logout').then(
              () => {
                alert("Session expired. Please login again.")
                this.$router.push('/signin');
              },
              error => {
                console.log(error);
              }
            ) 
          }else {
            if (res.data == "Success") {
              this.resident_name = this.unit_number = this.resident_address = this.contact_number = '';
              this.$refs.createAcc.reset();            
              this.dialog_msg_header = 'Successful'
              this.dialog_msg = "Successfully created account for resident. The username could be found under 'View Records' and the temporary password is 'Temppw123!' "
              this.dialogCreateAcc = true
            }else {
              this.resident_name = this.unit_number = this.resident_address = this.contact_number = '';
              this.$refs.createAcc.reset();  
              this.dialog_msg_header = 'Successful'
              this.dialog_msg = "Successfully reset account for resident. The username could be found under 'View Records' and the temporary password is 'Temppw123!' "
              this.dialogCreateAcc = true
            }
          }
        })
        .catch((error) => {
          alert("You are offline! Please connect to internet and try again.")
          console.log(error)
        }) 
      })
    },
    viewOwnProfile() { //view own profile
      let hostname = window.location.hostname;
      let API_URL = `http://${hostname}:5000/view_own_profile/${this.user_id}/${this.resident}`;
      axios.get(API_URL, {
        headers: authHeader()
      })
      .then((res) => {
        if (res.data.authenticated == false) {
          store.dispatch('auth/logout').then(
            () => {
              alert("Session expired. Please login again.")
              this.$router.push('/signin');
            },
            error => {
              console.log(error);
            }
          )          
        }else {
          this.own_name = res.data.s_name;
          this.own_username = res.data.s_username;
          this.nav_drawer = false;
          this.view_own_profile = true;
        }
      })
      .catch((error) => {
        alert("You are offline! Please connect to internet and try again.")
        console.log(error)
      })      
    },
    signOut() { //sign out
      store.dispatch('auth/logout')
      .then(() => {
        this.$router.push('/signin')
      },
      error => {
        console.log(error)
      })
    },
    viewRecord(record) { //select to view which records
      if (record == 1) {
        this.loadResident();
        this.viewRes = true;
        this.viewVisit = this.viewEE = false; 
      } else if (record == 2) {
        this.loadVisit();
        this.viewVisit = true;
        this.viewRes = this.viewEE = false;
      } else {
        this.loadEE();
        this.viewEE = true;
        this.viewRes = this.viewVisit = false;
      }
    },
    loadResident() { //load all resident's info
      let hostname = window.location.hostname;
      let API_URL = `http://${hostname}:5000/smo/load_resident`;
      axios.get(API_URL, {
        headers: authHeader()
      })
      .then((res) => {
        if (res.data.authenticated == false) {
          store.dispatch('auth/logout').then(
            () => {
              alert("Session expired. Please login again.")
              this.$router.push('/signin');
            },
            error => {
              console.log(error);
            }
          )          
        }else {
          this.allResidents = []
          for (let i=0;i<res.data.length;i++) {
            let concate_string1 = null;
            if (res.data[i].res_lp.length == 0) {
              concate_string1 = '';
            }
            else if (res.data[i].res_lp.length == 1) {
              concate_string1 = res.data[i].res_lp[0].trim();
            }
            else if (res.data[i].res_lp.length > 1) {
              concate_string1 = res.data[i].res_lp[0].trim();
              for (let j=0;j<(res.data[i].res_lp.length-1);j++) {
                let plate = res.data[i].res_lp[j+1].trim();
                concate_string1 = concate_string1.concat(" "+plate);
              }
            }
            let data = {
              res_id: res.data[i].res_id,
              r_unitno: res.data[i].r_unitno,
              r_name: res.data[i].r_name,
              r_contactno: res.data[i].r_contactno,
              r_username: res.data[i].r_username,
              r_secretcode: res.data[i].r_secretcode,
              r_address: res.data[i].r_address,
              res_lp: res.data[i].res_lp,
              res_lp_string: concate_string1,
              vis_lp: res.data[i].vis_lp,
              vis_bl_lp: res.data[i].vis_bl_lp
            }
            this.allResidents.push(data);
          }
          if (res.data.length < 10) {
            this.residents = []
            for (let i=0;i<res.data.length;i++) {
              this.residents.push(this.allResidents[i])
            }
            this.load_amount_1 = res.data.length;
            console.log('loadamt:', this.load_amount_1)
          } 
          else {
            this.residents = []
            for (let i=0;i<10;i++) {
              this.residents.push(this.allResidents[i])
            }
            this.load_amount_1 = 10;
            console.log('loadamt:', this.load_amount_1)
          }
        }
      })
      .catch((error) => {
        alert("You are offline! Please connect to internet and try again.")
        console.log(error)
      })  
    },
    nextPrevRecord(addAmount, record) { //next and previous button which loads 10 each time from the array
      if (record == 1) {
        if (this.allResidents.length <= 10) { //not enough records to next or previous
          return;
        } else if (addAmount == 10) {
          if (this.load_amount_1 == this.allResidents.length) { //not enough records to next or previous
            return;
          }
          let remaining = this.allResidents.length - this.load_amount_1
          if (remaining < 10) { //remaining records is lesser than 10, only load the remaining
            let starting = this.load_amount_1;
            this.load_amount_1 += remaining;
            this.residents = [];
            for (let i=starting;i<this.load_amount_1;i++) {
              this.residents.push(this.allResidents[i])
            }
          } else { //remaining records is more than 10, load 10 only
            let starting = this.load_amount_1;
            this.load_amount_1 += addAmount;
            this.residents = [];
            for (let i=starting;i<this.load_amount_1;i++) {
              this.residents.push(this.allResidents[i])
            }
          }
        } else if (addAmount == -10) { //previous record
          let starting = this.load_amount_1 - this.residents.length - 10;
          if (this.load_amount_1 <= 10){ //less than 10 then could not go previous
            return;
          }
          else { //go to previous 10 records
            this.load_amount_1 = this.load_amount_1 - this.residents.length;
            this.residents = [];
            for (let i=starting;i<this.load_amount_1;i++) {
              this.residents.push(this.allResidents[i])
            }
          } 
        }
      } else if (record == 2) {
        if (this.allVisits.length <= 10) {
          return;
        } else if (addAmount == 10) {
          if (this.load_amount_2 == this.allVisits.length) {
            return;
          }
          let remaining = this.allVisits.length = this.load_amount_2
          if (remaining < 10) {
            let starting = this.load_amount_2;
            this.load_amount_2 += remaining;
            this.visits = [];
            for (let i=starting;i<this.load_amount_2;i++) {
              this.visits.push(this.allVisits[i])
            }
          } else {
            let starting = this.load_amount_2;
            this.load_amount_2 += addAmount;
            this.visits = [];
            for (let i=starting;i<this.load_amount_2;i++) {
              this.visits.push(this.allVisits[i])
            }
          }
        } else if (addAmount == -10) {
          let starting = this.load_amount_2 - this.visits.length - 10;
          if (this.load_amount_2 <= 10){
            return;
          }
          else {
            this.load_amount_2 = this.load_amount_2 - this.visits.length;
            this.visits = [];
            for (let i=starting;i<this.load_amount_2;i++) {
              this.visits.push(this.allVisits[i])
            }
          } 
        }
      } else if (record == 3) {
        if (this.allEE.length <= 10) {
          return;
        } else if (addAmount == 10) {
          if (this.load_amount_3 == this.allEE.length) {
            return;
          }
          let remaining = this.allEE.length - this.load_amount_3
          if (remaining < 10) {
            let starting = this.load_amount_3;
            this.load_amount_3 += remaining;
            this.ee = [];
            for (let i=starting;i<this.load_amount_3;i++) {
              this.ee.push(this.allEE[i])
            }
          } else {
            let starting = this.load_amount_3;
            this.load_amount_3 += addAmount;
            this.ee = [];
            for (let i=starting;i<this.load_amount_3;i++) {
              this.ee.push(this.allEE[i])
            }
          }
        } else if (addAmount == -10) {
          let starting = this.load_amount_3 - this.ee.length - 10;
          if (this.load_amount_3 <= 10){
            return;
          }
          else {
            this.load_amount_3 = this.load_amount_3 - this.ee.length;
            this.ee = [];
            for (let i=starting;i<this.load_amount_3;i++) {
              this.ee.push(this.allEE[i])
            }
          } 
        }
      }
    },
    viewSpecificR(resident) { //click on a specific record to view in details
      this.viewSpecificRes = true;
      
      let concate_string1 = null;
      if (resident.res_lp.length == 0) {
        concate_string1 = 'None';
      }
      else if (resident.res_lp.length == 1) {
        concate_string1 = resident.res_lp[0].trim();
      }
      else if (resident.res_lp.length > 1) {
        concate_string1 = resident.res_lp[0].trim();
        for (let i=0;i<(resident.res_lp.length-1);i++) {
          let plate = resident.res_lp[i+1].trim();
          concate_string1 = concate_string1.concat(", "+plate);
        }
      }

      let concate_string2 = null;
      if (resident.vis_lp.length == 0) {
        concate_string2 = 'None';
      }
      else if (resident.vis_lp.length == 1) {
        concate_string2 = resident.vis_lp[0].trim();
      }
      else if (resident.vis_lp.length > 1) {
        concate_string2 = resident.vis_lp[0].trim();
        for (let i=0;i<(resident.vis_lp.length-1);i++) {
          let plate = resident.vis_lp[i+1].trim();
          concate_string2 = concate_string2.concat(", "+plate);
        }
      }

      let concate_string3 = null;
      if (resident.vis_bl_lp.length == 0) {
        concate_string3 = 'None';
      }
      else if (resident.vis_bl_lp.length == 1) {
        concate_string3 = resident.vis_bl_lp[0].trim();
      }
      else if (resident.vis_bl_lp.length > 1) {
        concate_string3 = resident.vis_bl_lp[0].trim();
        for (let i=0;i<(resident.vis_bl_lp.length-1);i++) {
          let plate = resident.vis_bl_lp[i+1].trim();
          concate_string3 = concate_string3.concat(", "+plate);
        }
      }
      this.specificRes = {
        unitno: resident.r_unitno,
        name: resident.r_name,
        contactno: resident.r_contactno,
        username: resident.r_username,
        secretcode: resident.r_secretcode,
        address: resident.r_address,
        res_lp: concate_string1,
        vis_lp: concate_string2,
        vis_bl_lp: concate_string3
      }
    },
    loadVisit() { //load all visits
      let hostname = window.location.hostname;
      let API_URL = `http://${hostname}:5000/smo/load_visit`;
      axios.get(API_URL, {
        headers: authHeader()
      })
      .then((res) => {
        if (res.data.authenticated == false) {
          store.dispatch('auth/logout').then(
            () => {
              alert("Session expired. Please login again.")
              this.$router.push('/signin');
            },
            error => {
              console.log(error);
            }
          )          
        }else {
          this.allVisits = []
          for (let i=0;i<res.data.length;i++) {
            let data = {
              visit_id: res.data[i].visit_id,
              plate_number: res.data[i].plate_number,
              visit_on: res.data[i].visit_on,
              r_name: res.data[i].r_name,
              r_unitno: res.data[i].r_unitno,
              v_name: res.data[i].v_name,
              v_contactno: res.data[i].v_contactno,
              visit_purpose: res.data[i].visit_purpose,
              visit_status: res.data[i].visit_status
            }
            this.allVisits.push(data);
          }
          if (res.data.length < 10) {
            this.visits = []
            for (let i=0;i<res.data.length;i++) {
              this.visits.push(this.allVisits[i])
            }
            this.load_amount_2 = res.data.length;
            console.log('loadamt:', this.load_amount_2)
          }else {
            this.visits = []
            for (let i=0;i<10;i++) {
              this.visits.push(this.allVisits[i])
            }
            this.load_amount_2 = 10;
            console.log('loadamt:', this.load_amount_2)
          }
        }
      })
      .catch((error) => {
        alert("You are offline! Please connect to internet and try again.")
        console.log(error)
      })  
    },
    viewSpecificV(visit) { //click on specific record to view in details
      this.viewSpecificVis = true;
      this.specificVis = {
        plate_number: visit.plate_number,
        visit_on: visit.visit_on,
        visit_purpose: visit.visit_purpose,
        r_unitno: visit.r_unitno,
        r_name: visit.r_name,
        v_name: visit.v_name,
        v_contactno: visit.v_contactno,
        visit_status: visit.visit_status
      }
    },
    loadEE() { //load all vehicle's entry and exit records
      let hostname = window.location.hostname;
      let API_URL = `http://${hostname}:5000/smo/load_ee`;
      axios.get(API_URL, {
        headers: authHeader()
      })
      .then((res) => {
        if (res.data.authenticated == false) {
          store.dispatch('auth/logout').then(
            () => {
              alert("Session expired. Please login again.")
              this.$router.push('/signin');
            },
            error => {
              console.log(error);
            }
          )          
        }else {
          this.allEE = []
          for (let i=0;i<res.data.length;i++) {
            let data = {
              ee_id: res.data[i].ee_id,
              plate_number: res.data[i].plate_number,
              ee_entryon: res.data[i].ee_entryon,
              ee_exiton: res.data[i].ee_exiton,
              name: res.data[i].name,
              contactno: res.data[i].contactno,
            }
            this.allEE.push(data);
          }
          if (res.data.length < 10) {
            this.ee = []
            for (let i=0;i<res.data.length;i++) {
              this.ee.push(this.allEE[i])
            }
            this.load_amount_3 = res.data.length;
            console.log('loadamt:', this.load_amount_3)
          }else {
            this.ee = []
            for (let i=0;i<10;i++) {
              this.ee.push(this.allEE[i])
            }
            this.load_amount_2 = 10;
            console.log('loadamt:', this.load_amount_2)
          }
        }
      })
      .catch((error) => {
        alert("You are offline! Please connect to internet and try again.")
        console.log(error)
      })  
    },
  },
  components: {
    ValidationProvider,
    ValidationObserver    
  }
}
</script>