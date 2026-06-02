const currentHost = window.location.hostname;
const protocol = window.location.protocol;
document.getElementById('btn-pdf').href = protocol + "//" + currentHost + ":9444/";
document.getElementById('btn-weylus').href = protocol + "//" + currentHost + ":9445/";
document.getElementById('btn-touch').href = protocol + "//" + currentHost + ":9446/";

document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('switch-weylus').checked = data["weylus"];
            document.getElementById('switch-pdf').checked = data["pdf-processor"];
            document.getElementById('switch-touchpad').checked = data["remote-touchpad"];
        })
        .catch(err => console.error("Cannot reach to API:", err));
});

function toggleService(serviceName, element) {
    const action = element.checked ? 'start' : 'stop';

    element.disabled = true;

    fetch(`/api/service/${action}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ service: serviceName })
    })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert("Hata: " + (data.error || "Server error. . ."));
                element.checked = !element.checked;
            }
        })
        .catch(err => {
            alert("Connection could not established!");
            element.checked = !element.checked;
        })
        .finally(() => {
            element.disabled = false;
        });
}