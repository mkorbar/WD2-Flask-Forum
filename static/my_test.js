

let user = {
 firstName: 'Janez',
 lastName: 'Novak',
 age: 123,

 fullName: function() {
  return this.firstName + ' ' + this.lastName
 }
}
