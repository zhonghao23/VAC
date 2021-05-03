<!--
Programmer Name:    CHIAM ZHONG HAO
Program Name:       views/VisitorPage.vue
Description:        It is the visitor page of VAC. It provides all the functions for the visitor in this page.
First Written On:   01/01/2021
Edited On:          04/03/2021
-->
<template>
  <v-container fill-height fluid class="teal lighten-5 pa-0">
<!-- LICENSE PLATE REGISTRATION -->
    <v-container v-if="btm_nav_bar == 'register_lp'">
      <!-- MAIN TITLE -->
      <v-row align="center" justify="center">
        <v-col align="start" cols="2" sm="1">
          <v-icon x-large @click="goToLanding()">mdi-arrow-left-circle</v-icon>
        </v-col>
        <v-col align="start" cols="10" sm="11">
          <h2>License Plate Registration</h2>
        </v-col>
      </v-row>
      <!-- INPUT FORM -->
      <ValidationObserver ref="registerLP">
        <form>
          <v-row align="center" justify="center">
            <!-- LICENSE PLATE NUMBER -->
            <v-col cols="12" sm="6" lg="4">
              <ValidationProvider name="PlateNumber" rules="required|alpha_num" v-slot="{ errors }">
                <v-text-field 
                  v-model="plate_number"
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
            <!-- HOUSE UNIT NUMBER -->
            <v-col cols="12" sm="6" lg="4">
              <ValidationProvider name="UnitNumber" rules="required|alpha_num" v-slot="{ errors }">
                <v-text-field 
                  v-model="unit_number"
                  label="House Unit Number (Visiting)"
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
            <!-- CONTACT NUMBER -->
            <v-col cols="12" sm="6" lg="4">
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
            <!-- VISITOR'S NAME -->
            <v-col cols="12" sm="6" lg="4">
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
            <!-- PURPOSE OF VISITING -->
            <v-col cols="12" lg="8">
              <ValidationProvider name="VisitPurpose" rules="required" v-slot="{ errors }">
                <v-textarea 
                  v-model="visit_purpose"
                  label="Purpose of Visitng"
                  outlined rounded dense clearable hide-details auto-grow rows="2"
                  color="teal darken-3"
                  placeholder="Barbeque party"
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
            <!-- DATE OF VISITING -->
            <v-col cols="12" sm="6" lg="4">
              <v-dialog
                ref="dialog_date"
                v-model="date_picker"
                :return-value.sync="visit_date"
                persistent
                width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <ValidationProvider name="VisitDate" rules="required" v-slot="{ errors }">
                    <v-text-field
                      v-model="visit_date"
                      label="Date of Visiting"
                      prepend-icon="mdi-calendar"
                      readonly outlined rounded dense clearable hide-details
                      color="teal darken-3"
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                    <ul class="text-left teal--text teal--darken-4 caption font-italic font-weight-bold">
                      <li v-for="(error, index) in errors" :key="index">
                        <span>{{ error }}</span>
                      </li>
                    </ul>
                  </ValidationProvider> 
                </template>
                <v-date-picker
                  v-model="visit_date"
                  scrollable
                  :min="new Date().toISOString().substr(0, 10)"
                  :max="endDate()"
                  color="teal darken-3"
                >
                  <v-spacer></v-spacer>
                  <v-btn
                    text
                    color="primary"
                    @click="date_picker = false"
                  >
                    Cancel
                  </v-btn>
                  <v-btn
                    text
                    color="primary"
                    @click="pickDate()"
                  >
                    OK
                  </v-btn>
                </v-date-picker>
              </v-dialog> 
            </v-col>            
            <!-- SECRET CODE -->
            <v-col cols="12" sm="6" lg="4">
              <ValidationProvider name="SecretCode" rules="required|digits:6" v-slot="{ errors }">
                <v-text-field 
                  v-model="secret_code"
                  label="Secret Code (Get from Resident)"
                  outlined rounded dense clearable hide-details
                  color="teal darken-3"
                  placeholder="123456"
                  autocomplete="off"
                  maxlength="6"
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
              <v-btn @click="register()" depressed :width="widthRegisterButton" class="teal lighten-2">REGISTER</v-btn>
            </v-col>
          </v-row>
        </form>
      </ValidationObserver>
      <!-- POP UP MESSAGE -->
      <v-dialog v-model="dialogRegisterLP" max-width="400">
        <v-card>
          <v-card-title class="teal lighten-2">
            {{ dialog_msg_header}}
          </v-card-title>
          <v-card-text class="subtitle-1 font-weight-bold mt-2">
            {{ dialog_msg }}
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
    </v-container>
