var hello = 3;
console.log(hello);
function resetDropdown(){
    document.getElementById("productType").selectedIndex = 0;
    myFunction();
    console.log("load");
}
function myFunction(){
    var select = document.getElementById("productType");
    var value = select.options[select.selectedIndex].value;
    if(value == "CPU"){
        document.getElementById('benchmarkTemp').innerHTML = `<div id="benchmark" class="benchmark-button" onclick="main()">
        <h2>Benchmark Score</h2>
        <h5>Click here to Benchmark</h5>
    </div>`;
    }
    else{
        document.getElementById('benchmarkTemp').innerHTML = "";
    }
    console.log(value);
    clearSpecifications();
    var submit = document.getElementById("submit");
    var text = document.getElementById('ProductText');

    if(value != "default"){
        getNewText(value);
        submit.disabled = false;
    }else{
        submit.disabled = true;
        text.innerText = "Choose A Product Type At The Top Of The Page First";
    }
        
    
    
    
}

function clearSpecifications(){
    var table = document.getElementById("table");
    var text = document.getElementById('ProductText');
    text.innerText = "";
    table.innerHTML = "";
}

function getNewText(value){
    clearSpecifications();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        document.getElementById("table").innerHTML = this.responseText;
        }
    };
    switch(value){
        case "CPU":
            xhttp.open("GET", "static/formTemplates/CPUHTML.html", true);
            break;
        case "CPU Cooler":
            xhttp.open("GET", "static/formTemplates/CPUCoolerHTML.html", true);
            break;
        case "Case":
            xhttp.open("GET", "static/formTemplates/CaseHTML.html", true);
            break;
        case "Power Supply":
                xhttp.open("GET", "static/formTemplates/PowerSupplyHTML.html", true);
                break;
        case "Memory":
            xhttp.open("GET", "static/formTemplates/memoryHTML.html", true);
            break;
        case "Graphics Card":
                    xhttp.open("GET", "static/formTemplates/GPUHTML.html", true);
                    break;
        case "Motherboard":
                    xhttp.open("GET", "static/formTemplates/MotherboardHTML.html", true);
                    break;

    }
    xhttp.send();
}

window.onload = function() {
    resetDropdown();
    document.getElementById('inputGroupFile01').onchange = function (evt) {
        var tgt = evt.target || window.event.srcElement,
            files = tgt.files;
    
        // FileReader support
        if (FileReader && files && files.length) {
            var fr = new FileReader();
            fr.onload = function () {
                document.getElementById('img1').src = fr.result;
            }
            fr.readAsDataURL(files[0]);
        }}
  };

  