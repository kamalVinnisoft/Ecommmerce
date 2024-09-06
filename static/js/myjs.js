function AddToCart(csrf_token,isAuth,productId, productName, price, MainImageUrl, quantity = 1) {
    // Get the existing cart data from local storage
    console.log(">>>>>>>>>>>>>>>>>>>>>>>>>>>>",csrf_token,isAuth)
    if (isAuth == 'True'){
        console.log("llllllllllllllllllllllllllllllllllllllllllllllllllllllll")
        $.ajax({
            url: '/cart/addtocart/',  // URL to the Django view
            type: 'POST',   // HTTP method
            dataType: 'json',  // Expected data type from server
            
            data:{
                'ProductId':productId,
                'csrfmiddlewaretoken':  csrf_token ,
            },
            success: function(response) {
                console.log("KKKKKKKKKKKKKKKKKKKKKKKK",response)
                
                $('#response').text(response.message);  // Handle success
            },
            error: function(xhr, status, error) {
                $('#response').text('An error occurred');  // Handle error
            }
        });
    }else{
        
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        console.log("Adding to cart:", productId, productName, price, MainImageUrl, quantity);

        // Check if the product is already in the cart
        let item = cart.find(item => item.productId === productId);
        if (item) {
            // If the product is already in the cart, update the quantity
            item.quantity += parseInt(quantity);
            console.log("Updated quantity:", item.quantity);
        } else {
            // If the product is not in the cart, add it
            cart.push({ productId, productName, price, MainImageUrl, quantity: parseInt(quantity) });
        }

        // Save the updated cart back to local storage
        localStorage.setItem('cart', JSON.stringify(cart));

        // Update the total number of products in the cart
        
        updateCartTotal();
    }
}

function remove_from_cart(csrf_token,isAuth,productId) {
    console.log(csrf_token,isAuth)
    if (isAuth){
        $.ajax({
            url: '/cart/removefromcart/',  // URL to the Django view
            type: 'POST',   // HTTP method
            dataType: 'json',  // Expected data type from server
            
            data:{
                'ProductId':productId,
                'csrfmiddlewaretoken':  csrf_token ,
            },
            success: function(response) {
                console.log("KKKKKKKKKKKKKKKKKKKKKKKK",response)
                $('#response').text(response.message);  // Handle success
            },
            error: function(xhr, status, error) {
                $('#response').text('An error occurred');  // Handle error
            }
        });
    }else{

        console.log("Attempting to remove product:", productId);

        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        cart = cart.filter(item => item.productId !== productId);
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartUI();
    }
}

function updateCartTotal() {
    // Get the cart from local storage
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Calculate the total quantity of items in the cart
    let totalQuantity = cart.reduce((total, item) => total + item.quantity, 0);

    // Display the total quantity in the cart badge
    // document.getElementById('cart-total').textContent = totalQuantity;
}


function updateCartUI() {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    let cartTableBody = document.getElementById('cart-table-body');
    
    let subtotal = 0;

    cartTableBody.innerHTML = cart.map(item => {
        const itemTotal = item.quantity * item.price;
        subtotal += itemTotal;
        return `
            <tr id="cart-item-${item.productId}">
                <td class="align-middle">
                    <img src="${item.MainImageUrl || ''}" alt="" style="width: 50px;">
                    ${item.productName}
                </td>
                <td class="align-middle">$${item.price}</td>
                <td class="align-middle">
                    <div class="input-group quantity mx-auto" style="width: 100px;">
                        <div class="input-group-btn">
                            <button class="btn btn-sm btn-primary btn-minus" onclick="dec_product_to_cart('None','False','${item.productId}')">
                                <i class="fa fa-minus"></i>
                            </button>
                        </div>
                        <input type="text" id="quantity-${item.productId}" class="form-control form-control-sm bg-secondary text-center" value="${item.quantity}" readonly>
                        <div class="input-group-btn">
                            <button class="btn btn-sm btn-primary btn-plus" onclick="inc_product_to_cart('None','False','${item.productId}')">
                                <i class="fa fa-plus"></i>
                            </button>
                        </div>
                    </div>
                </td>
                <td class="align-middle">$${itemTotal}</td>
                <td class="align-middle">
                    <button class="btn btn-sm btn-danger" onclick="remove_from_cart('None','False','${item.productId}')">
                        <i class="fa fa-times"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');

    // Update the cart summary
    document.getElementById('cart-subtotal').innerText = `$${subtotal}`;
    if (subtotal > 0){
        document.getElementById('cart-total').innerText = `$${subtotal + 10}`; // Assuming $10 shipping
    }else{
        document.getElementById('cart-total').innerText = `$0`; // Assuming $10 shipping
    }
    
}


function inc_product_to_cart(csrf_token,isAuth,productId) {
    console.log("User authenticated:", isAuth);
    console.log("Attempting to increment product:", productId);
    if (isAuth == 'True'){
        $.ajax({
            url: '/cart/addtocart/',  // URL to the Django view
            type: 'POST',   // HTTP method
            dataType: 'json',  // Expected data type from server
            
            data:{
                'ProductId':productId,
                'csrfmiddlewaretoken':  csrf_token ,
            },
            success: function(response) {
                $('#response').text(response.message);  // Handle success
            },
            error: function(xhr, status, error) {
                $('#response').text('An error occurred');  // Handle error
            }
        });
    }else{
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        let item = cart.find(item => item.productId === productId);
    
        if (item) {
            item.quantity += 1;
            localStorage.setItem('cart', JSON.stringify(cart));
        }
        updateCartUI();
    }
}



function dec_product_to_cart(csrf_token,isAuth,productId) {
    if (isAuth == 'True'){
        $.ajax({
            url: '/cart/decreasefromCart/',  // URL to the Django view
            type: 'POST',   // HTTP method
            dataType: 'json',  // Expected data type from server
            
            data:{
                'ProductId':productId,
                'csrfmiddlewaretoken':  csrf_token ,
            },
            success: function(response) {
                console.log("KKKKKKKKKKKKKKKKKKKKKKKK",response)
                $('#response').text(response.message);  // Handle success
            },
            error: function(xhr, status, error) {
                $('#response').text('An error occurred');  // Handle error
            }
        });
    }else{
        console.log("Attempting to decrement product:", productId);

        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        let item = cart.find(item => item.productId === productId);

        if (item) {
            item.quantity -= 1;
            if (item.quantity <= 0) {
                cart = cart.filter(item => item.productId !== productId);
            }
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartUI();
        }
    }
}