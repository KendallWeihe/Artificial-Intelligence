var debugOut = $("#debugText")
var board = {
  //this data structure was heavily discussed with Lydia Brothers. its current form is due to her help
  state: {
    flipped: true,
    ballWasDroppedLastMove: false,
    topPlace: 0,
    bottomPlace: 0,
    top:    [[1,2,3,4,5,6],[7,8,9,10,11,99],[12,13,14,15,99,99],[16,17,18,99,99,99],[19,20,99,99,99,99],[21,99,99,99,99,99]],
    bottom: [[0,0,0,0,0,0],[0,0,0,0,0,99],  [0,0,0,0,99,99],    [0,0,0,99,99,99],   [0,0,99,99,99,99],  [0,99,99,99,99,99]],
  },
  //this method was discussed with Lydia Brothers
  settle: function(){
    this.state.ballWasDroppedLastMove = false;
    //Abandon hope all ye who enter here
    for(var col=0;col<6;col++){
      //figure which top is lined up with which bottom
      var topIndex = (col+this.state.topPlace)%6;
      var botIndex = (col+this.state.bottomPlace)%6;

      //make sure air space at the top.
      this.bubbleTop(topIndex)
      this.bubbleBottom(botIndex)

      //count free space (all the zero cells) on bottom, and the first free slot
      var freeSpace = 0;
      var freeSlot = -1;
      for(var cell in this.state.bottom[botIndex]){
        if(this.state.bottom[botIndex][cell] == 0){
          freeSlot = Number(cell);
          freeSpace += 1;
        }
      }

      //shift that many balls from the top to the bottom
      for(var cell=freeSlot; cell>=0;cell--){
        if( Number(this.state.top[topIndex][freeSlot-cell]) != 99 && Number(this.state.top[topIndex][freeSlot-cell]) != 0 ){
          this.state.bottom[botIndex][cell] = this.state.top[topIndex][freeSlot-cell];
          this.state.top[topIndex][freeSlot-cell] = 0
          this.state.ballWasDroppedLastMove = true;
        }
      }

      //make sure
      this.bubbleTop(topIndex)
    }
  },
  //this method was discussed with Lydia Brothers
  bubbleTop: function(topIndex){
    //bubble empty spaces up for top
    for(var i=0;i<6;i++){
      for(var cell=0; cell<5;cell++){
        if(Number(this.state.top[topIndex][cell+1]) == 99){
          break;
        }else if(Number(this.state.top[topIndex][cell]) == 0 && Number(this.state.top[topIndex][cell+1]) != 0){
          var temp = Number(this.state.top[topIndex][cell])
          this.state.top[topIndex][cell] = this.state.top[topIndex][cell+1]
          this.state.top[topIndex][cell+1] = temp
        }
      }
    }
  },
  //this method was discussed with Lydia Brothers
  bubbleBottom: function(botIndex){
    //bubble empty spaces up for bottom
    for(var i=0;i<6;i++){
      for(var cell=6; cell>=1;cell--){
        if(Number(this.state.bottom[botIndex][cell-1]) == 99){
          continue;
        }else if(Number(this.state.bottom[botIndex][cell]) == 0 && Number(this.state.bottom[botIndex][cell-1]) != 0){
          var temp = Number(this.state.bottom[botIndex][cell])
          this.state.bottom[botIndex][cell] = this.state.bottom[botIndex][cell-1]
          this.state.bottom[botIndex][cell-1] = temp
        }
      }
    }
  },
  rotateLeft: function(){
    this.state.topPlace=(this.state.topPlace+1)%6
    this.update()
  },
  rotateRight: function(){
    this.state.topPlace=(this.state.topPlace+5)%6
    this.update()
  },
  //this method was heavily discussed with Lydia Brothers
  flip: function(){
    //switch the two. this could be done in one less variable (each) but im dumb and its late at night and i messed it up too many times already.
    var newBottom = this.state.top
    var newTop = this.state.bottom
    var newTopPlace = this.state.bottomPlace
    var newBottomPlace = this.state.topPlace

    this.state.top = newTop;
    this.state.bottom = newBottom;
    this.state.topPlace = newTopPlace;
    this.state.bottomPlace = newBottomPlace;
    this.state.flip = !this.state.flip;

    this.update()
  },
  update: function(){
    drawBoard(this.state)
    this.settle()
    setTimeout(function(){drawBoard(board.state);}, 50);
  },
  reset: function(){
    board.state.top =[[1,2,3,4,5,6],[7,8,9,10,11,99],[12,13,14,15,99,99],[16,17,18,99,99,99],[19,20,99,99,99,99],[21,99,99,99,99,99]]
    board.state.bottom = [[0,0,0,0,0,0],[0,0,0,0,0,99],  [0,0,0,0,99,99],    [0,0,0,99,99,99],   [0,0,99,99,99,99],  [0,99,99,99,99,99]]

    board.state.topPlace=0
    board.state.bottomPlace=0
    this.update()
  },
  align: function(){
    this.state.topPlace = (this.state.topPlace - this.state.bottomPlace+6)%6;
    this.state.bottomPlace = 0;
    this.update()
  },
  randomizeColor: function(){
    //assign 21 colors (6 unique) to 21 numbers (all unique)
    var oldColors = colorList.slice();
    var newColors = [];

    //trim colorlist to have 21 colors (6 unique)
    oldColors.splice(0,1)
    oldColors.splice(21,99)

    //pick a random color out of the old list.
    //push it to the front of the new list.
    //repeat till there are no more colors
    while(oldColors.length != 0){
      var colorIndex = Math.floor(Math.random()*(oldColors.length))
      newColors.push(oldColors[colorIndex])
      oldColors.splice(colorIndex,1);
    }

    //untrim new colors to match the list format
    newColors.splice(0,0,"darkgrey")
    newColors[99] = "grey"

    colorList = newColors.slice();
    this.update()
  },
  save: function(returnVal){
    var returnVal = {};
    for(i in this.state){
      returnVal.flipped = this.state.flipped
      returnVal.ballWasDroppedLastMove = this.state.ballWasDroppedLastMove
      returnVal.topPlace = this.state.topPlace
      returnVal.bottomPlace = this.state.bottomPlace
      returnVal.top = []
      for(j in this.state.top){
        returnVal.top.push([])
        for(k in this.state.top[j]){
          returnVal.top[j].push(0)
          returnVal.top[j][k] = this.state.top[j][k]
        }
      }

      returnVal.bottom = []
      for(j in this.state.bottom){
        returnVal.bottom.push([])
        for(k in this.state.bottom[j]){
          returnVal.bottom[j].push(0)
          returnVal.bottom[j][k] = this.state.bottom[j][k]
        }
      }
    }
    return returnVal
  },
  load: function(saveVal){
    for(i in saveVal){
      this.state.flipped = saveVal.flipped
      this.state.ballWasDroppedLastMove = saveVal.ballWasDroppedLastMove
      this.state.topPlace = saveVal.topPlace
      this.state.bottomPlace = saveVal.bottomPlace
      for(j in saveVal.top){
        for(k in saveVal.top[j]){
          this.state.top[j][k] = saveVal.top[j][k]
        }
      }
      for(j in saveVal.bottom){
        for(k in saveVal.bottom[j]){
          this.state.bottom[j][k] = saveVal.bottom[j][k]
        }
      }
    }
    this.update()
  },
}

