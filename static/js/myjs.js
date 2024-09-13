function displayMessages(message) {
    console.log("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
    const alertContainer = document.querySelector('.alert-container');
    console.log(alertContainer);

    // Clear previous messages
    alertContainer.innerHTML = '';

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${message.tags}`;

    const alertIcon = document.createElement('span');
    alertIcon.className = 'alert-icon';


    const alertMessage = document.createElement('span');
    alertMessage.className = 'alert-message';
    alertMessage.textContent = message; // Assuming `message` has a `text` property for the message content

    alertDiv.appendChild(alertIcon);
    alertDiv.appendChild(alertMessage);

    alertContainer.appendChild(alertDiv);
   
}


function AddToCart(csrf_token,isAuth,productId, productName, price, MainImageUrl, quantity = 1) {
    // Get the existing cart data from local storage
    if (isAuth == 'True'){
        $.ajax({
            url: '/cart/addtocart/',  // URL to the Django view
            type: 'POST',   // HTTP method
            dataType: 'json',  // Expected data type from server
            
            data:{
                'ProductId':productId,
                'quantity':quantity,
                'csrfmiddlewaretoken':  csrf_token ,
            },
            success: function(response) {
                document.querySelector('.badge').textContent = response.cart_count;
                displayMessages(response.message);
            },
            error: function(xhr, status, error) {
                $('#response').text('An error occurred');  // Handle error
            }
        });
    }else{
        
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        document.querySelector('.badge').textContent = cart.reduce((total, item) => total + item.quantity, 0)
        // Check if the product is already in the cart
        let item = cart.find(item => item.productId === productId);
        if (item) {
            // If the product is already in the cart, update the quantity
            item.quantity += parseInt(quantity);
        } else {
            // If the product is not in the cart, add it
            cart.push({ productId, productName, price, MainImageUrl, quantity: parseInt(quantity) });
        }

        // Save the updated cart back to local storage
        localStorage.setItem('cart', JSON.stringify(cart));

        // Update the total number of products in the cart
        displayMessages(`${productName} is added to your cart successfully`);
        updateCartTotal();
    }
}

function remove_from_cart(csrf_token,isAuth,productId) {
    if (isAuth == 'True'){
        $.ajax({
            url: '/cart/removefromcart/',  // URL to the Django view
            type: 'POST',   // HTTP method
            dataType: 'json',  // Expected data type from server
            
            data:{
                'ProductId':productId,
                'csrfmiddlewaretoken':  csrf_token ,
            },
            success: function(response) {
                displayMessages(response.message);
                // Parse the total_cost as an integer
                let total_cost = parseInt(response.total_cost, 10);
                document.querySelector('.badge').textContent = response.cart_count;
                // Update the cart's subtotal and total cost with shipping
                document.getElementById('cart-subtotal').innerText = total_cost;
                
                if (total_cost > 0) {
                    // Assuming $10 shipping fee, update the cart total
                    document.getElementById('cart-total').innerText = total_cost + 10;
                } else {
                    document.getElementById('cart-total').innerText = '$0';  // Set total to $0 if no items
                }
                const row = document.getElementById('cart-item-' + productId);
                if (row) {
                    row.remove();
                }
            },
            error: function(xhr, status, error) {
                $('#response').text('An error occurred');  // Handle error
            }
        });
    }else{
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        cart = cart.filter(item => item.productId !== productId);
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartUI();
        displayMessages(`${item.productName} is removed from your cart successfully`);
        document.querySelector('.badge').textContent = cart.reduce((total, item) => total + item.quantity, 0)

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
                displayMessages(response.message);
                var quantityInput = document.getElementById('quantity-' + productId);
                quantityInput.value= parseInt(quantityInput.value) + 1;
                document.querySelector('.badge').textContent = response.cart_count;
                // Parse the total_cost as an integer
                let total_cost = parseInt(response.total_cost, 10);
                
                // Update the cart's subtotal and total cost with shipping
                document.getElementById('cart-subtotal').innerText = total_cost;
                
                if (total_cost > 0) {
                    // Assuming $10 shipping fee, update the cart total
                    document.getElementById('cart-total').innerText = total_cost + 10;
                } else {
                    document.getElementById('cart-total').innerText = '$0';  // Set total to $0 if no items
                }
            },
        });
    }else{
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        let item = cart.find(item => item.productId === productId);
        document.querySelector('.badge').textContent = cart.reduce((total, item) => total + item.quantity, 0)
        if (item) {
            item.quantity += 1;
            localStorage.setItem('cart', JSON.stringify(cart));
        }
        updateCartUI();
        displayMessages(`${item.productName} is added to your cart successfully`);
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
                displayMessages(response.message);
                var quantityInput = document.getElementById('quantity-' + productId);
                quantityInput.value= parseInt(quantityInput.value) - 1;
                // Parse the total_cost as an integer
                let total_cost = parseInt(response.total_cost, 10);
                
                // Update the cart's subtotal and total cost with shipping
                document.getElementById('cart-subtotal').innerText = total_cost;
                document.querySelector('.badge').textContent = response.cart_count;
                if (total_cost > 0) {
                    // Assuming $10 shipping fee, update the cart total
                    document.getElementById('cart-total').innerText = total_cost + 10;
                } else {
                    document.getElementById('cart-total').innerText = '$0';  // Set total to $0 if no items
                }
            },
            error: function(xhr, status, error) {
                $('#response').text('An error occurred');  // Handle error
            }
        });
    }else{

        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        let item = cart.find(item => item.productId === productId);
        document.querySelector('.badge').textContent = cart.reduce((total, item) => total + item.quantity, 0)
        if (item) {
            item.quantity -= 1;
            if (item.quantity <= 0) {
                cart = cart.filter(item => item.productId !== productId);
            }
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartUI();
            displayMessages(`${item.productName} is removed from your cart successfully`);
        }
    }
}

function CartUpdate(isAuthenticated,csrf_token){
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    let productsList = cart.map(item => ({
        productId: item.productId,
        quantity: item.quantity
    }));
    if (cart.length > 0 && isAuthenticated) {
        $.ajax({
            url: '/cart/updateCart/',  // URL to the Django view
            type: 'POST',              // HTTP method
            dataType: 'json',          // Expected data type from server
            data: {
                'cart': productsList,
                'csrfmiddlewaretoken': csrf_token,  // Ensure csrf_token is defined
            },
            success: function(response) {
                localStorage.removeItem('cart');
                document.querySelector('.badge').textContent = response.cart_count;
            },
            error: function(xhr, status, error) {
                $('#response').text('An error occurred while updating the cart.');
            }
        });
    }
    
}