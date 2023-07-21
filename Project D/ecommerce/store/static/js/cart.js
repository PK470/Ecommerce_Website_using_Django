console.log("hello");
var upBtn = document.getElementsByClassName('update-cart');

for (var i = 0; i < upBtn.length; i++) {
    
    upBtn[i].addEventListener('click', function() {
        
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'action:', action)

        console.log('User:', user);
        if (user === 'AnonymousUser') {
            console.log('Not Logged in');
            alert("Please Login");
            window.location.assign("{% url 'login' %}");
        } else {
            updateUserOrder(productId, action);
        }
    });
}

function updateUserOrder(productId, action) {
    console.log('sending Data...');
    var url = '/updateItem/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action
        })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        location.reload();
        
    });
}