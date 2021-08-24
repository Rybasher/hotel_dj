// document.addEventListener('DOMContentLoaded', function(){
//     let form = document.querySelector(".search");
//     form.addEventListener("submit", function (e){
//         e.preventDefault();
//         let daten = document.querySelector('.daten').value;
//         let datek = document.querySelector('.daten').value;
//         let checkin = document.querySelector('.checkin-field').value;
//         let checkout = document.querySelector('.checkout-field').value;
//         daten = daten.split("-").join('');
//         datek = datek.split("-").join('');
//         checkin = checkin.split(":").join("") + "00";
//         checkout = checkout.split(":").join("") + "00";
//         if (checkin.split("").length == 5){
//             checkin = "0" + checkin
//         }
//         if (checkout.split("").length == 5){
//             checkout = "0" + checkout
//         }
//         console.log(daten.value, datek.value, checkin.value, checkout.value);
//         // form.submit();
//     })
//
// });
