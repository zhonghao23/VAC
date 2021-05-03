/*
Programmer Name:    CHIAM ZHONG HAO
Program Name:       store/auth.module.js
Description:        It handles the removing of JWT from localstorage and log out the user.
First Written On:   01/01/2021
Edited On:          04/03/2021
*/
export const auth = {
    namespaced: true,

    state: {
      status: {
        loggedIn: null
      }  
    },
    actions: {
        logout({ commit }) {
            localStorage.removeItem('user');
            commit('logout');
        },
    },
    mutations: {
        logout(state) {
            state.status.loggedIn = false;
        },
    }
};