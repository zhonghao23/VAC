/*
Programmer Name:    CHIAM ZHONG HAO
Program Name:       router/index.js
Description:        It stores the page url and does some checks before the user is redirected to the pages.
First Written On:   01/01/2021
Edited On:          04/03/2021
*/
import Vue from 'vue'
import VueRouter from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import VisitorPage from '../views/VisitorPage.vue'
import SignInPage from '../views/SignInPage.vue'
import ResidentPage from '../views/ResidentPage.vue'
import SMOPage from '../views/SMOPage.vue'
import { isValidJwt } from '../utils/index.js'
import store from '../store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
    meta: { title: 'VAC-Home'}
  },
  {
    path: '/visitor',
    name: 'VisitorPage',
    component: VisitorPage,
    meta: { title: 'VAC-Visitor'}
  },
  {
    path: '/signin',
    name: 'SignInPage',
    component: SignInPage,
    props: true,
    meta: { title: 'VAC-Sign In'}
  },
  {
    path: '/resident',
    name: 'ResidentPage',
    component: ResidentPage,    
    meta: { title: 'VAC-Resident'}
  },
  {
    path: '/smo',
    name: 'SMOPage',
    component: SMOPage,
    meta: { title: 'VAC-SMO'}
  }
]

const router = new VueRouter({
  //mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  const public_pages = ['/', '/visitor', '/signin']; //pages that everyone could access
  const auth_required = !public_pages.includes(to.path); //page that requires user to login
  const valid = isValidJwt(); //check if jwt has expired
  if (auth_required && !valid) { //if the page requires user to login and the token is expired
    store.dispatch('auth/logout')
    .then(() => {
      alert("Session Expired. Please sign in again.")
      next('/signin')
    },
    error => {
      console.log(error);
    })
  } else {
    next();
  }
})

const DEFAULT_TITLE = 'VAC';
router.afterEach((to) => {
  // Use next tick to handle router history correctly
  // see: https://github.com/vuejs/vue-router/issues/914#issuecomment-384477609
  Vue.nextTick(() => {
      document.title = to.meta.title || DEFAULT_TITLE; //it is used to change the page title of VAC
  });
});

export default router
