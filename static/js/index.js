$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    console.log(id)
    $.ajax({
        type: 'GET',
        url : '/pluscart',
        data: {
            prod_id : id,
        },
        success:function (data){
            console.log(data)


            // Update the quantity in the DOM
            document.getElementById("quantity-" + id).innerText = data.quantity;

            // Update the amount (price for this product)
            document.getElementById("amount-" + id).innerText = data.amount;

            // Update the total amount (sum of all products' prices + shipping)
            document.getElementById("total-amount").innerText = data.total_amount;

        }

    })
})


// minus cart ajax
$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    console.log(id)
    $.ajax({
        type: 'GET',
        url : '/minuscart',
        data: {
            prod_id : id,
        },
        success:function (data){
            console.log(data)
            document.getElementById("quantity-" + id).innerText = data.quantity;
            document.getElementById("amount-" + id).innerText = data.amount;
            document.getElementById("total-amount").innerText = data.total_amount;

        }

    })
})


// delete cart ajax 
$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    console.log(id)
    $.ajax({
        type: 'GET',
        url : '/removecart',
        data: {
            prod_id : id,
        },
        success:function (data){
            console.log(data)
            console.log('delete ho raha hy')
            // Update the amount (price for this product)
            document.getElementById("amount-" + id).innerText = data.amount;

            // Update the total amount (sum of all products' prices + shipping)
            document.getElementById("total-amount").innerText = data.total_amount;

        }

    })
})