//initial list of colors, this implementation of colors was discussed with lydia brothers.
//we both agree its a good solution.

var masterColors = [
  "red",
  "green",
  "yellow",
  "blue",
  "white",
  "black"
]
var inverseMasterColors = {
  "red":0,
  "green":1,
  "yellow":2,
  "blue":3,
  "white":4,
  "black":5
}
var colorList = [
  //6 red
  //5 green
  //4 yellow
  //3 blue
  //2 white
  //1 black
  "darkgrey",
  "red","red","red","red","red","red",
  "green","green","green","green","green",
  "yellow","yellow","yellow","yellow",
  "blue","blue","blue",
  "white","white",
  "black"
]
colorList[99] = "grey"

//putting states on global to simplify things
stateLists = {
  moveList: [0],
  boardState:[],
}
//a method of displaying the board. it works, surprisingly.
function drawBoard(boardState){
  //i honestly cant understand my own code anymore. im going to leave this one alone...
  //grab display board
  var displayBoard = $("#board")
  //empty display Board
  displayBoard.empty()
  for(var i=11;i>=0;i--){
    //make rows
    var row = document.createElement("tr")
    for(var j=0;j<6;j++){
      var jTop = ((j+boardState.topPlace)%6);
      var jBottom = ((j+boardState.bottomPlace)%6);
      //make cols (aka cells)
      var cell = document.createElement("td")
      $(cell).css({
        height: 30,
        width: 30,
        "text-align": "center",
        backgroundColor: "orange",
      })

      //top board
      if(i>5){
        $(cell).text(boardState.top[jTop][i-6])
        $(cell).css({
          backgroundColor: colorList[boardState.top[jTop][i-6]],
        })
      }
      //bottom board
      else{
        $(cell).text(boardState.bottom[jBottom][5-i])
        $(cell).css({
          backgroundColor: colorList[boardState.bottom[jBottom][5-i]],
        })
      }

      $(row).append(cell)
      //add col to row
    }
    displayBoard.append(row)
    //add row to display
  }
  return 0;
}

