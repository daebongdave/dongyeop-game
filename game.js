// game.js - Part 1

class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        
        // 캔버스 크기 설정
        this.canvas.width = 800;
        this.canvas.height = 600;
        
        // 게임 상태
        this.score = 0;
        this.lives = 3;
        this.gameOver = false;
        this.VICTORY_SCORE = 5;
        this.gameStartTime = Date.now();
        
        // 키 입력 상태
        this.keys = {
            ArrowLeft: false,
            ArrowRight: false,
            ArrowUp: false,
            ArrowDown: false
        };
        
        // 이벤트 리스너 설정
        this.setupEventListeners();
        
        // 게임 객체들
        this.head = new Head(this.canvas.width, this.canvas.height);
        this.minseok = new Minseok(this.canvas.width, this.canvas.height);
        this.oilDrops = [];
        this.jjaItems = [];
        
        // 이미지 로드
        this.loadImages();
    }

    loadImages() {
        this.images = {
            dongyeop: new Image(),
            minseok: new Image(),
            jjagaechi: new Image()
        };

        this.images.dongyeop.src = 'assets/KakaoTalk_Photo_2024-11-15-19-08-31.jpeg';
        this.images.minseok.src = 'assets/minseokface.png';
        this.images.jjagaechi.src = 'assets/jjagaechi.jpg';

        // 모든 이미지가 로드되면 게임 시작
        Promise.all(Object.values(this.images).map(img => {
            return new Promise(resolve => {
                img.onload = resolve;
            });
        })).then(() => this.startGame());
    }
// game.js - Part 2

setupEventListeners() {
    document.addEventListener('keydown', (e) => {
        if (this.keys.hasOwnProperty(e.code)) {
            this.keys[e.code] = true;
            e.preventDefault();
        }
    });

    document.addEventListener('keyup', (e) => {
        if (this.keys.hasOwnProperty(e.code)) {
            this.keys[e.code] = false;
            e.preventDefault();
        }
    });
}

startGame() {
    this.gameLoop();
}

gameLoop() {
    this.update();
    this.draw();
    if (!this.gameOver) {
        requestAnimationFrame(() => this.gameLoop());
    }
}

update() {
    // 머리 움직임
    this.head.move();

    // 민석이 움직임
    this.minseok.move(this.keys, this.head);

    // 기름방울 생성
    if (Math.random() < 0.059) {
        this.oilDrops.push(new OilDrop(this.head));
    }

    // 짜계치 생성
    if (Math.random() < 0.02) {
        this.jjaItems.push(new JjaItem(this.head));
    }

    // 기름방울 업데이트
    for (let i = this.oilDrops.length - 1; i >= 0; i--) {
        const drop = this.oilDrops[i];
        drop.move();
        
        if (drop.active && !this.minseok.invincible && 
            this.minseok.checkCollision(drop)) {
            this.lives--;
            drop.active = false;
            this.minseok.invincible = true;
            this.minseok.invincibleTimer = Date.now();
            if (this.lives <= 0) {
                this.gameOver = true;
            }
        }
        
        if (drop.y > this.canvas.height || !drop.active) {
            this.oilDrops.splice(i, 1);
        }
    }
// game.js - Part 3

        // 짜계치 업데이트
        for (let i = this.jjaItems.length - 1; i >= 0; i--) {
            const item = this.jjaItems[i];
            item.move();
            
            if (item.active && this.minseok.checkCollision(item)) {
                this.score++;
                item.active = false;
                if (this.score >= this.VICTORY_SCORE) {
                    this.gameOver = true;
                    this.victory = true;
                }
            }
            
            if (item.y > this.canvas.height || !item.active) {
                this.jjaItems.splice(i, 1);
            }
        }

        // 무적 상태 업데이트
        if (this.minseok.invincible && 
            Date.now() - this.minseok.invincibleTimer > 500) {
            this.minseok.invincible = false;
        }
    }

    draw() {
        // 화면 초기화
        this.ctx.fillStyle = 'white';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // 머리 그리기
        this.head.draw(this.ctx, this.images.dongyeop);

        // 민석이 그리기
        this.minseok.draw(this.ctx, this.images.minseok);

        // 기름방울 그리기
        this.oilDrops.forEach(drop => {
            if (drop.active) {
                this.ctx.fillStyle = 'yellow';
                this.ctx.beginPath();
                this.ctx.arc(drop.x, drop.y, drop.radius, 0, Math.PI * 2);
                this.ctx.fill();
            }
        });

        // 짜계치 그리기
        this.jjaItems.forEach(item => {
            if (item.active) {
                this.ctx.drawImage(this.images.jjagaechi, 
                    item.x, item.y, item.width, item.height);
            }
        });

        // UI 그리기
        this.drawUI();

        // 게임오버 화면
        if (this.gameOver) {
            this.drawGameOver();
        }
    }
