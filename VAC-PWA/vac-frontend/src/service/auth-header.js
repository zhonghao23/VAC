/*
Programmer Name:    CHIAM ZHONG HAO
Program Name:       service/auth-header.js
Description:        Export a function which retrieves the JWT from local storage and make it ready to be passed to the backend.
First Written On:   01/01/2021
Edited On:          04/03/2021
*/
export default function authHeader() {
  let user = JSON.parse(localStorage.getItem('user'));

  if (user && user.token) {
    return { Authorization: 'Bearer: ' + user.token };
  } else {
    return {};
  }
}