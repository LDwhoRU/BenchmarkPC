

function bench() {
    let product = 1.0;
    for (let counter = 1; counter < 1000; counter++) {
        for (let dex = 1; dex < 360; dex++) {
            angle = Math.radians(dex);
            product *= Math.pow(Math.sin(angle), 2) + Math.pow(Math.cos(angle), 2);
        }
    }
    return product
}
function timeIt(repeats, functionName) {
    let times = [];
    for (let i = 0; i < repeats; i++) {
        let t0 = performance.now();
        functionName();
        let t1 = performance.now();
        times.push(t1 - t0);
    }
    return times;
}

result = timeit.repeat(10, bench);
result.sort((a, b) => b - a);
final_result = ((3 - result[0] * 1 / 1.8) * 100;
console.log(final_result);