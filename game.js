const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const WIDTH = 1000;
const HEIGHT = 700;

// =========================
// VIDEOS
// =========================

const introVideo = document.getElementById("introVideo");
const homeVideo = document.getElementById("homeVideo");

// =========================
// AUDIO
// =========================

const bgMusic = document.getElementById("bgMusic");
const clickSound = document.getElementById("clickSound");
const appleSound = document.getElementById("appleSound");
const sweetSound = document.getElementById("sweetSound");
const winnerSound = document.getElementById("winnerSound");

// =========================
// IMAGES
// =========================



const sweetImage = new Image();
sweetImage.src = "assets/sweet.png"; // put your candy image here


const gameTemplate = new Image();
gameTemplate.src = "assets/game_template.png";

const winnerTemplate = new Image();
winnerTemplate.src = "assets/winner_template.png";


sweetImage.onload = () => {
    console.log("Candy image loaded");
};


// =========================
// GAME STATE
// =========================

let selectedTime = null;
let controlMode = null;

let currentScreen = "intro";

let mouseX = 0;
let mouseY = 0;

// =========================
// HOME BUTTONS
// =========================

const btn15 = {
    x:125,
    y:180,
    w:130,
    h:50
};

const btn30 = {
    x:330,
    y:180,
    w:130,
    h:50
};

const btn45 = {
    x:540,
    y:185,
    w:130,
    h:50
};

const btn60 = {
    x:750,
    y:185,
    w:130,
    h:50
};

const wasdBtn = {
    x:150,
    y:440,
    w:160,
    h:60
};

const arrowsBtn = {
    x:650,
    y:440,
    w:180,
    h:60
};

const playBtn = {
    x:720,
    y:45,
    w:180,
    h:70
};

const startBtn = {
    x:430,
    y:430,
    w:130,
    h:55
};

let showWarning = false;

// =========================
// HELPERS
// =========================

function inside(rect,x,y){
    return (
        x >= rect.x &&
        x <= rect.x + rect.w &&
        y >= rect.y &&
        y <= rect.y + rect.h
    );
}

function playSound(sound){
    try{
        sound.currentTime = 0;
        sound.play();
    }
    catch(err){}
}

// =========================
// INTRO VIDEO LOOP
// =========================

introVideo.addEventListener("timeupdate", () => {

    if (currentScreen !== "intro") return;

    if (!introVideo.duration) return;

    const startPoint = 2.5;
    const endPoint = introVideo.duration - 1.5;

    if (introVideo.currentTime >= endPoint) {

        introVideo.currentTime = startPoint;

        introVideo.play().catch(()=>{});

    }

});

// =========================
// HOME VIDEO LOOP
// =========================

homeVideo.addEventListener("timeupdate",()=>{

    if(
        homeVideo.currentTime
        >=
        homeVideo.duration - 3.169
    ){

        homeVideo.currentTime = 1.3;

        homeVideo.play();
    }

});

// =========================
// MOUSE CLICK
// =========================

canvas.addEventListener("click",(e)=>{

    const rect = canvas.getBoundingClientRect();

    const x =
        (e.clientX - rect.left) *
        (WIDTH / rect.width);

    const y =
        (e.clientY - rect.top) *
        (HEIGHT / rect.height);

    // HOME SCREEN
    if(currentScreen === "home"){

        if(inside(btn15,x,y)){
            selectedTime = 15;
            playSound(clickSound);
        }

        else if(inside(btn30,x,y)){
            selectedTime = 30;
            playSound(clickSound);
        }

        else if(inside(btn45,x,y)){
            selectedTime = 45;
            playSound(clickSound);
        }

        else if(inside(btn60,x,y)){
            selectedTime = 60;
            playSound(clickSound);
        }

        else if(inside(wasdBtn,x,y)){
            controlMode = "WASD";
            playSound(clickSound);
        }

        else if(inside(arrowsBtn,x,y)){
            controlMode = "ARROWS";
            playSound(clickSound);
        }

        else if(inside(playBtn,x,y)){

            if(
                selectedTime === null ||
                controlMode === null
            ){
                showWarning = true;
            }
            else{

                playSound(clickSound);

                startGame();
            }
        }
    }

});

// =========================
// INTRO CLICK
// =========================

document.addEventListener("click",()=>{

    if(currentScreen === "intro"){

        bgMusic.volume = 0.5;

        bgMusic.play().catch(()=>{});

        introVideo.classList.add("hidden");

        homeVideo.classList.remove("hidden");

        homeVideo.play();

        canvas.classList.remove("hidden");

        currentScreen = "home";
    }

},{once:true});

// =========================
// PLAYERS
// =========================

const players = [
    {
        name:"Player 1",
        color:"#dc4646"
    },
    {
        name:"Player 2",
        color:"#468cff"
    },
    {
        name:"Player 3",
        color:"#3cc850"
    },
    {
        name:"Player 4",
        color:"#b450ff"
    }
];

// =========================
// CONTROLS
// =========================

const CONTROL_MAP = {

    WASD:{
        KeyW:0,
        KeyA:1,
        KeyS:2,
        KeyD:3
    },

    ARROWS:{
        ArrowUp:0,
        ArrowLeft:1,
        ArrowDown:2,
        ArrowRight:3
    }
};

