// Gets the data of the seat available and seats occupied for show
schema = getJSON("seats-available")
seats_occ = getJSON("seats-occupied")

var canvas = document.querySelector("canvas")
var ctx = canvas.getContext("2d")

AVAILABLE_SEAT_COLOR = "#d0c8ea"
OCCUPIED_SEAT_COLOR = "#8f7ece"
SELECTED_SEAT_COLOR = "#553fa6"

// class to represent seat in canvas
class Seat {
    constructor(x, y, width, height, label){
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.reserved = false;
        this.label = label;
        this.selected = false;
    }
    draw(context) {
        if (this.selected && !this.reserved) {
            context.fillStyle = SELECTED_SEAT_COLOR;
        } else {
            context.fillStyle = AVAILABLE_SEAT_COLOR;
        }
        // check if already reserved
        if (seats_occ.find((i) => i == this.label)) {
            context.fillStyle = OCCUPIED_SEAT_COLOR;
            this.reserved = true;
        }
        context.fillRect(this.x, this.y, this.width, this.height);
    }
    isClicked(xmouse, ymouse) {
        if ((this.x < xmouse && xmouse < (this.x+this.width)) && (this.y < ymouse && ymouse < (this.y+this.height))){
            return this.label;
        } else {
            return null;
        }
    };
}

// General method to get data from Document
function getJSON(elid) {
    var i = document.getElementById(elid).innerText
    return JSON.parse(i.replaceAll("'", '"'));    
}


var SIZE = 75;
canvas.width = 16 * SIZE;
canvas.height = 9 * SIZE;

var ROW_NAME = "";
var PREP_SEATS_LAYOUT = {}
// creates the object to represent data friendlier format to render
for (var i = 0; i < schema["seats"].length; i++) {
    if (schema["seats"][i][0] != ROW_NAME) {
        ROW_NAME = schema["seats"][i][0];
        PREP_SEATS_LAYOUT[ROW_NAME] = [];
        PREP_SEATS_LAYOUT[ROW_NAME].push(schema["seats"][i]);
    } else {
        PREP_SEATS_LAYOUT[ROW_NAME].push(schema["seats"][i]);
    }
}


// get no of rows and cols to nicely  prepare layout
var MAX_ROW = Object.keys(PREP_SEATS_LAYOUT).length
var MAX_COL = 0;
for (const [k,v] of Object.entries(PREP_SEATS_LAYOUT)) {
    if (v.length > MAX_COL) {
        MAX_COL = v.length;
    }
}

var TWIDTH =canvas.width;
var THEIGHT = canvas.height;


var HEIGHT = THEIGHT*(0.7/MAX_ROW);
var WIDTH = TWIDTH*(0.8/(MAX_COL-1));
var FACTOR = 0.9;

var THEATER_COLOR = "#8f7ece";

// draws the theater
// c.strokRect(0,0,100,100)
ctx.fillStyle = THEATER_COLOR;
ctx.fillRect(0.1*TWIDTH,0.01*THEIGHT, 0.8*TWIDTH, 0.1*THEIGHT)

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
        a.draw(ctx)
        SEATS.push(a);
    }
    j++;
}

var SELECTED_SEAT = []
let it = document.getElementById("selected-seat")
canvas.addEventListener("click", function(event){
    // Check if the seat was clicked
    var seat = SEATS.filter((s) => {
        if (s && s.isClicked(event.offsetX, event.offsetY) && !s.reserved) {
            return s;
        } else {
            return null
        }
    })
    if (Boolean(seat[0])) {
        if (SELECTED_SEAT.find((s) => s == seat[0])){
            SELECTED_SEAT.splice(SELECTED_SEAT.findIndex((i) => i==seat[0]), 1);
            seat[0].selected = false;
            seat[0].draw(ctx)
        } else {
            SELECTED_SEAT.push(seat[0]);
            seat[0].selected = true;
            seat[0].draw(ctx)
        }
        it.value = ""
        console.log("selected seat", SELECTED_SEAT);
        SELECTED_SEAT.forEach((i) => {
            it.value += i.label + " ";
        });
    }
})

