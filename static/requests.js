"use strict";

(async function () {

/***************
function makeRequest(url, callback) {
  var httpRequest = new XMLHttpRequest();

  httpRequest.onreadystatechange = () => stateChangeHandler(httpRequest, callback)

  httpRequest.open('GET', url);
  httpRequest.send();
}

function stateChangeHandler(request, callback) {
//  console.log(request.readyState);
  if (request.readyState == XMLHttpRequest.DONE) {
    if(request.status == 200) {
      callback(request.response);
    } else {
      console.error('There was a problem with the request', request);
    }
  }

}

// callback hell:
makeRequest('https://catfact.ninja/fact', (response) => {
  var data1 = response.json();
  makeRequest('https://catfact.ninja/fact', (response) => {
    makeRequest('https://catfact.ninja/fact', (response) => {
      makeRequest('https://catfact.ninja/fact', (response) => {
        console.log(response)
      })
    })
  })
})

***********/
/***********
function errorHandler(error) {
  console.error('Request failed', error)
}

var fetch_promise = fetch('https://catfact.ninja/fact')

console.log(fetch_promise);

fetch_promise
.then(response => response.json())
.then(function (text) {
  console.log(text)
})
.catch(errorHandler);


*****************/
/*****************

var response = await fetch('https://catfact.ninja/fact')
var fact = await response.json()

console.log(fact.length);

*****************/

const formData = new FormData();
formData.set('field_name', 'field_value');
formData.set('field_name2', 'field_value2');

const options = {
  method: 'POST',
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({
    'field_name_1': 'field_value_1',
    'field_name_2': 'field_value_2'
  })
};

var response = await fetch('http://flask-forum.local:5000/api/user', options);
var fact = await response.json()

console.log(fact.length);



})()



