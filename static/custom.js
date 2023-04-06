document.addEventListener("DOMContentLoaded", () => {
    error_message = document.getElementsByClassName("error-message")[0]

    document.getElementById("form").addEventListener("submit", (e) => {
        error_message.innerHTML = ""

        e.preventDefault();

        var formData = new FormData(document.getElementById("form"));
        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = () => {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                json_response = JSON.parse(xhr.responseText);
                if ("error" in json_response) {
                    error_message.innerHTML = json_response["error"]
                }
            } else if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 302) {
                window.location.href = "/"
            } else if(xhr.readyState === XMLHttpRequest.DONE && xhr.status !== 200) {
                error_message.innerHTML = "An error occured, please try again later."
            }
        }
        xhr.open("POST", document.getElementById("form").attributes.action.value, true);
        xhr.setRequestHeader('Content-type', 'application/json');
        data = {email: formData.get("email"), password: formData.get("password")}
        console.log(JSON.stringify(data))
        xhr.send(JSON.stringify(data))
    })
})