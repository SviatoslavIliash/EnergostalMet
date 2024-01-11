// onsubmit and onclick functions
$(document).ready(function(){
    $(".remove_btn").on("click", (e) => {
        target = e.target
        url = target.getAttribute("data-url")
        remove_from_cart(target, url)
    });

    $(".cart_add_form").on('submit', (e) => {
        e.preventDefault()
        add_to_cart(e.target)
    });

    $('.cart_update_form').on('submit', (e) => {
        e.preventDefault()
        update_in_cart(e.target)
    });
}) // input -> on update


function update_in_cart(target){
    add_to_cart_inline(target, update_cart)
}

function add_to_cart(target){
    add_to_cart_inline(target, update_nav)
     // alert("Added to Cart!!!")


}

function add_to_cart_inline(form, after_func){
    const url  = form.getAttribute("action")
    const form_data = $(form).serialize()
    $.post(url, form_data, function(data){
        after_func(data, form)
    })
}

function remove_from_cart(button, url){
    $.get(url, function(data){
        update_cart(data, button)
    })
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
    if ("Price" in data){
        form_price = data["Price"]
    }
    if ("Deleted" in data){
        is_deleted = true
    }

    update_nav_cart_price(total_price)
    update_cart_total_price(total_price)

    row = obj.parentElement.parentElement
    if (is_deleted){
        // remove deleted row from Html DOM
        row.remove()
    }
    else{
        // update price in <td> element
        row.cells[row.cells.length - 1].textContent = form_price + " грн"
    }
}

//    function customAlert(msg,duration) // Function for message add product to cart
//    {
//     var styler = document.createElement("div");
//      styler.setAttribute("style","border: solid 1px Green;width:auto;height:auto;top:50%;left:40%;background-color:#22CE83;color:Black");
//     styler.innerHTML = "<h1>"+msg+"</h1>";
//     setTimeout(function()
//     {
//       styler.parentNode.removeChild(styler);
//     },duration);
//     document.body.appendChild(styler);
//         function caller()
//        {
//            customAlert("Added to cart","3000");
//        }
//    }
