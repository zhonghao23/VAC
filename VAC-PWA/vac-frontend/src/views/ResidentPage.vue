<!--
Programmer Name:    CHIAM ZHONG HAO
Program Name:       views/ResidentPage.vue
Description:        It is the resident page of VAC. It provides all the functions for the residents in this page.
First Written On:   01/01/2021
Edited On:          04/03/2021
-->
<template>
  <v-container fluid class="px-1">
    <!-- APP BAR -->
    <v-app-bar fixed app dense flat color="teal darken-1">
      <v-app-bar-nav-icon @click="nav_drawer = true" color="white"></v-app-bar-nav-icon>
      <v-toolbar-title v-if="btm_nav_bar == 'manage_lp' && view_own_profile == false && change_password == false" class="white--text">Manage License Plates</v-toolbar-title>
      <v-toolbar-title v-else-if="btm_nav_bar == 'access_request' && view_own_profile == false && change_password == false" class="white--text">Review Access Request</v-toolbar-title>
      <v-toolbar-title v-else-if="btm_nav_bar == 'manage_lp' && view_own_profile == false && change_password == true" class="white--text">Change Password</v-toolbar-title>
      <v-toolbar-title v-else-if="btm_nav_bar == 'access_request' && view_own_profile == false && change_password == true" class="white--text">Change Password</v-toolbar-title>
      <v-toolbar-title v-else-if="btm_nav_bar == 'manage_lp' && view_own_profile == true && change_password == false" class="white--text">View Profile</v-toolbar-title>
      <v-toolbar-title v-else-if="btm_nav_bar == 'access_request' && view_own_profile == true && change_password == false" class="white--text">View Profile</v-toolbar-title>
    </v-app-bar>
    <!-- NAVIGATION DRAWER -->
    <v-navigation-drawer v-model="nav_drawer" fixed temporary class="teal lighten-5" style="max-width:250px">
      <v-list nav dense>
        <v-list-item-group v-model="nav_group" class="teal lighten-5" active-class="teal-text text--accent-4">
          <v-list-item @click="viewOwnProfile()">
            <v-list-item-icon>
              <v-icon>mdi-account-circle</v-icon>
            </v-list-item-icon>
            <v-list-item-title class="body-1 teal--text text--darken-4">VIEW PROFILE</v-list-item-title>
          </v-list-item>
          <v-list-item @click="change_password = true, nav_drawer = false">
            <v-list-item-icon>
              <v-icon>mdi-lock-reset</v-icon>
            </v-list-item-icon>
            <v-list-item-title class="body-1 teal--text text--darken-4">CHANGE PASSWORD</v-list-item-title>
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
    <!-- MANAGE LICENSE PLATES -->
    <v-container v-if="btm_nav_bar == 'manage_lp' && add_lp == false && view_own_profile == false && change_password == false ">
      <!-- BUTTON TO LOAD ALL LICENSE PLATES -->
      <v-row align="center" justify="center">
        <v-col cols="12">
          <v-btn @click="loadLicensePlate()" block elevation="0" class="teal lighten-5">REFRESH</v-btn>
        </v-col>
      </v-row>
      <!-- SHOW ALL LICENSE PLATES -->
      <v-row v-if="manage_lp == true" align="center" justify="center">
        <v-col v-if="empty_record1 == true" cols="12" align="center">
          <h4 class="font-weight-black ">NO RECORD</h4>
        </v-col>
        <v-container v-for="info in allLP" :key="info.plate_number" class="pb-0">
          <v-row dense>
            <v-col cols="12">
              <v-card color="#385F73" dark>
                <v-card-title class="overline pt-0 pb-0">
                  {{ info.plate_number }}
                  <v-spacer></v-spacer>
                  <v-card-actions class="pr-0 mr-n2">
                    <v-btn @click="dialogRemoveLP(info)" icon>
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-card-title>
                <v-card-title v-if="info.identity == 'visitor'" class="overline pt-0 pb-0">Visitor: {{ info.v_name }}</v-card-title>
                <v-card-subtitle v-if="info.identity == 'visitor'" class="overline pb-0">{{ info.v_contactno }}</v-card-subtitle>
                <v-card-title v-if="info.lp_status == 'WHITELIST'" class="overline font-italic font-weight-black light-green--text text--accent-3 pt-0 pb-0">ACCESS GRANTED</v-card-title>
                <v-card-title v-else-if="info.lp_status == 'BLACKLIST'" class="overline font-italic font-weight-black deep-orange--text text--lighten-2 pt-0 pb-0">ACCESS DENIED</v-card-title>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
        <!-- DIALOG CONFIRM DELETE -->
        <v-dialog v-model="dialogRemovePlate" max-width="400">
          <v-card>
            <v-card-title class="teal lighten-2">
              CONFIRMATION
            </v-card-title>
            <v-card-text class="subtitle-1 font-weight-bold mt-2">
              Do you wish to delete the license plate?
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click="dialogRemovePlate = false" text color="primary">
                CANCEL
              </v-btn>
              <v-btn @click="removeLP()" text color="primary">
                CONFIRM
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
      <!-- ADD LP BUTTON -->
      <v-btn @click="add_lp = true" bottom right absolute fab dark color="green lighten-1" class="mb-12 mr-3">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-container>
    <!-- REVIEW ACCESS REQUEST -->
    <v-container v-if="btm_nav_bar == 'access_request' && add_lp == false && view_own_profile == false && change_password == false">
      <!-- BUTTON TO LOAD ALL LICENSE PLATES -->
      <v-row align="center" justify="center">
        <v-col cols="12">
          <v-btn @click="loadAccessRequest()" block elevation="0" class="teal lighten-5">REFRESH</v-btn>
        </v-col>
      </v-row>
      <!-- SHOW ALL ACCESS REQUEST -->
      <v-row v-if="review_request == true" align="center" justify="center">
        <v-col v-if="empty_record2 == true" cols="12" align="center">
          <h4 class="font-weight-black ">NO REQUEST</h4>
        </v-col>
        <v-container v-for="request in allRequest" :key="request.visit_id" class="pb-0">
          <v-row dense>
            <v-col cols="12">
              <v-card color="#385F73" dark>
                <v-card-title class="overline pt-0 pb-0">
                  {{ request.plate_number }}
                  <v-spacer></v-spacer>
                  <!-- APPROVE BUTTON -->
                  <v-card-actions v-if="request.visit_status == 'PENDING'" class="pr-0 mr-n2">
                    <v-btn @click="dialogApproveRequest(request)" icon>
                      <v-icon>mdi-eye-check</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-card-title>
                <v-card-title class="overline pt-0 pb-0">Visit On:{{ request.visit_on }}</v-card-title>
                <v-card-subtitle class="overline pb-0">{{ request.visit_purpose }}</v-card-subtitle>
                <v-card-title class="overline pt-0 pb-0">Visitor: {{ request.v_name }}</v-card-title>
                <v-card-subtitle class="overline pb-0">{{ request.v_contactno }}</v-card-subtitle>
                <v-card-title v-if="request.visit_status == 'APPROVED'" class="overline font-italic font-weight-black light-green--text text--accent-3 pt-0 pb-0">{{ request.visit_status }}</v-card-title>
                <v-card-title v-else class="overline font-italic font-weight-black light-blue--text text--lighten-3 pt-0 pb-0">{{ request.visit_status }}</v-card-title>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-row>
    </v-container>
    <!-- CONFIRM MESSAGE -->
    <v-dialog v-model="dialogRequest" max-width="400">
      <v-card>
        <v-card-title class="teal lighten-2">
          CONFIRMATION
        </v-card-title>
        <v-card-text class="subtitle-1 font-weight-bold mt-2">
          YOU CAN APPROVE OR REJECT THE ACCESS REQUEST
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialogRequest = false" text color="primary">
            CANCEL
          </v-btn>
          <v-btn @click="decideRequest('reject')" text color="red lighten-1">
            REJECT
          </v-btn>
          <v-btn @click="decideRequest('approve')" text color="green lighten-1">
            APPROVE
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- ADD LICENSE PLATE -->
    <v-container v-if="add_lp == true">
      <v-row align="start" justify="start">
        <v-col align="start" cols="2" sm="1" class="pb-0">
          <v-icon @click="cancelAddLP()" x-large>mdi-arrow-left-circle</v-icon>
        </v-col>
      </v-row>
      <v-row align="center" justify="center">
        <v-col align="center" cols="12">
          <h2>License Plate Registration</h2>
        </v-col>
      </v-row>
      <v-row align="center" justify="center">
        <v-radio-group v-model="identity" row mandatory>
          <v-radio
            label="Own Registration"
            value="resident"
            color="teal accent-4"
            class="font-weight-black"
          ></v-radio>
          <v-radio
            label="Visitor"
            value="visitor"
            color="teal accent-4"
            class="font-weight-black"
          ></v-radio>
        </v-radio-group>
      </v-row>
      <!-- FORM FOR RESIDENT OWN REGISTRATION -->
      <ValidationObserver v-if="identity == 'resident'" ref="registerResLP">
        <form>
          <v-row align="center" justify="center">
            <!-- LICENSE PLATE NUMBER -->
            <v-col cols="12" sm="6" lg="4">
              <ValidationProvider name="PlateNumber" rules="required|alpha_num" v-slot="{ errors }">
                <v-text-field 
                  v-model="plate_number1"
                  label="License Plate Number"
                  outlined rounded dense clearable hide-details
                  color="teal darken-3"
                  placeholder="WB7638C"
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
            <!-- CONFIRM BUTTON -->
            <v-col cols="12" align="center" justify="center">
              <v-btn @click="addResLP()" depressed :width="widthConfirmButton" class="teal lighten-2">CONFIRM</v-btn>
            </v-col>
          </v-row>
        </form>
      </ValidationObserver>
      <!-- FORM FOR VISITOR LP REGISTRATION -->
      <ValidationObserver v-if="identity == 'visitor'" ref="registerVisLP">
        <form>
          <v-row align="center" justify="center">
            <!-- LICENSE PLATE NUMBER -->
            <v-col cols="12">
              <ValidationProvider name="PlateNumber" rules="required|alpha_num" v-slot="{ errors }">
                <v-text-field 
                  v-model="plate_number2"
                  label="License Plate Number"
                  outlined rounded dense clearable hide-details
                  color="teal darken-3"
                  placeholder="WB7638C"
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
            <!-- NAME -->
            <v-col cols="12">
              <ValidationProvider name="VisitorName" rules="required|alpha_spaces" v-slot="{ errors }">
                <v-text-field 
                  v-model="visitor_name"
                  label="Visitor's Name"
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
            <!-- BLACKLIST CHECKBOX -->
            <v-checkbox v-model="blacklist" label="Blacklist" color="teal accent-4" class="font-weight-black"></v-checkbox>
            <!-- CONFIRM BUTTON -->
            <v-col cols="12" align="center" justify="center">
              <v-btn @click="addVisLP()" depressed :width="widthConfirmButton" class="teal lighten-2">CONFIRM</v-btn>
            </v-col>
          </v-row>
        </form>
      </ValidationObserver>
    </v-container>
    <!-- POP UP MESSAGE -->
    <v-dialog v-model="dialogRegisterLP" max-width="400">
      <v-card>
        <v-card-title class="teal lighten-2">
          {{ dialog_msg_header2 }}
        </v-card-title>
        <v-card-text class="subtitle-1 font-weight-bold mt-2">
          {{ dialog_msg2 }}
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialogRegisterLP = false" text color="primary">
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
              <v-card-title class="overline pb-0 justify-center">UNIT<br>{{ own_profile.unitno }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">NAME<br>{{ own_profile.name }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">CONTACT NO<br>{{ own_profile.contactno }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">USERNAME<br>{{ own_profile.username }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">SECRET CODE<br>{{ own_profile.secretcode }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">ADDRESS<br>{{ own_profile.address }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">LICENSE PLATES (R)<br>{{ own_profile.res_lp }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">LICENSE PLATES (V)<br>{{ own_profile.vis_lp }}</v-card-title>
              <v-card-title class="overline pb-0 justify-center">LICENSE PLATES (BL)<br>{{ own_profile.vis_bl_lp }}</v-card-title>
            </v-card>
          </v-col>
        </v-row>
      </v-container> 
    </v-container>
    <!-- CHANGE PASSWORD -->
    <v-container v-if="change_password == true">
      <v-row align="start" justify="start">
        <v-col align="start" cols="2" sm="1" class="pb-0">
          <v-icon @click="cancelChangePassword()" x-large>mdi-arrow-left-circle</v-icon>
        </v-col>
      </v-row>
      <v-row align="center" justify="center">
        <v-col align="center" cols="12">
          <h2>Change Password</h2>
        </v-col>
      </v-row>
      <ValidationObserver ref="changePassword">
        <form>
          <v-row align="center" justify="center">
            <!-- OLD PASSWORD -->
            <v-col cols="12">
              <ValidationProvider name="OldPassword" rules="required|customPassword" v-slot="{ errors }">
                <v-text-field 
                  v-model="old_password"
                  label="Current Password"
                  :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="show1 ? 'text' : 'password'"
                  @click:append="show1 = !show1"
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
            <!-- NEW PASSWORD -->
            <v-col cols="12">
              <ValidationProvider name="NewPassword" rules="required|customPassword" v-slot="{ errors }">
                <v-text-field 
                  v-model="new_password"
                  label="New Password"
                  :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="show2 ? 'text' : 'password'"
                  @click:append="show2 = !show2"
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
            <!-- CONFIRM NEW PASSWORD -->
            <v-col cols="12">
              <ValidationProvider name="ConfirmNewPassword" rules="required|customPassword" v-slot="{ errors }">
                <v-text-field 
                  v-model="confirm_password"
                  label="Confirm New Password"
                  :append-icon="show3 ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="show3 ? 'text' : 'password'"
                  @click:append="show3 = !show3"
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
            <!-- CONFIRM BUTTON -->
            <v-col cols="12" align="center" justify="center">
              <v-btn @click="changePassword()" depressed :width="widthConfirmButton" class="teal lighten-2">CONFIRM</v-btn>
            </v-col>
          </v-row>
        </form>
      </ValidationObserver>
    </v-container>
    <!-- POP UP MESSAGE -->
    <v-dialog v-model="dialogChangePassword" max-width="400">
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
          <v-btn @click="dialogChangePassword = false" text color="primary">
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- BOTTOM NAVIGATION BAR -->
    <v-bottom-navigation fixed app grow mandatory shift dark v-model="btm_nav_bar" background-color="teal darken-2">
      <v-btn value="manage_lp">
        <span>Manage License Plates</span>
        <v-icon>mdi-car-multiple</v-icon>
      </v-btn>
      <v-btn value="access_request">
        <span>Review Access Request</span>
        <v-icon>mdi-badge-account-horizontal</v-icon>
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
  name: 'ResidentPage',
  computed: {
    widthConfirmButton () {
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
      view_own_profile: false,
      change_password: false,
      add_lp: false,
      nav_drawer: false,
      nav_group: null,
      btm_nav_bar: 'manage_lp',
      own_profile: null,
      show1: false,
      show2: false,
      show3: false,
      old_password: '',
      new_password: '',
      confirm_password: '',
      dialogChangePassword: false,
      dialog_msg: '',
      dialog_msg_header: '',
      dialogRegisterLP: false,
      dialog_msg2: '',
      dialog_msg_header2: '',
      manage_lp: false,
      allLP: [],
      dialogRemovePlate: false,
      to_be_deleted: null,
      empty_record1: true,
      empty_record2: true,
      identity: 'resident',
      plate_number1: '',
      plate_number2: '',
      visitor_name: '',
      contact_number: '',
      blacklist: false,
      review_request: false,
      allRequest: [],
      dialogRequest: false,
      to_be_review: null,
    }
  },
  created() {
    let payload = getUser(); //get user id and identity read from JWT stored in local storage
    if (payload != false) {
      this.user_id = payload.user_id;
      this.resident = payload.resident;
      this.loadLicensePlate();
      this.loadAccessRequest();
    }else{ //logout user if the JWT is not valid or expired
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
    signOut() { //sign out function
      store.dispatch('auth/logout')
      .then(() => {
        this.$router.push('/signin')
      },
      error => {
        console.log(error)
      })
    },
    viewOwnProfile() { //view own resident's profile
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
          //check how many license plates has returned, and concate them
          let concate_string1 = null;
          if (res.data.res_lp.length == 0) {
            concate_string1 = 'None';
          }else if (res.data.res_lp.length == 1) {
            concate_string1 = res.data.res_lp[0].trim();
          }else if (res.data.res_lp.length > 1) {
            concate_string1 = res.data.res_lp[0].trim();
            for (let i=0;i<(res.data.res_lp.length-1);i++) {
              let plate = res.data.res_lp[i+1].trim();
              concate_string1 = concate_string1.concat(", "+plate);
            }
          }
          //check how many license plates has returned, and concate them
          let concate_string2 = null;
          if (res.data.vis_lp.length == 0) {
            concate_string2 = 'None';
          }
          else if (res.data.vis_lp.length == 1) {
            concate_string2 = res.data.vis_lp[0].trim();
          }
          else if (res.data.vis_lp.length > 1) {
            concate_string2 = res.data.vis_lp[0].trim();
            for (let i=0;i<(res.data.vis_lp.length-1);i++) {
              let plate = res.data.vis_lp[i+1].trim();
              concate_string2 = concate_string2.concat(", "+plate);
            }
          }
          //check how many license plates has returned, and concate them
          let concate_string3 = null;
          if (res.data.vis_bl_lp.length == 0) {
            concate_string3 = 'None';
          }
          else if (res.data.vis_bl_lp.length == 1) {
            concate_string3 = res.data.vis_bl_lp[0].trim();
          }
          else if (res.data.vis_bl_lp.length > 1) {
            concate_string3 = res.data.vis_bl_lp[0].trim();
            for (let i=0;i<(res.data.vis_bl_lp.length-1);i++) {
              let plate = res.data.vis_bl_lp[i+1].trim();
              concate_string3 = concate_string3.concat(", "+plate);
            }
          }
          this.own_profile = {
            unitno: res.data.r_unitno,
            name: res.data.r_name,
            contactno: res.data.r_contactno,
            username: res.data.r_username,
            secretcode: res.data.r_secretcode,
            address: res.data.r_address,
            res_lp: concate_string1,
            vis_lp: concate_string2,
            vis_bl_lp: concate_string3
          }
          this.nav_drawer = false;
          this.view_own_profile = true;
        }
      })
      .catch((error) => {
        alert("You are offline! Please connect to internet and try again.")
        console.log(error)
      })     
    },
    changePassword() { //change password
      this.$refs.changePassword.validate().then(success => {
        if (!success) {
          return;
        }
        //verify if the confirm new password matches
        if (this.new_password != this.confirm_password) {
          this.dialog_msg_header = "Unsuccessful"
          this.dialog_msg = "The new password and confirm new password does not match"
          this.dialogChangePassword = true;
        }
        else if (this.old_password == this.new_password) {
          this.dialog_msg_header = "Unsuccessful"
          this.dialog_msg = "The new password cannot be the same with the old password"
          this.dialogChangePassword = true;
        } else {
          let hostname = window.location.hostname;
          let API_URL = `http://${hostname}:5000/resident/change_password`;
          const payload = {
            user_id: this.user_id,
            old_password: this.old_password,
            new_password: this.new_password
          }
          axios.put(API_URL, payload, {
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
              if (res.data == 'FAIL') {
                this.dialog_msg_header = "Unsuccessful"
                this.dialog_msg = "The old password is incorrect"
                this.dialogChangePassword = true;
              }else if (res.data == 'SUCCESS') {
                this.dialog_msg_header = "Successful"
                this.dialog_msg = "The new password has been updated"
                this.dialogChangePassword = true;
                this.cancelChangePassword();
              }
            }
          })
          .catch((error) => {
            alert("You are offline! Please connect to internet and try again.")
            console.log(error)
          })
        }
      })        
    },
    cancelChangePassword() { //back to main page
      this.change_password = false;
      this.old_password = ''; 
      this.new_password = '';
      this.confirm_password = '';
    },
    loadLicensePlate() { //load all the license plates registered by the resident
      let hostname = window.location.hostname;
      let API_URL = `http://${hostname}:5000/resident/load_lp/${this.user_id}`;
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
          this.allLP = []
          for (let i=0;i<res.data.length;i++) {
            let data = {
              plate_number: res.data[i].plate_number,
              identity: res.data[i].identity,
              v_name: res.data[i].v_name,
              v_contactno: res.data[i].v_contactno,
              lp_status: res.data[i].lp_status
            }
            this.allLP.push(data);
          }
          if (this.allLP.length == 0) {
            this.empty_record1 = true;
          }else {
            this.empty_record1 = false;
          }
          this.manage_lp = true;
        }
      })
      .catch((error) => {
        console.log(error)
      })
    },
    dialogRemoveLP(info) {
      this.dialogRemovePlate = true;
      this.to_be_deleted = info;
    },
    removeLP() { //remove license plates registered
      let hostname = window.location.hostname;
      let API_URL = `http://${hostname}:5000/resident/remove_lp`;
      const payload = {
        user_id: this.user_id,
        plate_number: this.to_be_deleted.plate_number,
      }
      axios.put(API_URL, payload, {
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
          if (res.data == 'SUCCESS') {
            this.loadLicensePlate();
            this.dialogRemovePlate = false;
          }
        }
      })
      .catch((error) => {
        alert("You are offline! Please connect to internet and try again.")
        console.log(error)
      })
    },
    cancelAddLP() { //back to main page
      this.add_lp = false;
      this.plate_number1 = this.plate_number2 = this.visitor_name = this.contact_number = '';
    },
    addResLP() { //register own license plate
      this.$refs.registerResLP.validate().then(success => 
      {
        if (!success) {
          return;
        }
        let plate = this.plate_number1.toUpperCase();
        let hostname = window.location.hostname;
        let API_URL = `http://${hostname}:5000/resident/add_res_lp`;   
        const payload = {
          plate_number: plate,
          user_id: this.user_id
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
            if (res.data == '1') {
              this.dialog_msg_header2 = 'Unsuccessful'
              this.dialog_msg2 = 'The license plate is blacklisted by another user. Please find SMO for assistance'
              this.dialogRegisterLP = true
            }else if (res.data == '2') {
              this.dialog_msg_header2 = 'Unsuccessful'
              this.dialog_msg2 = 'The license plate is registered by another user. Please find SMO for assistance'
              this.dialogRegisterLP = true
            }else{ //SUCCESS
              this.dialog_msg_header2 = 'Successful'
              this.dialog_msg2 = 'The license plate is registered.'
              this.dialogRegisterLP = true
              this.cancelAddLP();
              this.$refs.registerResLP.reset();
              this.loadLicensePlate();          
            }
          }
        })
        .catch((error) => {
          alert("You are offline! Please connect to internet and try again.")
          console.log(error)
        })
      })
    },
    addVisLP() { //register visitor's license plate
      this.$refs.registerVisLP.validate().then(success => 
      {
        if (!success) {
          return;
        }
        let plate = this.plate_number2.toUpperCase();
        let name = this.visitor_name.toUpperCase();
        let hostname = window.location.hostname;
        let API_URL = `http://${hostname}:5000/resident/add_vis_lp`;   
        const payload = {
          plate_number: plate,
          user_id: this.user_id,
          v_name: name,
          v_contactno: this.contact_number,
          blacklist: this.blacklist
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
            if (res.data == '1') {
              this.dialog_msg_header2 = 'Unsuccessful'
              this.dialog_msg2 = 'The license plate is blacklisted by another user. Please find SMO for assistance'
              this.dialogRegisterLP = true
            }else if (res.data == '2') {
              this.dialog_msg_header2 = 'Unsuccessful'
              this.dialog_msg2 = 'The license plate is registered by another user. Please find SMO for assistance'
              this.dialogRegisterLP = true
            }else{ //SUCCESS
              this.dialog_msg_header2 = 'Successful'
              this.dialog_msg2 = 'The license plate is registered.'
              this.dialogRegisterLP = true
              this.cancelAddLP();
              this.$refs.registerVisLP.reset(); 
              this.loadLicensePlate();             
            }
          }
        })
        .catch((error) => {
          alert("You are offline! Please connect to internet and try again.")
          console.log(error)
        })
      })
    },
    loadAccessRequest() { //load all the access requests of the resident
      let hostname = window.location.hostname;
      let API_URL = `http://${hostname}:5000/resident/load_access_request/${this.user_id}`;
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
          this.allRequest = []
          for (let i=0;i<res.data.length;i++) {
            let data = {
              visit_id: res.data[i].visit_id,
              plate_number: res.data[i].plate_number,
              visit_on: res.data[i].visit_on,
              visit_purpose: res.data[i].visit_purpose,
              visit_status: res.data[i].visit_status,
              v_name: res.data[i].v_name,
              v_contactno: res.data[i].v_contactno,
            }
            this.allRequest.push(data);
          }
          if (this.allRequest.length == 0) {
            this.empty_record2 = true;
          }else {
            this.empty_record2 = false;
          }
          this.review_request = true;
        }
      })
      .catch((error) => {
        console.log(error)
      })
    },
    dialogApproveRequest(request) { //dialog
      this.dialogRequest = true;
      this.to_be_review = request;
    },
    decideRequest(decision) { //approve/reject access request
      console.log(this.to_be_review.plate_number)
      let hostname = window.location.hostname;
      let API_URL = `http://${hostname}:5000/resident/decide_request`;
      const payload = {
        user_id: this.user_id,
        visit_id: this.to_be_review.visit_id,
        decision: decision
      }
      axios.put(API_URL, payload, {
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
          if (res.data == 'SUCCESS') {
            this.loadAccessRequest();
            this.dialogRequest = false;
          }
        }
      })
      .catch((error) => {
        alert("You are offline! Please connect to internet and try again.")
        console.log(error)
      })
    }
  },
  components: {
    ValidationProvider,
    ValidationObserver
  }
}
</script>