function magicSolve(){
  getKFromSolvedState(board,Number($("#kmoves").val()));
}
function GrandfatherParadox(){
  getKFromSolvedState(board,Number($("#kmoves").val()));
  playLastKMoves(Number($("#kmoves").val()))
}
//gets a state that is k moves from being solved.
//discussed heavily on the canvas discussion board, most notably with Evan Heaton
//but also with Spenser King, Lydia Brothers, a little bit Robert Mcgillverey, and Dr. Goldsmith
function getKFromSolvedState(pboard,k){
  stateLists = {
    moveList: [0],
    boardState:[],
  }
  stateLists.boardState.push(pboard.save());

  //do k random moves
  for(var count=0;count<k;count++){
    randomLegalMove(pboard,stateLists)
    //setTimeout(function(){randomLegalMove(board,stateLists)}, 800*count);
  }

  //if its already in a flat state, force a non flat state
  if(flatCheck(pboard)){
    //if the top and bottom are lined up first rotate then flip
    if(((pboard.state.topPlace - pboard.state.bottomPlace+6)%6) == 0){

      specificLegalMove(pboard,1)
      stateLists.moveList.push(1)
      stateLists.boardState.push(pboard.save());
    }

    specificLegalMove(pboard,0)
    stateLists.moveList.push(0)
    stateLists.boardState.push(pboard.save());
  }

  //keep making moves until its flat (it'll get there eventually)
  var itWentTooLong = 0
  var tooLong = 200
  while(!flatCheck(pboard) && itWentTooLong<tooLong){
    randomLegalMove(pboard,stateLists)
    itWentTooLong++
  }

  //for when it inevitably just does not get there (I gave it 100 moves, that should be plenty)
  while(itWentTooLong == tooLong && !flatCheck(pboard)){
    console.log("it took too long to get to a flat state", tooLong)
    specificLegalMove(pboard,1)
    stateLists.moveList.push(1)
    stateLists.boardState.push(pboard.save());
  }

  //now make sure the top and bottom are lined up in the least amount of moves.
  //find which direction is less, left or right
  var centeringCounter=0;
  var adjTop = (pboard.state.topPlace - pboard.state.bottomPlace+6)%6;
  while(pboard.state.topPlace - pboard.state.bottomPlace!=0){
    centeringCounter++
    if(adjTop > 3){
      //go left
      specificLegalMove(pboard,1)
      stateLists.moveList.push(1)
      stateLists.boardState.push(pboard.save());
    }else{
      //go right
      specificLegalMove(pboard,2)
      stateLists.moveList.push(2)
      stateLists.boardState.push(pboard.save());
    }
  }
  /*console.log(k + " moves to k")
  console.log(itWentTooLong + " moves to flat")
  console.log(centeringCounter + " moves to center")
  console.log("--------------==-------------")*/

  //cheat in the solution
  cheatySolve(pboard)

  //go back in time to the k moves back state.
  pboard.load(stateLists.boardState[stateLists.boardState.length-1-k])
  //print out solution in debug for prosperity
  var moveReadable = ["flip","left","right"]
  $("#debugText").empty()
  var csvContent = "data:text/csv;charset=utf-8,"
  for(count=0;count<k;count++){
    var moveIndex = stateLists.moveList.length-k+count
    // console.log(moveReadable[stateLists.moveList[moveIndex]])
    csvContent += moveReadable[stateLists.moveList[moveIndex]] + ","
    $("#debugText").append("<br></br>"+moveReadable[stateLists.moveList[moveIndex]]+
                            " | move #: " + (stateLists.moveList.length - moveIndex-1) +
                            " >= h #: " + h(stateLists.boardState[moveIndex]) +
                            " = " + ((stateLists.moveList.length - moveIndex-1) >= h(stateLists.boardState[moveIndex])))
    if(!((stateLists.moveList.length - moveIndex-1) >= h(stateLists.boardState[moveIndex]))){
      alert("something is wrong");//this should never run
    }
  }
  // console.log(csvContent)
  // var encodedUri = encodeURI(csvContent);
  // var link = document.createElement("a");
  // link.setAttribute("href", encodedUri);
  // link.setAttribute("download", "my_data.csv");
  // document.body.appendChild(link); // Required for FF
  //
  // link.click();
  // console.log(stateLists.moveList)
  console.log(stateLists)
  
}
var h = function(boardState){
  //h1
  //for every bottom tube that has a ball of the wrong color in it +2
  //for every top tube that has a ball
  var hCount = 0
  var movesTillCenter = -Math.abs(Math.abs(boardState.bottomPlace - boardState.topPlace)-3)+3;
  var maxMovesTillFilled = 0;
  var misplacedTopBalls = false;
  var misplacedBottomBalls = false;
  for(i in boardState.bottom){
    var topIndex = (boardState.topPlace-i+6)%6;
    var botIndex = (boardState.bottomPlace-i+6)%6
    for(j in boardState.bottom[i]){
      if(!(Number(boardState.bottom[i][j]) == 0 || Number(boardState.bottom[i][j]) == 99) && (colorList[boardState.bottom[i][j]] != masterColors[i])){
        misplacedBottomBalls = true;
      }
      if(!(Number(boardState.top[topIndex][j]) == 0 || Number(boardState.top[topIndex][j]) == 99)){
        misplacedTopBalls = true;
      }
    }
  }

  hCount+=movesTillCenter

  if(misplacedBottomBalls){
    hCount+=1;
  }

  if(misplacedTopBalls){
    hCount = Math.max(hCount,1)
  }
  return hCount
}

