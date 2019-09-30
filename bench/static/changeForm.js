var hello = 3;
console.log(hello);

function myFunction(){
    select = document.getElementById("productType");

    var value = select.options[select.selectedIndex].value;
    console.log(value);
    clearSpecifications();
    if(value == "CPU"){
        getNewText();
    }
}

function clearSpecifications(){
    var table = document.getElementById("table");
    table.innerHTML = "";
}

function getNewText(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        document.getElementById("table").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "static/CPU html.txt", true);
    xhttp.send();
}