import pygame
import random
import os

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("한동엽 기름 피하기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
OIL_COLOR = (100, 70, 40)  # 기름색

# 게임 변수
score = 0  # 이제는 짜계치 점수
game_start_time = 0  # 게임 시작 시간
elapsed_time = 0  # 경과 시간
VICTORY_SCORE = 5  # 승리에 필요한 짜계치 수

# 게임 변수 추가
lives = 3  # 목숨 3개
game_over = False
difficulty_timer = 0
difficulty_increase = 1000  # 1000틱마다 난이도 증가

# 현재 파일의 디렉토리 경로를 가져옴
current_dir = os.path.dirname(os.path.abspath(__file__))

# 이미지 로드
dongyeop_image = pygame.image.load(os.path.join(current_dir, 'assets', 'KakaoTalk_Photo_2024-11-15-19-08-31.jpeg'))
dongyeop_image = pygame.transform.scale(dongyeop_image, (200, 200))
minseok_image = pygame.image.load(os.path.join(current_dir, 'assets', 'minseokface.png'))
minseok_image = pygame.transform.scale(minseok_image, (40, 40))
jjagaechi_image = pygame.image.load(os.path.join(current_dir, 'assets', 'jjagaechi.jpg'))
jjagaechi_image = pygame.transform.scale(jjagaechi_image, (25, 25))

# 게임 상태 변수 추가
ONBOARDING = 0
ZOOM_ANIMATION = 1
PLAYING = 2
VICTORY_ANIMATION = 3
GAME_OVER = 4

# 게임 초기 상태 설정
game_state = ONBOARDING
zoom_scale = 1.0
zoom_speed = 0.02

# 온보딩 화면용 이미지 준비
full_dongyeop = pygame.transform.scale(dongyeop_image, (WIDTH, HEIGHT))

# 김민석 클래스
class Minseok:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.speed = 5.6
        self.direction = 1  # 1: 아래로, -1: 위로
        self.min_y = HEIGHT - 150  # 최소 y 위치
        self.max_y = HEIGHT - 50   # 최대 y 위치
        self.invincible = False
        self.invincible_timer = 0
        self.show_speech = False
        self.speech_timer = 0
        self.hit_count = 0
        self.speeches = [
            "아 시발 더러워",
            "맞짱깔래",
            "난 실패작이야..."
        ]
        self.jja_speeches = [
            "개이득",
            "지리노",
            "맛있노",
            "배부르노"
        ]
        self.show_jja_speech = False
        self.jja_speech_timer = 0
        self.jja_speech_index = 0
        
    def move(self):
        keys = pygame.key.get_pressed()
        new_x = self.x
        new_y = self.y
        
        # 좌우 이동
        if keys[pygame.K_LEFT]:
            new_x = self.x - self.speed
        if keys[pygame.K_RIGHT]:
            new_x = self.x + self.speed
            
        # 상하 이동
        if keys[pygame.K_UP]:
            new_y = self.y - self.speed
        if keys[pygame.K_DOWN]:
            new_y = self.y + self.speed
            
        # 이동 범위 제한 (마진 줄임)
        movement_margin = 5  # 45에서 20으로 줄임
        if (new_x >= head.x + movement_margin and 
            new_x <= head.x + head.width - self.width - movement_margin):
            self.x = new_x
            
        # y축 이동 범위 확장
        if (new_y >= HEIGHT - 300 and new_y <= HEIGHT - 50):  # 위쪽 범위 확장
            self.y = new_y
            
    def draw(self):
        if not self.invincible or (self.invincible and pygame.time.get_ticks() % 200 < 100):
            screen.blit(minseok_image, (self.x, self.y))
            
        # 말풍선 표시 (크기 30% 축소)
        if self.show_speech:
            speech_text = self.speeches[self.hit_count - 1]
            text_surface = game_font.render(speech_text, True, BLACK)
            text_width = int(text_surface.get_width() * 0.7)  # 30% 축소
            text_height = int(text_surface.get_height() * 0.7)  # 30% 축소
            
            # 말풍선 위치
            bubble_x = self.x - (text_width//2 - self.width//2)
            bubble_y = self.y - 45  # 위치도 약간 조정
            
            # 말풍선 그리기
            padding = 7  # 패딩도 축소
            bubble_rect = pygame.Rect(
                bubble_x - padding,
                bubble_y - padding,
                text_width + padding*2,
                text_height + padding*2
            )
            
            # 말풍선 배경
            pygame.draw.rect(screen, WHITE, bubble_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, bubble_rect, 2, border_radius=10)
            
            # 말풍선 꼬리
            tail_points = [
                (self.x + self.width//2, self.y),
                (self.x + self.width//2 - 10, bubble_y + text_height + padding - 5),
                (self.x + self.width//2 + 10, bubble_y + text_height + padding - 5)
            ]
            pygame.draw.polygon(screen, WHITE, tail_points)
            pygame.draw.polygon(screen, BLACK, tail_points, 2)
            
            # 축소된 텍스트 그리기
            scaled_surface = pygame.transform.scale(text_surface, (text_width, text_height))
            screen.blit(scaled_surface, (bubble_x, bubble_y))
            
            # 1.5초 후 말풍선 숨기기
            if pygame.time.get_ticks() - self.speech_timer > 1500:
                self.show_speech = False
        
        # 짜계치 획득 말풍선
        if self.show_jja_speech:
            speech_text = self.jja_speeches[self.jja_speech_index]
            text_surface = game_font.render(speech_text, True, BLACK)
            text_width = int(text_surface.get_width() * 0.7)
            text_height = int(text_surface.get_height() * 0.7)
            
            bubble_x = self.x - (text_width//2 - self.width//2)
            bubble_y = self.y - 45
            
            padding = 7
            bubble_rect = pygame.Rect(
                bubble_x - padding,
                bubble_y - padding,
                text_width + padding*2,
                text_height + padding*2
            )
            
            pygame.draw.rect(screen, WHITE, bubble_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, bubble_rect, 2, border_radius=10)
            
            tail_points = [
                (self.x + self.width//2, self.y),
                (self.x + self.width//2 - 10, bubble_y + text_height + padding - 5),
                (self.x + self.width//2 + 10, bubble_y + text_height + padding - 5)
            ]
            pygame.draw.polygon(screen, WHITE, tail_points)
            pygame.draw.polygon(screen, BLACK, tail_points, 2)
            
            scaled_surface = pygame.transform.scale(text_surface, (text_width, text_height))
            screen.blit(scaled_surface, (bubble_x, bubble_y))
            
            if pygame.time.get_ticks() - self.jja_speech_timer > 1000:
                self.show_jja_speech = False

    def check_collision(self, oil_drop):
        if (oil_drop.x > self.x and oil_drop.x < self.x + self.width and 
            oil_drop.y > self.y and oil_drop.y < self.y + self.height):
            return True
        return False

    def update_invincible(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_timer > 500:  # 0.5초로 변경
                self.invincible = False

# 머 클래스
class Head:
    def __init__(self):
        self.width = 200
        self.height = 200
        self.x = WIDTH // 2 - self.width // 2
        self.y = 20
        self.direction = 1  # 1: 아래로, -1: 위로
        self.speed = 2
        self.min_y = 20  # 최소 y 위치
        self.max_y = 100  # 최대 y 위치
        
    def move(self):
        self.y += self.speed * self.direction
        if self.y >= self.max_y:
            self.direction = -1
        elif self.y <= self.min_y:
            self.direction = 1
            
    def draw(self):
        screen.blit(dongyeop_image, (self.x, self.y))

# 기름방울 클래스
class OilDrop:
    def __init__(self):
        self.radius = 8.5
        self.x = random.randint(head.x, head.x + head.width)
        self.y = head.y + (head.height // 2)
        self.speed = random.randint(6, 13)
        self.active = True
        
    def move(self):
        if self.active:
            self.y += self.speed
            
    def draw(self):
        if self.active:
            pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius)

# 짜계치 클래스 추가
class JjaItem:
    def __init__(self):
        self.width = 25
        self.height = 25
        movement_margin = 20  # 45에서 20으로 줄임
        self.x = random.randint(head.x + movement_margin, 
                              head.x + head.width - self.width - movement_margin)
        self.y = head.y + (head.height // 2)
        self.speed = 5  # 속도 조정
        self.active = True
        
    def move(self):
        if self.active:
            self.y += self.speed
            
    def draw(self):
        if self.active:
            screen.blit(jjagaechi_image, (self.x, self.y))

# 게임 객체 생성
head = Head()
minseok = Minseok()
oil_drops = []
clock = pygame.time.Clock()

# 다른 맥OS 한글 폰트들
fonts = [
    '/System/Library/Fonts/AppleSDGothicNeo.ttc',
    '/Library/Fonts/AppleGothic.ttf',
    '/System/Library/Fonts/Supplemental/AppleGothic.ttf'
]

# 사용 가능한 폰트 찾기
for font_path in fonts:
    try:
        game_font = pygame.font.Font(font_path, 36)
        title_font = pygame.font.Font(font_path, 74)
        break
    except:
        continue

# 시작 버튼 클래스
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (50, 50, 50)
        self.hover_color = (100, 100, 100)
        self.text_color = WHITE
        self.font = pygame.font.Font('/System/Library/Fonts/AppleSDGothicNeo.ttc', 36)
        
    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# 시작 버튼 생성
start_button = Button(WIDTH//2 - 100, HEIGHT - 150, 200, 60, "시작하기")

# 게임 시작 시 변수 초기화
jja_items = []
game_start_time = pygame.time.get_ticks()

# reset_game 함수 정의 (게임 변수 설정 다음에 추가)
def reset_game():
    global score, lives, game_over, game_state, game_start_time, oil_drops, jja_items, minseok, zoom_scale, game_timer
    score = 0
    lives = 3
    game_over = False
    game_state = PLAYING
    game_start_time = pygame.time.get_ticks()
    oil_drops = []
    jja_items = []
    zoom_scale = 1.0
    minseok = Minseok()  # 김민석 객체 새로 생성
    game_timer = GameTimer()

# 승리 애니메이션 관련 변수 추가
class VictoryAnimation:
    def __init__(self):
        self.minseok_x = -100  # 화면 왼쪽 밖에서 시작
        self.minseok_y = HEIGHT // 2
        self.dongyeop_x = WIDTH // 2
        self.dongyeop_y = HEIGHT // 2
        self.dongyeop_rotation = 0
        self.dongyeop_fall_speed = 0
        self.stage = 0  # 애니메이션 단계
        self.timer = 0
        
    def update(self):
        if self.stage == 0:  # 김민석이 날아오는 단계
            self.minseok_x += 15
            if self.minseok_x >= WIDTH // 2 - 100:
                self.stage = 1
                self.timer = pygame.time.get_ticks()
        
        elif self.stage == 1:  # 충돌 효과
            if pygame.time.get_ticks() - self.timer > 500:
                self.stage = 2
        
        elif self.stage == 2:  # 한동엽이 떨어지는 단계
            self.dongyeop_y += self.dongyeop_fall_speed
            self.dongyeop_fall_speed += 0.5
            self.dongyeop_rotation += 5
            if self.dongyeop_y > HEIGHT + 200:  # 화면 밖으로 완전히 떨어짐
                self.stage = 3
                self.timer = pygame.time.get_ticks()
        
        elif self.stage == 3:  # 대기 후 게임 오버 화면으로
            if pygame.time.get_ticks() - self.timer > 1000:
                return True
        return False
    
    def draw(self):
        if self.stage < 3:
            # 불구덩이 그리기
            pygame.draw.rect(screen, (255, 69, 0), (0, HEIGHT - 50, WIDTH, 50))
            
            # 한동엽 그리기 (회전)
            if self.stage >= 1:
                rotated_dongyeop = pygame.transform.rotate(dongyeop_image, self.dongyeop_rotation)
                screen.blit(rotated_dongyeop, (self.dongyeop_x - rotated_dongyeop.get_width()//2, 
                                             self.dongyeop_y - rotated_dongyeop.get_height()//2))
            
            # 김민석 그리기
            scaled_minseok = pygame.transform.scale(minseok_image, (100, 100))
            screen.blit(scaled_minseok, (self.minseok_x, self.minseok_y))

# 게임 시작 시간 관련 변수 추가
class GameTimer:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()
        self.oil_delay = 1500  # 1.5초
        self.jja_delay = 2000  # 2초
        
    def can_spawn_oil(self):
        return pygame.time.get_ticks() - self.start_time > self.oil_delay
        
    def can_spawn_jja(self):
        return pygame.time.get_ticks() - self.start_time > self.jja_delay

# 게임 시작 시 타이머 초기화 (파일 상단에 추가)
game_timer = GameTimer()

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == ONBOARDING:
                if start_button.is_clicked(event.pos):
                    game_state = ZOOM_ANIMATION
            elif game_state == GAME_OVER:
                if restart_button.is_clicked(event.pos):
                    reset_game()
        
    screen.fill(WHITE)
    
    if game_state == ONBOARDING:
        # 온보딩 화면
        screen.fill(BLACK)
        screen.blit(full_dongyeop, (0, 0))
        
        # 반투명 검정 오버레이
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        # 설명 텍스트
        font = pygame.font.Font('/System/Library/Fonts/AppleSDGothicNeo.ttc', 32)
        texts = [
            "1. 당신은 더러운 한동엽 대가리 기름 덩어리를 피해야합니다.",
            "2. 짜계치 5개를 획득하면 승리",
            "3. 방향키로 움직이세요"
        ]
        
        for i, text in enumerate(texts):
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, (50, 200 + i * 50))
        
        start_button.draw()
        
    elif game_state == ZOOM_ANIMATION:
        # 줌아웃 애니메이션
        zoom_scale -= zoom_speed
        if zoom_scale <= 0.3:  # 최종 크기에 도달하면
            game_state = PLAYING
            
        current_size = (int(WIDTH * zoom_scale), int(HEIGHT * zoom_scale))
        zoomed_image = pygame.transform.scale(full_dongyeop, current_size)
        
        # 이미지를 화면 중앙에 배치
        x = (WIDTH - current_size[0]) // 2
        y = (HEIGHT - current_size[1]) // 2
        screen.blit(zoomed_image, (x, y))
        
    elif game_state == PLAYING:
        if not game_over:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - game_start_time) // 1000

            # 화면 초기화
            screen.fill(WHITE)
            
            # 머리 움직임 및 그리기
            head.move()
            head.draw()
            
            # 김민 이동 및 그리기
            minseok.move()
            minseok.draw()
            
            # 딜레이 후 기름방울 생성
            if game_timer.can_spawn_oil():
                if random.random() < 0.059:
                    oil_drops.append(OilDrop())
                
            # 딜레이 후 짜계치 아이템 생성
            if game_timer.can_spawn_jja():
                if random.random() < 0.02:  # 0.00368에서 0.02로 크게 증가
                    jja_items.append(JjaItem())

            # 기름방울 업데이트 및 그리기
            for drop in oil_drops[:]:
                drop.move()
                drop.draw()
                
                if drop.active and not minseok.invincible and minseok.check_collision(drop):
                    lives -= 1
                    drop.active = False
                    minseok.invincible = True
                    minseok.invincible_timer = pygame.time.get_ticks()
                    minseok.hit_count += 1
                    minseok.show_speech = True
                    minseok.speech_timer = pygame.time.get_ticks()
                    if lives <= 0:
                        game_over = True
                        break
                
                if drop.y > HEIGHT:
                    oil_drops.remove(drop)
            
            # 짜계치 아이템 업데이트 및 그리기
            for item in jja_items[:]:
                item.move()
                item.draw()
                
                # 짜계치 획득 체크
                if item.active and not minseok.invincible and minseok.check_collision(item):
                    score += 1
                    item.active = False
                    jja_items.remove(item)
                    # 짜계치 획득 대사 표시
                    minseok.show_jja_speech = True
                    minseok.jja_speech_timer = pygame.time.get_ticks()
                    minseok.jja_speech_index = score - 1  # 0부터 시작하는 인덱스
                    if score >= VICTORY_SCORE:
                        game_state = VICTORY_ANIMATION
                        victory_animation = VictoryAnimation()
                        break
                        
                if item.y > HEIGHT:
                    jja_items.remove(item)
            
            # 점수와 목숨 표시 (위치 조정)
            font = pygame.font.Font('/System/Library/Fonts/AppleSDGothicNeo.ttc', 36)
            
            # 짜계치 점수 표시 (왼쪽 상단)
            score_text = font.render(f"짜계치: {score}/{VICTORY_SCORE}", True, BLACK)
            screen.blit(score_text, (10, 10))
            
            # 시간 표시 (중앙 상단)
            time_text = font.render(f"시간: {elapsed_time}초", True, BLACK)
            time_rect = time_text.get_rect(midtop=(WIDTH//2, 10))
            screen.blit(time_text, time_rect)
            
            # 하트(목숨) 표시 (오쪽 상단)
            heart_size = 30
            heart_spacing = 40
            for i in range(lives):
                heart_x = WIDTH - (heart_spacing * (lives - i))
                heart_y = 10
                pygame.draw.polygon(screen, RED, [
                    (heart_x + heart_size//2, heart_y + heart_size//4),
                    (heart_x + heart_size//4, heart_y),
                    (heart_x, heart_y + heart_size//4),
                    (heart_x + heart_size//2, heart_y + heart_size),
                    (heart_x + heart_size, heart_y + heart_size//4),
                    (heart_x + heart_size*3//4, heart_y),
                ])
            
            # 난이도 증가
            difficulty_timer += 1
            if difficulty_timer > difficulty_increase:
                for drop in oil_drops:
                    drop.speed += 1
                difficulty_timer = 0
            
            # 무적 상태 업데이트
            minseok.update_invincible()
            
        else:
            game_state = GAME_OVER
            
    elif game_state == VICTORY_ANIMATION:
        screen.fill(WHITE)
        victory_animation.draw()
        if victory_animation.update():
            game_state = GAME_OVER
    
    elif game_state == GAME_OVER:
        try:
            game_over_font = pygame.font.Font('/System/Library/Fonts/AppleSDGothicNeo.ttc', 17)
        except:
            game_over_font = pygame.font.Font(None, 17)
            
        if score >= VICTORY_SCORE:
            # 승리 화면 (여러 줄의 텍스트)
            victory_messages = [
                "승리! 당신은 개 좆같이 드러워서 소름이 돋는 한동엽 대가리 기름 덩어리를 피하고",
                "짜계치를 모두 획득하여 한동엽을 처참하게 불구덩이로 떨어뜨렸습니다.",
                "이제 한동엽은 영원히 지옥에서 븅신같이 족발이나 쳐먹으며 살아가겠죠.",
                f"한동엽을 물리치는데 걸린 시간: {elapsed_time}초"
            ]
            
            # 여러 줄의 텍스트 렌더링
            text_surfaces = []
            for msg in victory_messages:
                text_surfaces.append(game_over_font.render(msg, True, BLACK))
            
            # 텍스트 위치 계산 및 그리기
            start_y = HEIGHT//2 - (len(victory_messages) * 20)  # 텍스트 시작 y좌표
            for i, surface in enumerate(text_surfaces):
                text_rect = surface.get_rect(center=(WIDTH//2, start_y + i * 25))
                screen.blit(surface, text_rect)
        else:
            # 패배 화면 (기존과 동일)
            text = game_over_font.render("게임 오버!", True, BLACK)
            score_text = game_over_font.render(f"당신은 한동엽 대가리 기름 지옥에 갇혔습니다. 좆된거죠 뭐", True, BLACK)
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 15))
            score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 15))
            screen.blit(text, text_rect)
            screen.blit(score_text, score_rect)

        # 다시하기 버튼 위치도 약간 아래로 조정
        restart_button = Button(WIDTH//2 - 100, HEIGHT//2 + 120, 200, 60, "다시하기")
        restart_button.draw()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()