//this function plays back the last k moves.
function playLastKMoves(k){
  var timing = 300;
  var specialcount = 0;
  for(count=1;count<=k;){
    count++;
    setTimeout(function(){
      specificLegalMove(board,stateLists.moveList[stateLists.moveList.length-k+specialcount])
      specialcount++;
    }, timing*count);
  }
}
function randomLegalMove(pboard,stateLists){

  //validMoves is a array that stores an array that contains a function to either flip,left,or right
  //and 0,1,2 (which correspond to the move list definition above).
  var validMoves = []

  //if last move wasnt a flip, means its a valid move, add it to the list.
  if(stateLists.moveList[stateLists.moveList.length-1] != 0){
    validMoves.push(0);
  }
  //if the last move wasnt (a right and no ball was dropped), left is valid add it to the list
  if(stateLists.moveList[stateLists.moveList.length-1] != 2 || pboard.state.ballWasDroppedLastMove){
    validMoves.push(1);
  }
  //if the same but reverse of above
  if(stateLists.moveList[stateLists.moveList.length-1] != 1 || pboard.state.ballWasDroppedLastMove){
    validMoves.push(2);
  }

  var selectedMove = Math.floor(Math.random()*validMoves.length);

  //run the correct function
  if(validMoves[selectedMove]==0){
    pboard.flip()
  }
  if(validMoves[selectedMove]==1){
    pboard.rotateLeft()
  }
  if(validMoves[selectedMove]==2){
    pboard.rotateRight()
  }

  //push move for later recollection
  //push current board state for later recollection
  stateLists.moveList.push(validMoves[selectedMove])
  stateLists.boardState.push(pboard.save());


}
function specificLegalMove(pboard,move){

  //run the correct function
  if(move==0){
    pboard.flip()
  }
  if(move==1){
    pboard.rotateLeft()
  }
  if(move==2){
    pboard.rotateRight()
  }
}
function flatCheck(pboard){
  for(col in pboard.state.bottom){
    for(cell in pboard.state.bottom[col]){
      if(Number(pboard.state.bottom[col][cell]) == 0){
        return false;
      }
    }
  }
  return true;
}
function cheatySolve(pboard){
  //make sure in flat state.
  //this will be a check later on instead of just this.
  if(!flatCheck(pboard)){
    return;
  }
  //reassign colors
  for(col in pboard.state.bottom){
    for(cell in pboard.state.bottom[col]){
      if(Number(pboard.state.bottom[col][cell]) != 99 && Number(pboard.state.bottom[col][cell]) != 0){
        colorList[pboard.state.bottom[col][cell]] = masterColors[col];
      }
    }
  }
  pboard.update()
}


window.onload = function(){
	board.settle()
	drawBoard(board.state)
}
