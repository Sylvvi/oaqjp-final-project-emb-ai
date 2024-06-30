// static/mywebscript.js

let RunSentimentAnalysis = () => {
    let textToAnalyze = document.getElementById("textToAnalyze").value;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            let responseElement = document.getElementById("system_response");
            responseElement.innerHTML = ''; // Clear previous response
            if (this.status == 200) {
                responseElement.innerHTML = xhttp.responseText;
            } else if (this.status == 400) {
                try {
                    let response = JSON.parse(xhttp.responseText);
                    responseElement.innerHTML = response.error;
                } catch (e) {
                    responseElement.innerHTML = "Unexpected error occurred while processing the error message.";
                    console.error("Error parsing response:", e);
                }
            } else {
                responseElement.innerHTML = "Unexpected error occurred.";
                console.error("Error:", xhttp.status, xhttp.statusText, xhttp.responseText);
            }
        }
    };

    xhttp.open("POST", "/emotionDetector", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify({ "text": textToAnalyze });
    xhttp.send(data);
};

