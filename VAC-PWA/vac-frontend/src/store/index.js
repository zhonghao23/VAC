/*
Programmer Name:    CHIAM ZHONG HAO
Program Name:       store/index.js
Description:        It uses the Vuex state management and export the function in auth.module.js
First Written On:   01/01/2021
Edited On:          04/03/2021
*/
import Vue from 'vue';
import Vuex from 'vuex';
import { auth } from './auth.module';

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        auth
    }
})