<!-- CHECK APPROVAL STATUS -->
    <v-container v-else-if="btm_nav_bar == 'check_status'">
      <!-- MAIN TITLE -->
      <v-row align="center" justify="center">
        <v-col align="start" cols="2" sm="1">
          <v-icon x-large @click="goToLanding()">mdi-arrow-left-circle</v-icon>
        </v-col>
        <v-col align="start" cols="10" sm="11">
          <h3>Check Approval Status</h3>
        </v-col>
        <v-col align="center" cols="12" class="body-1 px-0 pt-0">
          <span>Key in your license plate number to check the status of your request</span>
        </v-col>
      </v-row>
      <!-- LICENSE PLATE NUMBER -->
      <ValidationObserver ref="checkStatus">
        <form>
          <v-row align="center" justify="center">
            <v-col cols="12" class="px-2">
              <ValidationProvider name="CheckStatus" rules="required2|alpha_num" v-slot="{ errors }">
                  <v-text-field 
                    v-model="check_plate_number"
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
            <!-- DATE OF VISITING -->
            <v-col cols="12">
              <v-dialog
                ref="dialog_date2"
                v-model="date_picker2"
                :return-value.sync="visit_date2"
                persistent
                width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <ValidationProvider name="VisitDate2" rules="required" v-slot="{ errors }">
                    <v-text-field
                      v-model="visit_date2"
                      label="Date of Visiting"
                      prepend-icon="mdi-calendar"
                      readonly outlined rounded dense clearable hide-details
                      color="teal darken-3"
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                    <ul class="text-left teal--text teal--darken-4 caption font-italic font-weight-bold">
                      <li v-for="(error, index) in errors" :key="index">
                        <span>{{ error }}</span>
                      </li>
                    </ul>
                  </ValidationProvider> 
                </template>
                <v-date-picker
                  v-model="visit_date2"
                  scrollable
                  :min="new Date().toISOString().substr(0, 10)"
                  :max="endDate()"
                  color="teal darken-3"
                >
                  <v-spacer></v-spacer>
                  <v-btn
                    text
                    color="primary"
                    @click="date_picker2 = false"
                  >
                    Cancel
                  </v-btn>
                  <v-btn
                    text
                    color="primary"
                    @click="pickDate2()"
                  >
                    OK
                  </v-btn>
                </v-date-picker>
              </v-dialog> 
            </v-col>
            <v-col cols="12" align="center" justify="center">
              <v-btn @click="checkStatus()" depressed :width="widthRegisterButton" class="teal lighten-2">CHECK STATUS</v-btn>
            </v-col>    
          </v-row>      
        </form>
      </ValidationObserver>
      <!-- POP UP MESSAGE -->
      <v-dialog v-model="dialogCheckStatus" max-width="400">
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
            <v-btn @click="dialogCheckStatus = false" text color="primary">
              OK
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>      
    </v-container>
    <!-- BOTTOM NAVIGATION BAR -->
    <v-bottom-navigation fixed app grow mandatory shift dark v-model="btm_nav_bar" background-color="teal darken-2">
      <v-btn value="register_lp">
        <span>Register License Plate</span>
        <v-icon>mdi-card-account-details</v-icon>
      </v-btn>
      <v-btn value="check_status">
        <span>Check Status</span>
        <v-icon>mdi-list-status</v-icon>
      </v-btn>       
    </v-bottom-navigation>      
  </v-container>
</template>

<script>
import { ValidationProvider, extend, ValidationObserver } from "vee-validate";
import { required, alpha_num, alpha_spaces, digits } from 'vee-validate/dist/rules';
import { getUser } from '../utils';
import axios from 'axios';

extend('alpha_num', {
  ...alpha_num,
  message: 'Must be only alphabetic characters or numbers'
})
extend('alpha_spaces', {
  ...alpha_spaces,
  message: 'Must be only alphabetic characters'
})
extend('digits', {
  ...digits,
  message: 'Must be 6 digits'
})
extend('required', {
  ...required,
  message: 'This field is required'
})
extend('required2', {
  ...required,
  message: 'Enter License Plate Number to Check'
})
extend('minMax', {
  validate(value, { min, max}) {
    let isnum = /^\d+$/.test(value);
    return value.length >= min && value.length <= max && isnum;
  },
  params: ['min', 'max'],
  message: '{_field_} must be only between {min} to {max} numbers'
})


