// onsubmit, onclick and oninput functions
$(document).ready(function(){
    nav_height_changer()

    $(".remove_btn").on("click", (e) => {
        url = e.target.getAttribute("data-url")
        remove_from_cart(e.target, url)
    });

    $(".cart_add_form").on('submit', (e) => {
        e.preventDefault()
        add_to_cart(e.target)
    });

    $(".input_quantity").on('input', (e) => {
        if (e.target.validity.valid){
            update_quantity(e.target)
        }
        else{
            e.target.reportValidity()
        }
    });

    $(".input_quantity").on('keypress', (e) => {
        //if(is_update(e.target) && e.which == 13){
        if(e.which == 13){
            e.preventDefault()
        }
    });

    $(".form-check-input").on('change', (e) => {
        if(e.target.checked){
            update_price(
                "product_price",
                e.target.getAttribute("data-price"),
                "/" + e.target.getAttribute("data-unit") // suffix for price
            )
        }
    });

})

function nav_height_changer(){
    let top_navbar = document.getElementById("main-navbar");
    let top_navbar_height = $(top_navbar).outerHeight();

    let sidebar_menu = document.getElementById("sidebarMenu");
    let main_block = document.getElementById("main-block");

    let top_navbar_height_px = top_navbar_height.toString() + "px";
    // following if blocks needed as in Cart we don't have side bar and main block
    if (sidebar_menu){
        sidebar_menu.style["margin-top"] = top_navbar_height_px;
    }
    if (main_block){
        main_block.style["margin-top"] = top_navbar_height_px;
    }
}

function str_to_bool(str){
    if (str.toLowerCase() === "true"){
        return true
    }
    else if (str.toLowerCase() === "false"){
        return false
    }
    throw "String " + str + " is not boolean value"
}

function is_update(target_input){
    var form_data = new FormData(target_input.form)
    return str_to_bool(form_data.get("update"))
}

function update_quantity(target_input){
    var form = target_input.form
    var form_data = new FormData(form)
    if(str_to_bool(form_data.get("update"))){
        // we are in cart now, let's update it
        update_in_cart(form)
    }
    else{
        // we are on Product page now
        //TODO add price update here if needed
    }
}


function update_in_cart(form){
    const url  = form.getAttribute("action")
    const form_data = $(form).serialize()
    multiplier = form.getAttribute("data-pack")
    let data_to_send = form_data + "&multiplier=" + multiplier
    console.log(data_to_send)
    $.post(url, data_to_send, function(data){
        update_cart(data, form)
    })
}

function add_to_cart(form){
    let price = null
    let multiplier = null

    const radioButtons = document.querySelectorAll('input[name="radioPackaging"]');
    for (const radioButton of radioButtons) {
        if (radioButton.checked){
            price = radioButton.getAttribute("data-price")
            multiplier = radioButton.getAttribute("data-mult")
        }
    }

    const url  = form.getAttribute("action")
    const form_data = $(form).serialize()
    let data_to_send = form_data

    if (price){
        data_to_send += "&price=" + price
    }
    if (multiplier){
        data_to_send += "&multiplier=" + multiplier
    }

    $.post(url, data_to_send, function(data){
        update_nav(data)
    })
    tempAlert("Товар додано у кошик!",3000);
}

function remove_from_cart(button, url){
    if (confirm("Видалити товар з кошика?")) {
        let form = button.closest("form")
        let data_to_send = $(form).serialize()
        let mult = form.getAttribute("data-pack")
        data_to_send += "&" + "multiplier=" + mult

        $.post(url, data_to_send, function(data){
            update_cart(data, button)

        })
    }
}

function update_price(elem_id, new_price, suffix=""){
    elem = document.getElementById(elem_id)
    elem.textContent = new_price + " грн" + suffix
}

function update_nav_cart_price(price){
    update_price("cart_nav_total_price", price)
}

function update_cart_total_price(price){
    update_price("cart_total_price", price)
}

function update_discount_total_price(price){
    update_price("discount_total_price", price)
}

function update_discount(price){
    update_price("discount", price)
}

function update_nav(data){
    update_nav_cart_price(data["Total_discount"])
}

function update_cart(data, obj){
    let total_price = data["Total"]
    let discount_total_price = data["Total_discount"]
    let discount = data["Discount"]
    let form_price = 0
    let is_deleted = false

    if ("Deleted" in data && data["Deleted"]){
        is_deleted = true
    }

    update_nav(data)
    update_cart_total_price(total_price)
    update_discount_total_price(discount_total_price)
    update_discount(discount)

    card = obj.closest(".card")
    if (is_deleted){
        card.remove()
    }

}

function tempAlert(msg,duration)
{
 var el = document.createElement("div");
 el.setAttribute("class", "alert alert-success d-flex align-items-center");
 el.setAttribute( "style","position:fixed;top:10%;left:50%;z-index: 2000;");
 el.innerHTML = msg;
 setTimeout(function(){
  el.parentNode.removeChild(el);
 },duration);
 document.body.appendChild(el);
}

