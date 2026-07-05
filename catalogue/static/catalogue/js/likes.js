const likeButton = document.getElementById("like-button");

if (likeButton) {
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
                likeButton.textContent = "Unlike";
            } else {
                likeButton.textContent = "Like";
            }

            document.getElementById("like-count").textContent = data.like_count;
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