export default {
  name: 'VisitorPage',
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
    return{
      btm_nav_bar: 'register_lp',
      plate_number: '',
      unit_number: '',
      contact_number: '',
      visit_purpose: '',
      visitor_name: '',
      secret_code: '',
      visit_date: '', //new Date().toISOString().substr(0, 10)
      visit_date2: '',
      date_picker: false,
      date_picker2: false,
      check_plate_number: '',
      dialogRegisterLP: false,
      dialog_msg_header: '',
      dialog_msg: '',
      dialogCheckStatus: false,
      dialog_msg_header2: 'STATUS',
      dialog_msg2: '',
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
    goToLanding() { // back to landing page
      this.$router.push({name: 'LandingPage'});
    },
    pickDate() {
      this.$refs.dialog_date.save(this.visit_date)
    },
    pickDate2() {
      this.$refs.dialog_date2.save(this.visit_date2)
    },
    endDate() {
      var date = new Date().toISOString().substr(0, 4)
      let month = "-12-31"
      var end_date = date.concat(month)
      return end_date
    },
    close_dialogRegisterLP() {
      this.dialogRegisterLP = false
    },
    register() { //register visitor's license plate
      this.$refs.registerLP.validate().then(success => 
      {
        if (!success) {
          return;
        }
        let plate = this.plate_number.toUpperCase();
        let unit = this.unit_number.toUpperCase();
        let purpose = this.visit_purpose.toUpperCase();
        let name = this.visitor_name.toUpperCase();
        let hostname = window.location.hostname;
        let API_URL = `http://${hostname}:5000/visitor_lp`;   
        const payload = {
          plate_number: plate,
          unit_number: unit,
          v_contactno: this.contact_number,
          visit_purpose: purpose,
          visitor_name: name,
          secret_code: this.secret_code,
          visit_date: this.visit_date
        }
        axios.post(API_URL, payload)
        .then((res) => {
          this.dialog_msg_header = 'Unsuccessful Registration'
          if (res.data == '1') { //BLACKLISTED LP
            this.dialog_msg = 'The license plate is blacklisted. Please proceed to the security guard house for registration at the entrance when you arrive at the residential area.'
          } else if (res.data == '2') { //WHITELISTED LP
            this.dialog_msg = 'The license plate has already registered by the resident. You can access the residential area with your registered license plate.'
          } else if (res.data == '3') { //LP IS REGISTERED BY OTHERS
            this.dialog_msg = 'The license plate has already registered by other users.'
          } else if (res.data == '4') { //LP EXISTED ON SAME DATE
            this.dialog_msg = 'The license plate is registered on the same date before. Please check the status instead.'
          } else if (res.data == '5') { //INVALID CODE/UNIT NUMBER
            this.dialog_msg = 'Invalid secret code or unit number. Please try again.'
          } else { //SUCCESSFUL REGISTRATION
            this.dialog_msg_header = 'Successful Registration'
            this.dialog_msg = 'The license plate registration is completed. You can check the status of the request.'
            this.plate_number = this.unit_number = this.contact_number = this.visit_purpose = 
            this.visitor_name = this.secret_code = this.visit_date = '';
            this.$refs.registerLP.reset();
          }
          this.dialogRegisterLP = true;
        })
        .catch((error) => {
          alert("You are offline! Please connect to internet and try again.")
          console.log(error)
        })
      })
    },
    checkStatus() { //check approval status
      this.$refs.checkStatus.validate().then(success => {
        if (!success) {
          return
        }
        let plate = this.check_plate_number.toUpperCase();
        let hostname = window.location.hostname;
        let API_URL = `http://${hostname}:5000/visitor_lp/${plate}/${this.visit_date2}`;
        axios.get(API_URL)
        .then((res) => {
          this.dialog_msg2 = res.data;
          this.dialogCheckStatus = true
          this.check_plate_number = this.visit_date2 ='';
          this.$refs.checkStatus.reset();
        })
        .catch((error) => {
          alert("You are offline! Please connect to internet and try again.")
          console.log(error)
        })  
      })
    }
  },
  components:{
    ValidationProvider,
    ValidationObserver
  },
}
</script>