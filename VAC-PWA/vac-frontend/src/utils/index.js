/*
Programmer Name:    CHIAM ZHONG HAO
Program Name:       utils/index.js
Description:        It will be called when it has to check if the JWT is valid and to get user ID and identity.
First Written On:   01/01/2021
Edited On:          04/03/2021
*/
import store from '../store'


//CHECK IF JWT TOKEN STORED IN LOCAL STORAGE IS VALID
export function isValidJwt() {
    const user = localStorage.getItem('user');
    if (!user) {
        return false;
    }
    const data = JSON.parse(user);
    const jwt = data.token;
    if (!jwt || jwt.split('.').length < 3) { //INVALID JWT
        return false
    }
    const payload = JSON.parse(atob(jwt.split('.')[1]))
    const exp = new Date(payload.exp * 1000)
    const now = new Date()
    if (now < exp) { //IF TOKEN IS NOT EXPIRED
        return true;
    } else { //IF THE TOKEN IS EXPIRED
        store.dispatch('auth/logout').then(
            () => {
                return false;
            },
            error => {
                console.log(error);
            }
        )
    }
}

//GET USER ID & IDENTITY FROM JWT
export function getUser() {
    const user = localStorage.getItem('user');
    if (!user) {
        return false;
    }
    const data = JSON.parse(user);
    const jwt = data.token;
    const payload = JSON.parse(atob(jwt.split('.')[1]));
    return payload;
}