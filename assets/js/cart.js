document.addEventListener('DOMContentLoaded', function(){
    let add_forms = document.querySelectorAll('.room-types__form');
    let basket_items = document.querySelector('.cart-items');
    let cart_count_main = document.querySelector('.cart-count');
    let total_price = document.querySelector(".stay__total-price");
    let basket_items_arr = [];


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

    function ajaxBlockCategory(url, params) {
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
                add_items(JSON.parse(data).data, basket_items_arr)
            }

        )
        .catch(error => console.error(error))
    }

    function ajaxBlockCancel(url, params) {
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
    for (let form = 0; form < add_forms.length; form++) {
        let form_item = add_forms[form];
        form_item.addEventListener("submit", function (e){
            e.preventDefault();
            let add_button = form_item.querySelector('.booking-add');
            let category_id = add_button.dataset.categoryid;
            let hotel_id = add_button.dataset.hotelid;
            let category_name = add_button.dataset.category;
            let tariff = add_button.dataset.tariff;
            let tariff_id = add_button.dataset.tariffid;
            let tariff_price = add_button.dataset.tariffprice;
            let datn = add_button.dataset.datn;
            let datk = add_button.dataset.datk;


            let basket_item_dir = {
                "hotel_id": hotel_id,
                "category_id": category_id,
                "category_name": category_name,
                "tariff_name": tariff,
                "tariff_price": tariff_price,
                "tariff_id": tariff_id,
                "datn": datn,
                "datk": datk,

            }
            ajaxBlockCategory("block_category", basket_item_dir)
            form_item.closest(".room-types__type").style.display = "none";


        })
    }
    function add_items(dir, arr){
        let new_basket_item = "<div class='room-item' data-cancelid='${dir.category_id}${dir.tariff_id}'><div class=\"room-item__wrapper\">" +
            "<div class=\"cancel buscket-delete\"> <span></span> <span></span> </div>" +
            "<p class=\"room-item__name\">" + dir.category_name + "</p>" +
            "<p class=\"room-item__price\">€ " + dir.tariff_price + "</p>" + "" +
            "<div class=\"room-item__more-info\"> <span></span> <span></span> </div>" +
            "</div><p class=\"room-item__dop\">Bed & breakfast</p></div>";

        arr.push(dir);
        localStorage.setItem("basket_items", JSON.stringify(arr))
        // basket_items.append(new_basket_item);
        let arr_zakid = []
        arr.forEach((element) => {
            arr_zakid.push(String(element.idzakaza));
            console.log(arr_zakid);
        })
        if (arr_zakid.length > 1){
            console.log(arr_zakid[arr_zakid.length - 2]);
            ajaxBlockContinue("block_continue", arr_zakid[arr_zakid.length - 2])
        }
        const hotelCatalog = new BasketItems();
        hotelCatalog.render()
        let count = document.querySelector(".cart-count");
        localStorage.setItem("count", arr.length)
        count.innerHTML = arr.length;
        let summ = 0;
        JSON.parse(localStorage.getItem("basket_items")).forEach((element) => {
            summ += Number(element.tariff_price);
        })
        total_price.innerHTML = "€ " + summ;

        basket_delete = document.querySelectorAll(".cancel.buscket-delete");
            for (let i = 0; i < basket_delete.length; i++) {
                let del_item = basket_delete[i];
                del_item.addEventListener('click', function(e){
                    e.preventDefault();
                    let id_zak = this.closest(".room-item").dataset.idzak;
                    let tar = this.dataset.cancelid;
                    ajaxBlockCancel("block_cancel", id_zak);
                    this.closest(".room-item").remove();
                    let all_tariffs = document.querySelectorAll(".room-types__type");
                    delete_item(del_item.dataset.cancelid);
                    all_tariffs.forEach((element) => {
                        if (element.dataset.tarifid == del_item.dataset.cancelid){
                            element.style.display = "flex";
                        }
                    })
                })
            }
    }
    function delete_item(data){
        let items = []
        JSON.parse(localStorage.getItem("basket_items")).forEach((element) => {
            let cat_tar = element.category_id + element.tariff_id;
            if (cat_tar != data){
                items.push(element);
            }
        })
        localStorage.setItem("basket_items", JSON.stringify(items));
        const hotelCatalog = new BasketItems();
        hotelCatalog.render();
        let count = document.querySelector(".cart-count");
        localStorage.setItem("count", String(items.length));
        count.innerHTML = String(items.length);
        let sum = 0;
        JSON.parse(localStorage.getItem("basket_items")).forEach((element) => {
            sum += Number(element.tariff_price);
        })
        total_price.innerHTML = "€ " + sum;


    }
    class BasketItems {
        render() {
            if (JSON.parse(localStorage.getItem("basket_items").length > 0)) {
                let local_items = JSON.parse(localStorage.getItem("basket_items"));
                let htmlCatalog = '';
                local_items.forEach((element) => {
                    htmlCatalog += `
                        <div class="room-item"  data-idzak="${element.idzakaza}">
                        <div class="room-item__wrapper">
                    <div class="cancel buscket-delete" data-cancelid="${element.category_id}${element.tariff_id}"> <span></span> <span></span> </div>
                    <p class="room-item__name">${element.category_name}</p>
                    <p class="room-item__price">${element.tariff_price}</p>
                    <div class="room-item__more-info"> <span></span> <span></span> </div>
                    </div>
                    <p class="room-item__dop">Bed & breakfast</p>
                        </div>`
                })
                const html = htmlCatalog;
                basket_items.innerHTML = html;
                let sum = 0;
                JSON.parse(localStorage.getItem("basket_items")).forEach((element) => {
                    sum += Number(element.tariff_price);
                })
                total_price.innerHTML = "€ " + sum;
            }
            else {
                console.log("no items");
            }
        }
    }
    const hotelCatalog = new BasketItems();
    hotelCatalog.render()
    let basket_delete = document.querySelectorAll(".cancel.buscket-delete");
     for (let i = 0; i < basket_delete.length; i++) {
        let del_item = basket_delete[i];
        del_item.addEventListener('click', function(){
            console.log(this.closest(".room-item").dataset.idzak);
            let data = this.closest(".room-item").dataset.idzak;
            ajaxBlockCancel("block_cancel", data);
            this.closest(".room-item").remove();
            delete_item(del_item.dataset.cancelid);

        })
     }
});