// game.js - Part 4

drawUI() {
    this.ctx.font = '24px Arial';
    this.ctx.fillStyle = 'black';
    
    // 점수
    this.ctx.fillText(`짜계치: ${this.score}/${this.VICTORY_SCORE}`, 10, 30);
    
    // 시간
    const elapsedTime = Math.floor((Date.now() - this.gameStartTime) / 1000);
    this.ctx.fillText(`시간: ${elapsedTime}초`, 
        this.canvas.width/2 - 50, 30);
    
    // 목숨
    for (let i = 0; i < this.lives; i++) {
        this.drawHeart(this.canvas.width - 40 * (i + 1), 10);
    }
}

drawHeart(x, y) {
    this.ctx.fillStyle = 'red';
    this.ctx.beginPath();
    this.ctx.moveTo(x + 15, y + 5);
    this.ctx.bezierCurveTo(x + 15, y + 5, x + 10, y, x, y + 5);
    this.ctx.bezierCurveTo(x - 10, y + 15, x + 15, y + 25, x + 15, y + 25);
    this.ctx.bezierCurveTo(x + 15, y + 25, x + 40, y + 15, x + 30, y + 5);
    this.ctx.bezierCurveTo(x + 30, y, x + 15, y, x + 15, y + 5);
    this.ctx.fill();
}

drawGameOver() {
    this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    
    this.ctx.font = '48px Arial';
    this.ctx.fillStyle = 'white';
    if (this.victory) {
        this.ctx.fillText('승리!', 
            this.canvas.width/2 - 50, this.canvas.height/2 - 50);
        this.ctx.font = '24px Arial';
        this.ctx.fillText('한동엽을 물리쳤습니다!', 
            this.canvas.width/2 - 100, this.canvas.height/2);
    } else {
        this.ctx.fillText('게임 오버', 
            this.canvas.width/2 - 100, this.canvas.height/2 - 50);
        this.ctx.font = '24px Arial';
        this.ctx.fillText('한동엽의 기름에 당했습니다...', 
            this.canvas.width/2 - 120, this.canvas.height/2);
    }
}
}
// game.js - Part 5

class Head {
    constructor(canvasWidth, canvasHeight) {
        this.width = 200;
        this.height = 200;
        this.x = (canvasWidth / 2) - (this.width / 2);
        this.y = 20;
        this.direction = 1;  // 1: 아래로, -1: 위로
        this.speed = 2;
        this.minY = 20;
        this.maxY = 100;
    }

    move() {
        this.y += this.speed * this.direction;
        if (this.y >= this.maxY) {
            this.direction = -1;
        } else if (this.y <= this.minY) {
            this.direction = 1;
        }
    }

    draw(ctx, image) {
        ctx.drawImage(image, this.x, this.y, this.width, this.height);
    }
}

class Minseok {
    constructor(canvasWidth, canvasHeight) {
        this.width = 40;
        this.height = 40;
        this.x = canvasWidth / 2;
        this.y = canvasHeight - 100;
        this.speed = 5.6;
        this.invincible = false;
        this.invincibleTimer = 0;
    }

    move(keys, head) {
        if (keys.ArrowLeft) this.x -= this.speed;
        if (keys.ArrowRight) this.x += this.speed;
        if (keys.ArrowUp) this.y -= this.speed;
        if (keys.ArrowDown) this.y += this.speed;

        // 이동 범위 제한
        const margin = 5;
        this.x = Math.max(head.x + margin, 
                Math.min(this.x, head.x + head.width - this.width - margin));
        this.y = Math.max(head.y + head.height, 
                Math.min(this.y, head.y + head.height + 250));
    }

    draw(ctx, image) {
        if (!this.invincible || (this.invincible && Date.now() % 200 < 100)) {
            ctx.drawImage(image, this.x, this.y, this.width, this.height);
        }
    }

    checkCollision(object) {
        return (object.x > this.x && 
                object.x < this.x + this.width && 
                object.y > this.y && 
                object.y < this.y + this.height);
    }
}
// game.js - Part 6

class OilDrop {
    constructor(head) {
        this.radius = 8.5;
        this.x = head.x + Math.random() * head.width;
        this.y = head.y + (head.height / 2);
        this.speed = 6 + Math.random() * 7; // 6~13 사이의 속도
        this.active = true;
    }

    move() {
        this.y += this.speed;
    }
}

class JjaItem {
    constructor(head) {
        this.width = 25;
        this.height = 25;
        this.x = head.x + Math.random() * (head.width - this.width);
        this.y = head.y + (head.height / 2);
        this.speed = 3 + Math.random() * 2; // 3~5 사이의 속도
        this.active = true;
    }

    move() {
        this.y += this.speed;
    }
}

// 게임 시작
window.onload = () => {
    new Game();
};