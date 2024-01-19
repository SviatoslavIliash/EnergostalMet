// onsubmit, onclick and oninput functions
$(document).ready(function(){
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

    nav_height_changer()
})

function nav_height_changer(){
    let top_navbar = document.getElementById("main-navbar");
    let top_navbar_height = $(top_navbar).outerHeight();

    let sidebar_menu = document.getElementById("sidebarMenu");
    let main_block = document.getElementById("main-block");

    let top_navbar_height_px = top_navbar_height.toString() + "px";
    sidebar_menu.style["margin-top"] = top_navbar_height_px;
    main_block.style["margin-top"] = top_navbar_height_px;
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


function update_in_cart(target){
    add_to_cart_inline(target, update_cart)
}

function add_to_cart(target){
    add_to_cart_inline(target, update_nav)
    tempAlert("Товар додано у кошик!",3000);
}

function add_to_cart_inline(form, after_func){
    const url  = form.getAttribute("action")
    const form_data = $(form).serialize()
    $.post(url, form_data, function(data){
        after_func(data, form)
    })
}

function remove_from_cart(button, url){
    if (confirm("Видалити товар з кошика?")) {
        $.get(url, function(data){
            update_cart(data, button)

        })
    }
}

function update_price(elem_id, new_price){
    elem = document.getElementById(elem_id)
    elem.textContent = new_price + " грн"
}

function update_nav_cart_price(price){
    update_price("cart_nav_total_price", price)
}

function update_cart_total_price(price){
    update_price("cart_total_price", price)
}

function update_nav(data, obj){
    update_nav_cart_price(data["Total"])
}

function update_cart(data, obj){
    var total_price = data["Total"]
    var form_price = 0
    var is_deleted = false

    if ("Deleted" in data){
        is_deleted = true
    }
    if ("Price" in data){
        form_price = data["Price"]
    }

    update_nav_cart_price(total_price)
    update_cart_total_price(total_price)

    card = obj.closest(".card")
    if (is_deleted){
        card.remove()
    }
    else{
        var price_elem = card.getElementsByClassName("card_price")[0]
        price_elem.textContent = form_price + " грн"
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

