// Variable to set the number of squares
var numSquares = 3;
// Get all elements with class 'square' in a variable
var squares = document.querySelectorAll(".square");
// Set the color display variable
var  colorDisplay = document.getElementById("colorDisplay");

var colors;
var pickedColor;

// Variables for h1, reset button and message
var h1Tag = document.querySelector("h1");
var resetButton = document.getElementById("reset");
var msgTxt = document.getElementById("message");

// Call functions - In JS we can call functions before they are actually defined in the script
setupSquares()

resetButton.addEventListener("click", function(){ 
    if (this.textContent == "Play Again?") {
        this.textContent = "New Colors"
        msgTxt.textContent = ""
    } 
    resetColors();
})

// Define function to loop through the elements with class 'square'
function setupSquares() {
    for (var i=0;i < squares.length; i++) {
        // Add callback function event listener for clicks
        squares[i].addEventListener("click", function () {
            if (this.style.backgroundColor == pickedColor) {
                h1Tag.style.backgroundColor = pickedColor;
                msgTxt.textContent = "Correct!"
                resetButton.textContent = "Play Again?"
                changeColors(pickedColor);
            }
            else {
                this.style.backgroundColor = "#232323"
                msgTxt.textContent = "Try Again!"
            }
        })
    }
}

function genRandomColor() {
    // pick a r value between 0 and 255
    var r = Math.floor(Math.random() * 256)     // Math.random generates a value between 0 and 1

    // pick a g value between 0 and 255
    var g = Math.floor(Math.random() * 256) 

    // pick a b value between 0 and 255
    var b = Math.floor(Math.random() * 256) 

    return "rgb(" + r + ", " + g + ", " + b +")";
}

// Higher Order Function
function generateRandomColors(num) {
    var arrColor = new Array();

    for (var i=0; i < num; i++) {
        arrColor.push(genRandomColor())
    }

    return arrColor;
}

// function to select a random color for display
function pickColors() {
    var randomColorIndex = Math.floor(Math.random() * numSquares);
    return colors[randomColorIndex];
}

// function to reset colors
function resetColors () {
    // Reset h1 and message
    h1Tag.style.backgroundColor = "steelblue";
    msgTxt.textContent="";

    colors = generateRandomColors(numSquares);
    pickedColor = pickColors();
    
    // Change text of colorDisplay
    colorDisplay.textContent = pickedColor;
    
    for (var i =0; i < squares.length; i ++) {
        squares[i].style.backgroundColor=colors[i]
    }
}

// Change square colors on correct selection
function changeColors(color) {
    for (var i = 0; i < numSquares; i++) {
        squares[i].style.backgroundColor = color;
    }
}