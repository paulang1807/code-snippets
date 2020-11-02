function convToFarenheit(varTemp) {
  convTemp=(varTempVal * 9/5) + 32;
  //console.log("Temp in Celcius is:" + convTemp + "C");
  return "Temp in Farenheit is: " + convTemp.toFixed(2) + "&deg;F";
}


function convToCelcius(varTemp) {
  convTemp=(varTempVal - 32)* 5/9;
  //console.log("Temp in Farenheit is:" + convTemp + "F");
  return "Temp in Celcius is: " + convTemp.toFixed(2) + "&deg;C";
}


function callConvTemp(varTemp) {
  //varTemp = prompt("Enter a temp");
  varTempVal = Number(varTemp.substr(0, varTemp.length - 1));
  if (isNaN(varTempVal)) {
    alert("Invalid Input. Please try again.")
  }
  else {
    varTempTyp = varTemp.slice(-1).toUpperCase();
    switch (varTempTyp){
    case 'F':
      //return convToFarenheit(varTempVal);
      document.getElementById('rslt').innerHTML=convToFarenheit(varTempVal);
      document.getElementById('rslt').style.color='green';
      break;
    case 'C':
      //return convToCelcius(varTempVal);
      document.getElementById('rslt').innerHTML=convToCelcius(varTempVal);
      document.getElementById('rslt').style.color='red';
      break;
    default:
      console.log("Please specify C or F along with the temperature.");
      alert("Please specify C or F along with the temperature")
  }
}
}
