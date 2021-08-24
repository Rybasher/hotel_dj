document.addEventListener('DOMContentLoaded', function(){
    let room_choince = document.querySelector(".room-choice");
    let personal_information = document.querySelector(".personal-information");
    let reciept = document.querySelector(".reciept");
    let cont_but = document.querySelector(".stay__total-button");
    let step1 = "filtration";
    let step2 = "add_details";
    let step3 = "payment";

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function ajaxBlockContinue(url, params) {
        const csrfToken = getCookie("csrftoken");
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(params)
        })
        .then(
            response => console.log(response.text())
        )
        .catch(error => console.error(error))
    }
    function ajaxBlockPay(url, params) {
        const csrfToken = getCookie("csrftoken");
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(params)
        })
        .then(
            response => response.text()
        )
            .then(
                (data) => {
                    text();

                    ajaxUpcPay("upc_pay", JSON.parse(data).data)
                }
            )
        .catch(error => console.error(error))
    }
    function text(params){
        console.log(params);
    }

    function ajaxUpcPay(url, params) {
        const csrfToken = getCookie("csrftoken");
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(params)
        })
        .then(
            response => console.log(response.text())
        )

        .catch(error => console.error(error))
    }

    function renewBlock(){
        JSON.parse(localStorage.getItem("basket_items")).forEach((element) => {
                ajaxBlockContinue("block_continue", String(element.idzakaza))
            })
    }

    cont_but.addEventListener("click", function (){

        if (!cont_but.classList.contains(step2)) {
            renewBlock();
            room_choince.classList.add("hidden");
            personal_information.classList.remove("hidden");
            console.log("step1")
            cont_but.classList.add(step2);


        }
        else if (cont_but.classList.contains(step2) && !cont_but.classList.contains(step3)){
            let ids = [];
            JSON.parse(localStorage.getItem("basket_items")).forEach((element) => {
                ids.push(element.idzakaza);
            })
            let datastore = [];


            JSON.parse(localStorage.getItem("basket_items")).forEach((element) => {
                datastore.push(element);
            })
            let params = {
                "name": document.querySelector(".inputs__name").value,
                "l_name": document.querySelector(".inputs__last-name").value,
                "email": document.querySelector(".inputs__email").value,
                "phone": document.querySelector(".inputs__phone").value,
                "desc": document.querySelector(".inputs__textarea").value,
                "spisid": ids,
                "datatostore": datastore
            }

            console.log("step2");
            console.log(params);
            ajaxBlockPay("block_pay", params);
            cont_but.classList.add(step3);


        }
    })

});
