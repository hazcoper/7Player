
let myHeight = 0
let myWidth = 0

let connection;
let IP;

let mykeypad;
let mypredict



function sendData(command, extra){
    //will receive the command to send to the server and send it in the correct way
    //this is the updated version that is using flask
    //information will be transmitted via get requests

    print("starting sending ", extra);
    const Http = new XMLHttpRequest();
    let url='';

    switch(command){
        case "volume":
            url='http://' + location.hostname + ':4443/volume/' + extra;
            break;
        case "start":
            url='http://' + location.hostname + ':4443/start/' + extra;
            break;
        case "stop":
            url='http://' + location.hostname + ':4443/stop';
            break;
        default:
            print("Command is not valid");
    }

    Http.open("GET", url);
    Http.send();
    print("done sending");
    Http.onreadystatechange = (e) => {
        console.log("Command: " + command + " response: " + Http.responseText)
        messageParser(Http.responseText)
    }

}


function messageParser(myResponse){
    
    if (myResponse === "accepted"){
        mypredict.text = "Começando música";
    }
    else if(myResponse === "volumechange"){
        console.log("Volume Alterado");
        mypredict.text = "Volume Alterado";

    }
    else if(myResponse === "stopped"){
        mypredict.text = "Música Parada";

    }
    else{
        mypredict.text = "Seleção não válida";
        print("I am here ");
    }

    // connection.close();
    // connection = null;
    //event.data vai conter a informacao da mensagem
}


class KeyPad{
    constructor(x, y, sizex, sizey, spaceX, spaceY, numKeys){
        // space x and space y is the space between the boxes
        this.pos = createVector(x,y);
        this.size = createVector(sizex, sizey);
        this.numKeys = numKeys;

        
        var ncolumns =  numKeys/3
        var nrows = 3

        var _sizeX = this.size.x/nrows;
        var _sizeY = this.size.y/ncolumns;

        this.rectList = {};
        this.charList = null;

        for(var counter = 0; counter < numKeys; counter++){
            
            var _startX = _sizeX * (counter % nrows) + spaceX * (counter % nrows);
            var _startY = _sizeY * (counter % ncolumns) + spaceY * (counter % ncolumns); 

            var index = (counter%ncolumns * nrows) + counter%nrows;
            print(index, counter);
            this.rectList[index] = [_startX, _startY, _sizeX, _sizeY];

            
        }

    }   

    setCharList(charList){
        this.charList = charList;
    }
    
    show(){
        push();
        
        translate(this.pos);
        strokeWeight(2);
        // rect(0, 0,this.size.x, this.size.y, 5);

        for(var counter = 0; counter < this.numKeys; counter++){
            
            var _x = this.rectList[counter][0]
            var _y = this.rectList[counter][1]

            var _sizeX = this.rectList[counter][2]
            var _sizeY = this.rectList[counter][3]
            
            fill(49, 107, 131);
            rect(_x, _y, _sizeX, _sizeY, 3);
            
            fill(213, 191, 191);
            textAlign(CENTER, CENTER);
            textSize(40);
            if(this.charList[counter] == int(this.charList[counter])){
                text(String.fromCharCode(this.charList[counter]),_x, _y, _sizeX, _sizeY);
            }else{
                text(this.charList[counter],_x, _y, _sizeX, _sizeY);
            }
            // text(String.fromCharCode(counter + 49),this.rectList[counter][0], this.rectList[counter][1], this.rectList[counter][0]+this.rectList[counter][2], this.rectList[counter][1]+this.rectList[3])
        }
        pop();
    }

    checkHit(mouseX,mouseY){
        // not the fastest version, but prob good enough
        
        for(var counter = 0; counter < this.numKeys; counter++){
            var myRect = this.rectList[counter];

            var startX = myRect[0] + this.pos.x;
            var startY = myRect[1] + this.pos.y;
            var endX = startX + myRect[2];
            var endY = startY + myRect[3];


            if (mouseX > startX && mouseX < endX && mouseY > startY && mouseY < endY){
                console.log("there has been a hit ");
                console.log(counter, "\n");
                return this.charList[counter];
            }
        }

        return null;
    }


    
}

class PredictBox{
    constructor(x, y, sizex, sizey){
        this.pos = createVector(x,y);
        this.size = createVector(sizex, sizey);
        this.text = "";
        
        var textMarginP = 2;
        this.textMarginX = this.size.x * textMarginP / 100
        //need to calculate the font size based on the size of the square
        var nChars = 20;
        var baseChar = "P";
        var baseFontS = 10;

        

        textSize(baseFontS);
        this.textSize = floor( baseFontS * ((this.size.x - 2 * this.textMarginX) / (textWidth(baseChar) * nChars)));

    }   