// =========================
// GAME VARIABLES
// =========================

let scores = [0,0,0,0];

let item = null;

let itemSpawnTime = 0;

let nextSpawn = 0;

let gameStartTime = 0;

let totalGameTime = 0;

let remainingTime = 0;

// =========================
// SPAWN ITEM
// =========================

function spawnItem(){

    return {

        type:
            Math.random() < 0.5
            ? "apple"
            : "sweet"
    };
}

// =========================
// START GAME
// =========================

function startGame(){

    currentScreen = "game";

    scores = [0,0,0,0];

    item = null;

    nextSpawn =
        performance.now()
        +
        (
            500 +
            Math.random() * 2000
        );

    gameStartTime = performance.now();

    totalGameTime =
        selectedTime * 1000;
}

// =========================
// KEY PRESS
// =========================

document.addEventListener(
    "keydown",
    (e)=>{

        if(
            currentScreen !== "game"
        ) return;

        if(!item) return;

        const mapping =
            CONTROL_MAP[
                controlMode
            ];

        if(
            e.code in mapping
        ){

            const playerIndex =
                mapping[e.code];

            if(
                item.type === "apple"
            ){

                scores[playerIndex]++;

                playSound(
                    appleSound
                );
            }

            else{

                scores[playerIndex] -= 2;

                playSound(
                    sweetSound
                );
            }

            item = null;

            nextSpawn =
                performance.now()
                +
                (
                    500 +
                    Math.random() * 2000
                );
        }
    }
);

// =========================
// DRAW APPLE
// =========================

function drawApple(){

    const cx = WIDTH/2;
    const cy = HEIGHT/2;

    // body (slightly irregular apple shape)
    ctx.fillStyle = "#e53935";
    ctx.beginPath();
    ctx.ellipse(cx, cy, 30, 38, 0, 0, Math.PI * 2);
    ctx.fill();

    // highlight
    ctx.fillStyle = "rgba(255,255,255,0.25)";
    ctx.beginPath();
    ctx.ellipse(cx - 10, cy - 10, 10, 18, 0, 0, Math.PI * 2);
    ctx.fill();

    // stem
    ctx.strokeStyle = "#5d4037";
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(cx, cy - 38);
    ctx.lineTo(cx, cy - 55);
    ctx.stroke();

    // leaf
    ctx.fillStyle = "#43a047";
    ctx.beginPath();
    ctx.ellipse(cx + 12, cy - 45, 12, 6, -0.5, 0, Math.PI * 2);
    ctx.fill();
}

// =========================
// DRAW SWEET
// =========================

function drawSweet(){

    const cx = WIDTH / 2;
    const cy = HEIGHT / 2;

    const size = 120; // adjust size if needed

    // draw only when image is loaded
    if (sweetImage.complete) {
        ctx.drawImage(
            sweetImage,
            cx - size / 2,
            cy - size / 2,
            size,
            size
        );
    }
}


// =========================
// WINNER SCREEN VARIABLES
// =========================

let winnerParticles = [];

let winnerScores = [];

let winnerIndex = 0;

let isTie = false;

// =========================
// CREATE CONFETTI
// =========================

function createWinnerParticles(){

    winnerParticles = [];

    const colors = [
        "#ff5050",
        "#508cff",
        "#50dc78",
        "#ffd850",
        "#b450ff"
    ];

    for(let i=0;i<200;i++){

        winnerParticles.push({

            x: Math.random()*WIDTH,

            y: Math.random()*-HEIGHT,

            speed:
                2 + Math.random()*4,

            size:
                3 + Math.random()*3,

            color:
                colors[
                    Math.floor(
                        Math.random()
                        *
                        colors.length
                    )
                ]
        });
    }
}

// =========================
// SHOW WINNER SCREEN
// =========================

function showWinnerScreen(){

    winnerScores = [...scores];

    const maxScore =
        Math.max(...scores);

    const winners =
        scores.filter(
            s=>s===maxScore
        ).length;

    isTie = winners > 1;

    winnerIndex =
        scores.indexOf(
            maxScore
        );

    if(
        !isTie &&
        winnerSound
    ){
        playSound(
            winnerSound
        );
    }

    createWinnerParticles();

    currentScreen = "winner";
}

// =========================
// WINNER CONTROLS
// =========================

document.addEventListener(
    "keydown",
    (e)=>{

        if(
            currentScreen !==
            "winner"
        ) return;

        if(
            e.code === "Space"
        ){

            selectedTime = null;

            controlMode = null;

            showWarning = false;

            currentScreen = "home";

            homeVideo.currentTime = 1.3;

            homeVideo.play();
        }

        if(
            e.code === "Escape"
        ){

            location.reload();
        }
    }
);

// =========================
// DRAW GAME SCREEN
// =========================

