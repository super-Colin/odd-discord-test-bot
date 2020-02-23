
function calcTest(){
    const args = ['2', '+', '2'];
    const inputEquation = args.join("").toString(); // "2 + 2" => "2+2"
    console.log('inputEquation: ' + inputEquation + ', type is:  ' + (typeof inputEquation));

    let digitArray = [...inputEquation.matchAll(/\d+/g)];
    let operatorArray = [...inputEquation.matchAll(/[+-/*]/g)];
    console.log(digitArray);
    console.log(operatorArray);

}
calcTest();


