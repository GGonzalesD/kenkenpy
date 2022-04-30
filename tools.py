import pygame

def draw_borders(surface:pygame.Surface, coords:list):
    for i, j in coords:
        if not (i+1, j) in coords:
            pygame.draw.line(surface, (0, 0, 0), ((i+1)*60, j*60), ((i+1)*60, (j+1)*60), 4)
        if not (i-1, j) in coords:
            pygame.draw.line(surface, (0, 0, 0), ((i)*60, j*60), ((i)*60, (j+1)*60), 4)
        if not (i, j+1) in coords:
            pygame.draw.line(surface, (0, 0, 0), ((i)*60, (j+1)*60), ((i+1)*60, (j+1)*60), 4)
        if not (i, j-1) in coords:
            pygame.draw.line(surface, (0, 0, 0), ((i)*60, (j)*60), ((i+1)*60, (j)*60), 4)

def all_taken(grupos:list):
    for g in grupos:
        for i, j in g['coords']:
            yield (i, j)

def get_grupo(grupos:list, index):
    for x, g in enumerate(grupos):
        for i, j in g['coords']:
            if (i, j) == index:
                return x
    return -1

def get_top(coords):
    g = [9999, None]
    for i, j in coords:
        c = j*10 + i
        if c < g[0]:
            g = [c, (i, j)]
    return g[1]


def draw_text_ext(surface:pygame.Surface, poss, font:pygame.font.Font, text, color, mode=True):
    img = font.render(text, True, color)
    r = img.get_rect()
    if mode:
        r.topleft = poss
    else:
        r.center = poss
    surface.blit(img, r)

def draw_text(surface:pygame.Surface, poss, font:pygame.font.Font, text, mode=True):
    draw_text_ext(surface, poss, font, text, (0, 0, 0), mode)




def draw_boton_if(surface, event, rect, mouse, font, text, bg1, bg2):
    c = bg1 if rect.collidepoint(mouse) else bg2
    pygame.draw.rect(surface, c, rect)
    draw_text(surface, rect.center, font, text, False)
    return rect.collidepoint(mouse) and event.mouse_down(1)

def draw_label(surface, rect, font, text, bg):
    pygame.draw.rect(surface, bg, rect)
    draw_text(surface, rect.center, font, text, False)