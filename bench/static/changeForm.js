var hello = 3;
console.log(hello);

function myFunction(){
    select = document.getElementById("productType");

    var value = select.options[select.selectedIndex].value;
    console.log(value);
    clearSpecifications();
    if(value != "default"){
        getNewText(value);
    }
}

function clearSpecifications(){
    var table = document.getElementById("table");
    table.innerHTML = "";
}

function getNewText(value){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        document.getElementById("table").innerHTML = this.responseText;
        }
    };
    switch(value){
        case "CPU":
            xhttp.open("GET", "static/CPU html.html", true);
            break;
        case "CPU Cooler":
            xhttp.open("GET", "static/CPUCoolerHTML .html", true);
            break;



    }
    xhttp.send();
}