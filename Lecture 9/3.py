import pygame, math
pygame.init()

# Создание игрового окна
screen = pygame.display.set_mode((800, 600))
base_layer = pygame.Surface((800, 600))
clock = pygame.time.Clock()
ColorLine = 'red'

# Переменные для работы с мышью
mouse_pos = pygame.mouse.get_pos()
prev_pos = mouse_pos
current_pos = mouse_pos
thickness = 5  # Начальная толщина линии

pencil = 0
line = 1
rectangle = 2
circle = 3
square = 4
right_3 = 5
equilateral = 6
rhombus = 7

current_mode = pencil
drawing = False
start_pos = (0, 0)

# Функция для рисования ромба
def draw_rhombus(surface, color, rect, width):  
    points = [
        (rect.centerx, rect.top),
        (rect.right, rect.centery),
        (rect.centerx, rect.bottom),
        (rect.left, rect.centery)
    ]
    pygame.draw.polygon(surface, color, points, width)

# Функция для рисования равностороннего треугольника
def draw_equilateral_triangle(surface, color, start, end, width):
    side_length = max(abs(end[0] - start[0]), abs(end[1] - start[1]))
    height = side_length * math.sqrt(3) / 2
    
    points = [
        (start[0], start[1] + height),  # Нижний левый
        (start[0] + side_length, start[1] + height),  # Нижний правый
        (start[0] + side_length/2, start[1])  # Верхний
    ]
    pygame.draw.polygon(surface, color, points, width)

# Функция для рисования прямоугольного треугольника
def draw_right_triangle(surface, color, start, end, width):
    points = [
        start,
        (start[0], end[1]),
        end
    ]
    pygame.draw.polygon(surface, color, points, width)

# Главный цикл программы
running = True
while running:
    current_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                start_pos = current_pos
                prev_pos = current_pos
                
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                # Рисуем в зависимости от выбранного режима
                if current_mode == line:
                    pygame.draw.line(base_layer, ColorLine, start_pos, current_pos, thickness)

                elif current_mode == rectangle:
                    rect = pygame.Rect(min(start_pos[0], current_pos[0]), min(start_pos[1], current_pos[1]), abs(current_pos[0] - start_pos[0]), abs(current_pos[1] - start_pos[1]))
                    pygame.draw.rect(base_layer, ColorLine, rect, thickness)

                elif current_mode == circle:
                    radius = int(math.hypot(current_pos[0] - start_pos[0], current_pos[1] - start_pos[1]))
                    pygame.draw.circle(base_layer, ColorLine, start_pos, radius, thickness)

                elif current_mode == square:
                    size = max(abs(current_pos[0] - start_pos[0]), abs(current_pos[1] - start_pos[1]))
                    rect = pygame.Rect(min(start_pos[0], current_pos[0]), min(start_pos[1], current_pos[1]), size, size)
                    pygame.draw.rect(base_layer, ColorLine, rect, thickness)
                
                elif current_mode == right_3:
                    draw_right_triangle(base_layer, ColorLine, start_pos, current_pos, thickness)
                
                elif current_mode == equilateral:
                    draw_equilateral_triangle(base_layer, ColorLine, start_pos, current_pos, thickness)
                
                elif current_mode == rhombus:
                    rect = pygame.Rect(min(start_pos[0], current_pos[0]), min(start_pos[1], current_pos[1]), abs(current_pos[0] - start_pos[0]), abs(current_pos[1] - start_pos[1]))
                    draw_rhombus(base_layer, ColorLine, rect, thickness)
                    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_mode = line
            elif event.key == pygame.K_2:
                current_mode = rectangle
            elif event.key == pygame.K_3:
                current_mode = circle
            elif event.key == pygame.K_4:
                current_mode = square
            elif event.key == pygame.K_5:
                current_mode = right_3
            elif event.key == pygame.K_6:
                current_mode = equilateral
            elif event.key == pygame.K_7:
                current_mode = rhombus
            elif event.key == pygame.K_0:
                current_mode = pencil
            
            # Изменение толщины линии
            if event.key == pygame.K_EQUALS:
                thickness += 1
            elif event.key == pygame.K_MINUS and thickness > 1:
                thickness -= 1
            elif event.key == pygame.K_g:
                ColorLine = 'green'
            elif event.key == pygame.K_b:
                ColorLine = 'blue'
            elif event.key == pygame.K_r:
                ColorLine = 'red'
            elif event.key == pygame.K_c:   # Очистка экрана
                base_layer.fill((0, 0, 0))

    screen.fill((0, 0, 0))
    screen.blit(base_layer, (0, 0))
    
    if drawing:
        if current_mode == pencil:
            pygame.draw.line(base_layer, ColorLine, prev_pos, current_pos, thickness)
            prev_pos = current_pos
        else:
            if current_mode == line:
                pygame.draw.line(screen, ColorLine, start_pos, current_pos, thickness)

            elif current_mode == rectangle:
                rect = pygame.Rect(min(start_pos[0], current_pos[0]), min(start_pos[1], current_pos[1]), abs(current_pos[0] - start_pos[0]), abs(current_pos[1] - start_pos[1]))
                pygame.draw.rect(screen, ColorLine, rect, thickness)

            elif current_mode == circle:
                radius = int(math.hypot(current_pos[0] - start_pos[0], current_pos[1] - start_pos[1]))
                pygame.draw.circle(screen, ColorLine, start_pos, radius, thickness)

            elif current_mode == square:
                size = max(abs(current_pos[0] - start_pos[0]), abs(current_pos[1] - start_pos[1]))
                rect = pygame.Rect(min(start_pos[0], current_pos[0]), min(start_pos[1], current_pos[1]), size, size)
                pygame.draw.rect(screen, ColorLine, rect, thickness)
                
            elif current_mode == right_3:
                draw_right_triangle(screen, ColorLine, start_pos, current_pos, thickness)
            
            elif current_mode == equilateral:
                draw_equilateral_triangle(screen, ColorLine, start_pos, current_pos, thickness)
            
            elif current_mode == rhombus:
                rect = pygame.Rect(min(start_pos[0], current_pos[0]), min(start_pos[1], current_pos[1]), abs(current_pos[0] - start_pos[0]), abs(current_pos[1] - start_pos[1]))
                draw_rhombus(screen, ColorLine, rect, thickness)
    
    # Отображаем текст
    font = pygame.font.SysFont(None, 24)
    mode_names = ["Pencil (0)", "Line (1)", "Rectangle (2)", "Circle (3)", "Square (4)", "Right triangle (5)", "Equilateral triangle (6)", "Rhombus (7)"]
    text_surface = font.render(f"Mode: {mode_names[current_mode]}", True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

    next_text = font.render(f"Color: {ColorLine}", True, "white")
    screen.blit(next_text, (10, 40))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()