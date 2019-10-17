
let activated = false;
function bench() {
    let product = 1.0;
    for (let counter = 1; counter < 1000; counter++) {
        for (let dex = 1; dex < 360; dex++) {
            angle = dex * (Math.PI / 180);
            product *= Math.pow(Math.sin(angle), 2) + Math.pow(Math.cos(angle), 2);
        }
    }
    return product
}
function timeIt(sampleSize, repeats , functionName) {
    let times = [];
    for (let i = 0; i < sampleSize; i++) {
        let t0 = performance.now();
        for (let j = 0; j < repeats; j++) {
            functionName();
        }
        let t1 = performance.now();
        times.push((t1 - t0));
    }
    return times;
}
function main() {
    if (!activated) {
        result = timeIt(10, 10, bench);
        result.sort((a, b) => a - b);
        final_result = Math.floor(((3 - (result[0] / 1000)) * 1/1.8) * 100)
        console.log(final_result);
        activated = true;
        document.getElementById('benchmark').innerHTML = "<h3>Score: " + final_result + "</h3>"
    }
}

