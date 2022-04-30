import functools, operator
from textwrap import indent
import pygame
import pygame.locals as lcs
import pygame.time, json

import events

from tools import *
from gui_edit import *
from gui_msg import *
from gui_save import *
from gui_load import *

import kenken_logic

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20)

operations = ['+', '-', 'x', '/', '.']
ADD, DIF, MUL, DIV, SET = range(5)

mainfname = None

win = pygame.display.set_mode((900, 600))
back = win.copy()
event_ctrl = events.EventCtrl()

c_white = pygame.Color(255, 255, 255)
c_gray = pygame.Color(100, 100, 100)
c_gray_w = pygame.Color(140, 140, 140)
c_green = pygame.Color(0, 255, 0)
c_green_g = pygame.Color(100, 200, 100)
c_black = pygame.Color(0, 0, 0)
c_red_l =pygame.Color(255, 190, 190)
c_red_g =pygame.Color(190, 150, 150)
c_blue_g = pygame.Color(80, 90, 110)

c_yellow = pygame.Color(255, 255, 0)
c_yellow_d = pygame.Color(150, 150, 0)

r_add = pygame.rect.Rect(600, 0, 75, 60)
r_sav = pygame.rect.Rect(675, 0, 75, 60)
r_loa = pygame.rect.Rect(750, 0, 75, 60)
r_sol = pygame.rect.Rect(825, 0, 75, 60)
r_box = pygame.rect.Rect(600, 0, 300, 60)

scroll = 0
grupos = [
    {
        'op': ADD,
        'r': 4,
        'coords': [(0, 0), (1, 0), (1, 1)]
    }
]
grupo_seleccionado = -1
result = None

hold_click = False

while True:
    win.fill((0, 0, 0))

    mouse = pygame.mouse.get_pos()
    event_ctrl.update(pygame.event.get())

    if event_ctrl.mouse_down(1):
        hold_click = True
    if event_ctrl.mouse_up(1):
        hold_click = False

    if event_ctrl.key_down(lcs.K_x):
        if message_box_bool(win, event_ctrl, back, "¿Quiere salir?"):
            break

    for i in range(10):
        for j in range(10):
            r = pygame.rect.Rect(i*60, j*60, 60, 60)
            if r.collidepoint(mouse) and event_ctrl.mouse_down(1):
                if (i, j) in all_taken(grupos):
                    ind = get_grupo(grupos, (i, j))
                    if ind != -1:
                        grupo_seleccionado = ind

    for i in range(10):
        for j in range(10):
            r = pygame.rect.Rect(i*60, j*60, 60, 60)
            if r.collidepoint(mouse):
                if grupo_seleccionado != -1:
                    g = grupos[grupo_seleccionado]
                    if hold_click:
                        if not (i, j) in all_taken(grupos):
                            if result != None and message_box_bool(win, event_ctrl, back, "Se perderá el cálculo"):
                                result = None
                            if result == None:
                                if (g['op'] == DIF or g['op'] == DIV):
                                    if len(g['coords']) < 2:
                                        g['coords'].append((i, j))
                                    else:
                                        message_box_warning(win, event_ctrl, back, "Solo se permiten 2 bloques")
                                        hold_click = False
                                else: 
                                    g['coords'].append((i, j))
                    elif event_ctrl.mouse_press(3):
                        if (i, j) in g['coords']:
                            if result != None and message_box_bool(win, event_ctrl, back, "Se perderá el cálculo"):
                                result = None
                            if result == None:
                                g['coords'].remove((i, j))
                pygame.draw.rect(win, c_white, r)
            else:
                pygame.draw.rect(win, c_gray, r)
    
    for k, g in enumerate(grupos):
        r = pygame.rect.Rect(r_box)
        r.y += 60 + 60*k + scroll

        r1 = pygame.Rect(r)
        r1.w = r1.w // 2
        r2 = pygame.Rect(r)
        r2.w = r2.w // 2
        r2.x += r1.w

        # Dibuajar Selectores
        cc = (150, 0, 0) if len(g['coords'])==0 else (c_green_g if grupo_seleccionado == k else c_gray)
        pygame.draw.rect(win, cc, r)
        
        draw_text(win, r1.center, font, str(g['r']), False)
        draw_text(win, r2.center, font, operations[g['op']], False)

        if r.collidepoint(mouse):
            if event_ctrl.mouse_down(1):
                grupo_seleccionado = k
            if event_ctrl.mouse_down(3):
                mode, op, number = ChangeData(win, event_ctrl, back, g, r)
                if mode:
                    g['op'] = op
                    g['r'] = int(number)
        
        pygame.draw.rect(win, c_green if grupo_seleccionado == k else c_black, r, 3)


        # Dibujar Fondos de grupos
        for i, j in g['coords']:
            r = pygame.rect.Rect(i*60, j*60, 60, 60)
            if grupo_seleccionado == k:
                pygame.draw.rect(win, (100, 200, 50), r)
            else:
                pygame.draw.rect(win, c_gray_w, r)
    
    if result != None:
        for i in range(10):
            for j in range(10):
                r = pygame.rect.Rect(i*60, j*60, 60, 60)
                draw_text_ext(win, r.center, font, str(result[j][i]), (0, 0, 100), False)

    # Dibujar Bordes y textos
    for k, g in enumerate(grupos):
        draw_borders(win, g['coords'])
        if len(g['coords']) > 0:
            i, j = get_top(g['coords'])
            draw_text(win, (i*60 + 3, j*60 +3), font, f"{g['r']}{operations[g['op']]}")

    # Boton de agregar
    if draw_boton_if(win, event_ctrl, r_add, mouse, font, "Agregar", c_red_l, c_red_g):
        grupos.append({'op':0, 'r':1, 'coords':[]})
        grupo_seleccionado = len(grupos)-1

    if draw_boton_if(win, event_ctrl, r_sav, mouse, font, "Guardar", c_yellow, c_yellow_d):
        name = GuiSave(win, event_ctrl, back, grupos, mainfname)
        if name != None:
            with open("save/"+name, "w") as f:
                f.write(json.dumps(grupos, indent=4))
    
    if draw_boton_if(win, event_ctrl, r_loa, mouse, font, "Cargar", c_white, c_gray):
        name = GuiLoad(win, event_ctrl, back, grupos)
        if name != None:
            with open("save/"+name, "r") as f:
                text = functools.reduce(operator.add, f.readlines())
                jsn = json.loads(text)
                for block in jsn:
                    block['coords'] = list(map(tuple, block['coords']))
                grupos = jsn
                mainfname = name
    
    if draw_boton_if(win, event_ctrl, r_sol, mouse, font, "Solve", (0, 255, 0), (0, 100, 0)):
        result = kenken_logic.solve(grupos, 10)



    if event_ctrl.mouse_up(4):
        scroll += 30
    if event_ctrl.mouse_up(5) and scroll + len(grupos)*60 > 60:
        scroll -= 30
    scroll = min(scroll, 0)

    back = win.copy()
    clock.tick(60)
    pygame.display.update()