function drawGame(){

    ctx.drawImage(
        gameTemplate,
        0,
        0,
        WIDTH,
        HEIGHT
    );

    const now =
        performance.now();

    remainingTime =
        Math.max(
            0,
            Math.floor(
                (
                    totalGameTime
                    -
                    (
                        now
                        -
                        gameStartTime
                    )
                )
                /
                1000
            )
        );

    if(
        now - gameStartTime
        >= totalGameTime
    ){

        showWinnerScreen();

        return;
    }

    // TIMER

    ctx.fillStyle =
        "black";

    ctx.font =
        "bold 36px Comic Sans MS";

    ctx.fillText(
        remainingTime,
        485,
        60
    );

    // SCORES

    ctx.font =
        "bold 42px Comic Sans MS";

    ctx.fillText(
        scores[0],
        55,
        165
    );

    ctx.fillText(
        scores[1],
        55,
        665
    );

    ctx.fillText(
        scores[2],
        925,
        145
    );

    ctx.fillText(
        scores[3],
        925,
        655
    );

    // SPAWN

    if(
        !item &&
        now >= nextSpawn
    ){

        item = spawnItem();

        itemSpawnTime = now;
    }

    if(
        item &&
        now -
        itemSpawnTime
        >= 1500
    ){

        item = null;

        nextSpawn =
            now
            +
            (
                500
                +
                Math.random()
                *
                2000
            );
    }

    if(item){

        if(
            item.type ===
            "apple"
        ){
            drawApple();
        }
        else{
            drawSweet();
        }
    }
}

// =========================
// DRAW WINNER SCREEN
// =========================

function drawWinnerScreen(){

    ctx.drawImage(
        winnerTemplate,
        0,
        0,
        WIDTH,
        HEIGHT
    );

    if(!isTie){

        winnerParticles.forEach(
            p=>{

                p.y += p.speed;

                if(
                    p.y > HEIGHT
                ){

                    p.y =
                        Math.random()*-20;

                    p.x =
                        Math.random()*WIDTH;
                }

                ctx.fillStyle =
                    p.color;

                ctx.beginPath();

                ctx.arc(
                    p.x,
                    p.y,
                    p.size,
                    0,
                    Math.PI*2
                );

                ctx.fill();
            }
        );
    }

    ctx.textAlign =
        "center";

    ctx.fillStyle =
        "#e6c8ff";

    ctx.font =
        "42px Chewy";

    let title =
        isTie
        ?
        "A Tie!"
        :
        `Player ${winnerIndex+1} has won the game!`;

    ctx.fillText(
        title,
        WIDTH/2,
        275
    );

    ctx.font =
        "bold 28px Arial";

    players.forEach(
        (player,i)=>{

            ctx.fillStyle =
                player.color;

            ctx.fillText(
                `${player.name} : ${winnerScores[i]}`,
                WIDTH/2,
                340 + (i*55)
            );
        }
    );

    ctx.fillStyle =
        "#bfebf4";

    ctx.font =
        "30px Chewy";

    ctx.fillText(
        "Press SPACE to Play Again",
        WIDTH/2,
        585
    );

    ctx.fillText(
        "Press ESC to Quit",
        WIDTH/2,
        155
    );
}

// =========================
// MAIN LOOP
// =========================

function animate(){

    requestAnimationFrame(
        animate
    );

    // INTRO SCREEN

    if(
        currentScreen ===
        "intro"
    ){

        ctx.drawImage(
            introVideo,
            0,
            0,
            WIDTH,
            HEIGHT
        );
    }

    // HOME SCREEN

    else if(
        currentScreen ===
        "home"
    ){

        ctx.drawImage(
            homeVideo,
            0,
            0,
            WIDTH,
            HEIGHT
        );

        // TIMER UNDERLINES

        ctx.strokeStyle = "black";
        ctx.lineWidth = 5;

        if(selectedTime === 15){

            ctx.beginPath();
            ctx.moveTo(125,230);
            ctx.lineTo(215,230);
            ctx.stroke();
        }

        else if(selectedTime === 30){

            ctx.beginPath();
            ctx.moveTo(350,230);
            ctx.lineTo(440,230);
            ctx.stroke();
        }

        else if(selectedTime === 45){

            ctx.beginPath();
            ctx.moveTo(560,235);
            ctx.lineTo(650,235);
            ctx.stroke();
        }

        else if(selectedTime === 60){

            ctx.beginPath();
            ctx.moveTo(770,235);
            ctx.lineTo(860,235);
            ctx.stroke();
        }

        // CONTROL UNDERLINES

        if(controlMode === "WASD"){

            ctx.beginPath();
            ctx.moveTo(180,505);
            ctx.lineTo(285,505);
            ctx.stroke();
        }

        else if(controlMode === "ARROWS"){

            ctx.beginPath();
            ctx.moveTo(690,505);
            ctx.lineTo(810,505);
            ctx.stroke();
        }

        // WARNING

        if(showWarning){

            ctx.fillStyle =
                "red";

            ctx.font =
                "14px Comic Sans MS";

            ctx.fillText(
                "pls chose the modes first",
                790,
                135
            );
        }
    }

    else if(
        currentScreen ===
        "game"
    ){

        drawGame();
    }

    else if(
        currentScreen ===
        "winner"
    ){

        drawWinnerScreen();
    }
}

animate();