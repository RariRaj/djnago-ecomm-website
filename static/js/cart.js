var updateBtns = document.getElementsByClassName('update-cart')
// console.log(updateBtns)
for(var i=0; i<updateBtns.length; i++)
{
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log("productId:",productId,"action:",action)

        console.log("USER:",user)
        if (user == 'AnonymousUser')
        {
            console.log("YOU ARE NOT LOGGED IN")
            addCookieItem(productId,action)
        }
        else{

            updateUserOrder(productId,action)

        }

    })
}

function updateUserOrder(productId,action){
    console.log("User is authenticated,Sending data..")
    //set url variable to view -updateItem
    var url = '/update_item'

    //use fetch api to post data to updateItem view
    //The Fetch API is a modern interface that allows you to make HTTP requests to servers from web browsers
    fetch(url, {
        method : 'POST',  // *GET, POST, PUT, DELETE, etc.
        headers : {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrftoken ,
        },
        body:JSON.stringify({'productId':productId,'action':action})  // body data type must match "Content-Type" header
    })
    .then((response) => {
        return response.json();  // parses JSON response into native JavaScript objects
    })
    .then((data) => {
        console.log("Data:",data)   // JSON data parsed by `data.json()` call
        location.reload()
    });

}


function addCookieItem(productId,action){
    console.log("You are not authenticated")
    if(action == 'add'){

        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }
        else{
            cart[productId]['quantity'] += 1
        }
            
    }
    if(action == 'remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            console.log("Item should be deleted")
            delete cart[productId]
        }
    }

    
    console.log('Cart:',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

    location.reload()
}

