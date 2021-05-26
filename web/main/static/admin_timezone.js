function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function setTimeZone(csrf_token, url) {
    let data = {
        "timezone": Intl.DateTimeFormat().resolvedOptions().timeZone,
    }
    $.ajax({
        headers: {
            "X-CSRFToken": csrf_token
        },
        url: url,
        data: data,
        type: 'post',
    })
}

