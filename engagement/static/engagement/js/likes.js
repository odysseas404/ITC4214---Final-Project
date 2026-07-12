//The like button is selected from the page.
const likeButton = document.querySelector("#like-button");

//The like count is selected from the page.
const likeCount = document.querySelector("#like-count");

//Checks that both elements exist, before adding the click event.
if (likeButton && likeCount) {

    //Run this code when the user clicks the like button.
    likeButton.addEventListener("click", function () {
        
        //Get the URL for the like request from the button's data-like-url attribute.
        const likeUrl = this.dataset.likeUrl;

        //Send a POST request to Django to like or unlike the camera.
        fetch(likeUrl, {
            method: "POST",
            headers: {

                //Send the CSRF token required by Django for POST requests.
                "X-CSRFToken": getCookie("csrftoken"),

                //Identifies this request as an AJAX request.
                "X-Requested-With": "XMLHttpRequest"
            }
        })

        //Convert the response from Django into JSON.
        .then(function (response) {
            return response.json();
        })


        //Use the JSON data returned by Django to update the page.  
        .then(function (data) {

            //If the camera is now liked, show a filled heart icon.
            if (data.liked) {
                likeButton.textContent = "♥";

            //If the camera is unliked, show an empty heart icon.
            } else {
                likeButton.textContent = "♡";
            }

            //Update the number of likes displayed on the page.
            likeCount.textContent = data.like_count;
        });
    });
}

//This function gets a specific cookie by name and is used to get Django's CSRF token.
function getCookie(name) {
    let cookieValue = null;

    //Check that cookies exist.
    if (document.cookie && document.cookie !== "") {

        //Split all cookies into separate items.
        const cookies = document.cookie.split(";");

        //Loop through all cookies.
        for (let i = 0; i < cookies.length; i++) {

            //Remove extra spaces from the current cookie.
            const cookie = cookies[i].trim();

            //Check if this cookie is the one we are looking for.
            if (cookie.substring(0, name.length + 1) === (name + "=")) {

                //Decode and store the cookie value.
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                //Stop the loop because the cookie was found.
                break;
            }
        }
    }

    //Return the cookie value.
    return cookieValue;
}