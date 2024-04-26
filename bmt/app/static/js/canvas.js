var canvas = document.querySelector("canvas")
var c = canvas.getContext("2d")

class Seat {
    constructor(x, y, width, height, label){
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.label = label;
        this.color = "yellow"
    }
    draw(c) {
        c.beginPath();
        c.fillStyle = this.color;
        c.fillRect(this.x, this.y, this.width, this.height);
        c.fill();
        c.stroke();
    }
    isClicked(xmouse, ymouse) {
        if ((this.x < xmouse && xmouse < (this.x+this.width)) && (this.y < ymouse && ymouse < (this.y+this.height))){
            return this.label;
        } else {
            return null;
        }
    };
}

var SIZE = 75;
canvas.width = 16 * SIZE;
canvas.height = 9 * SIZE;

schema = {"seats": ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14", "E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12", "E13", "E14", "F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "F14", "G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12", "G13", "G14", "H0", "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "H11", "H12", "H13", "H14"]}

var ROW_NAME = "";
var PREP_SEATS_LAYOUT = {}

for (var i = 0; i < schema["seats"].length; i++) {
    if (schema["seats"][i][0] != ROW_NAME) {
        ROW_NAME = schema["seats"][i][0];
        PREP_SEATS_LAYOUT[ROW_NAME] = [];
        PREP_SEATS_LAYOUT[ROW_NAME].push(schema["seats"][i]);
    } else {
        PREP_SEATS_LAYOUT[ROW_NAME].push(schema["seats"][i]);
    }
}

var MAX_ROW = Object.keys(PREP_SEATS_LAYOUT).length
var MAX_COL = 0;
for (const [k,v] of Object.entries(PREP_SEATS_LAYOUT)) {
    if (v.length > MAX_COL) {
        MAX_COL = v.length;
    }
}

var TWIDTH =canvas.width;
var THEIGHT = canvas.height;

// var X = i*WIDTH + 0.1*TWIDTH;
// var Y = i*HEIGHT + 0.25*THEIGHT;
var HEIGHT = THEIGHT*(0.7/MAX_ROW);
var WIDTH = TWIDTH*(0.8/(MAX_COL-1));
var FACTOR = 0.9;

c.fillRect(0.1*TWIDTH,0.01*THEIGHT, 0.8*TWIDTH, 0.1*THEIGHT)
// c.strokeStyle("black")
// c.strokRect(0,0,100,100)

var j = 0;
var SEATS = []
for (const [k,v] of Object.entries(PREP_SEATS_LAYOUT)) {
    for (var i =0; i<v.length; i++) {
        let a = new Seat(
            (0.1*TWIDTH-(WIDTH/2)) + i*WIDTH,
            0.30*THEIGHT + j*HEIGHT,
            WIDTH*0.9,
            HEIGHT*0.9,
            v[i]
        )
        a.draw(c)
        SEATS.push(a);
    }
    j++;
}

var SELECTED_SEAT = []
let it = document.getElementById("selected-seat")
canvas.addEventListener("click", function(event){
    var seat = SEATS.filter((seat) => {
        if (seat && seat.isClicked(event.clientX, event.clientY)) {
            return seat;
        } else {
            return null
        }
    })
    if (SELECTED_SEAT.find((s) => s == seat[0])){
        SELECTED_SEAT.pop(seat[0]);
        seat[0].color = "yellow";
        seat[0].draw(c)
    } else {
        SELECTED_SEAT.push(seat[0]);
        seat[0].color = "red";
        seat[0].draw(c)
    }
    console.log("selected seat", SELECTED_SEAT);
    it.innerText = "You have selected :"
    SELECTED_SEAT.forEach((element) => {
        it.innerText += element.label + " ";
    });
})

