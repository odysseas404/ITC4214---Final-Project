const likeButton = document.querySelector("#like-button");
const likeCount = document.querySelector("#like-count");

if (likeButton && likeCount) {
    likeButton.addEventListener("click", function () {
        const likeUrl = this.dataset.likeUrl;

        fetch(likeUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.liked) {
                likeButton.textContent = "♥";
            } else {
                likeButton.textContent = "♡";
            }

            likeCount.textContent = data.like_count;
        });
    });
}

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }

    return cookieValue;
}