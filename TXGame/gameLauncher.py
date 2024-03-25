import sys
import pygame

def scale_image(img, max_width, max_height):
    """
    等比例缩放图片，使图片能够在设定的最大宽度和高度内显示。
    """
    width, height = img.get_size()
    aspect_ratio = width / height
    new_width = min(max_width, width)
    new_height = int(new_width / aspect_ratio)

    # 如果高度超过最大高度，则按照高度进行缩放
    if new_height > max_height:
        new_height = min(max_height, height)
        new_width = int(new_height * aspect_ratio)

    return pygame.transform.scale(img, (new_width, new_height))

# 初始化Pygame
pygame.init()

# 设置窗口大小
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置标题
pygame.display.set_caption('GameExample')

# 加载图片
character_image = pygame.image.load('GameAssets/character.png')

# 设置最大宽度和高度
max_width = 100
max_height = 100

# 调用函数进行等比例缩放
character_image = scale_image(character_image, max_width, max_height)

# 获取缩放后的图片rect
character_rect = character_image.get_rect()

# 角色移动速度
character_speed = 5

# 加载图片
background_image = pygame.image.load('GameAssets/background.png')

# 将图片缩放到与屏幕尺寸相同
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# 游戏主循环
running = True
while running:
    # 事件监听
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 按键检测以移动角色
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        character_rect.y -= character_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        character_rect.y += character_speed
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        character_rect.x -= character_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        character_rect.x += character_speed

    # 防止角色移出窗口
    if character_rect.left < 0:
        character_rect.left = 0
    if character_rect.right > screen_width:
        character_rect.right = screen_width
    if character_rect.top < 0:
        character_rect.top = 0
    if character_rect.bottom > screen_height:
        character_rect.bottom = screen_height

    # 使用背景图片填充屏幕
    screen.blit(background_image, (0, 0))
    # 绘制角色图像
    screen.blit(character_image, character_rect)
    # 更新屏幕显示
    pygame.display.update()

    # 控制游戏帧率
    pygame.time.Clock().tick(60)

# 退出游戏
pygame.quit()
sys.exit()