    show(){
        push();

        translate(this.pos)
        fill(255, 20, 100);
        noFill();
        strokeWeight(2);
        rect(0, 0,this.size.x, this.size.y, 5);
        
        fill(213, 191, 191);
        
        textAlign(LEFT, CENTER);
        textSize(this.textSize);

        text(this.text, this.textMarginX ,0, this.size.x - this.textMarginX, this.size.y);

        pop();
    }

    add(value){
        if(value == 9003){
            //this is delete
            if(this.text.length < 1) return;
            if(this.text === "Começando música" || this.text === "Seleção não válida" || this.text === "Volume Alterado" || this.text === "Música Parada") return;
        
            this.text = this.text.slice(0, -1);
            return;
        
        }
        if(value == 9166){
            //this is enter
            if(this.text.length < 1) return;
            print("THis is going to send")
            sendData("start", this.text);
            return;
        }
        if(value === '🔊'){
            sendData("volume", 5);
                return;
        }
        
        if(value === '🔉'){
            sendData("volume", -5);
            return
        }
        if(value == '🚫'){
            sendData("stop");
            return
        }

        if(value == 101){
            return  
        }

        //if i get here, it means that a number was pressed
        if(this.text === "Começando música" || this.text === "Seleção não válida" || this.text === "Volume Alterado" || this.text === "Música Parada") this.text = "";
        this.text += String.fromCharCode(value);
    }
}

document.addEventListener("visibilitychange", function() {
    if (document.hidden){
        console.log("browser tab is not visable")
    } else {
        console.log("Browser tab is visible")
    }
});

//prevent certain moves on mobile
document.ontouchmove = function(event) {
     event.preventDefault();
};


function viewport(){
    var e = window, a = 'inner';
    if( !( 'innerWidth' in window )){
        a = 'client';
        e = document.documentElement || document.body;
    }
    myWidth = e[a+'Width'];
    myHeight = e[a+'Height'];
    return { width : e[ a+'Width' ] , height : e[ a+'Height' ] }
}

function mouseCallback(event){

    var value = mykeypad.checkHit(event.offsetX, event.offsetY);
    
    if (value === null){
        return;
    }
    
    
    mypredict.add(value);

}

function setup() {

    document.addEventListener("click", mouseCallback);

    // get the screeen dimensions
    viewport();
    pixelDensity(1);
    createCanvas(myWidth, myHeight);
    
    // print(location.hostname);
    
    // print(location.host.split(":")[0])
    // console.log('ws://' + location.host.split(":")[0] + ':4441')
    
    print(myHeight);
    print(myWidth);


    var xMarginP = 5;  //both this values are percentages of the actual size
    var yMarginP = 5;  //both this values are percentages of the actual size

    var yKeypadP = 80;      //percentage of y filled by keypad
    var yPredP = 10;        //percentage of y filled by pred box

    //lets draw the keypad box
    //calculate the actual size of the margin
    var _xMarginS = xMarginP * myWidth  / 100;
    var _yMarginS = yMarginP * myHeight / 100;

    //calculate the acutal size of the box (it will use all available x size)
    var _keypadXSize =  myWidth - 2 * _xMarginS - 2 * 10;
    //y size will the the x size + x size / 3 (to have one extra row)
    var _keypadYSize =  yKeypadP * myHeight / 100 - 3 * 10;

    var _keypadX = _xMarginS; 
    var _keyPadY = myHeight - _yMarginS - _keypadYSize;
    

    var _predictXSize = _keypadXSize + 2 * 10;
    var _predictYSize =  yPredP * myHeight / 100;

    var _predictX = _keypadX;
    var _predictY = _keyPadY - _predictYSize - _yMarginS;

    mykeypad = new KeyPad(_keypadX, _keyPadY, _keypadXSize, _keypadYSize, 10, 10, 15);
    mykeypad.setCharList([ '🔉', '🔊', '🚫', 49, 50, 51, 52, 53, 54, 55, 56, 57, 9003, 48, 9166]);
    mypredict = new PredictBox(_predictX, _predictY, _predictXSize, _predictYSize);
}


// old function to deal with mouse click, does not work with safari
// function mouseClicked(event) {
//     console.log(mouseX, mouseY);
//     var value = mykeypad.checkHit(mouseX, mouseY);
    
//     if (value === null){
//         return;
//     }
    
    
//     mypredict.add(value);

// }


function draw() {
    // background(0, 30);
    background(140, 161, 165);
  

    mykeypad.show();
    mypredict.show();




    // textSize(32);
    // fill(0, 102, 153);
    // text(myWidth, 10, 30);
    // text(myHeight, 10, 60);

  
}
