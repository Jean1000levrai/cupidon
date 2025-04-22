import tkinter as tk
from PIL import Image, ImageTk
import math
import multiprocessing
import random
import time

# -------------------------------fonctions----------------------------------------

def charger_image(chemin, nb_image = 1, taille=None ,index_debut = 1, miroir=False):
    '''fonction qui sert sert à charger les images. Elle prend en parametre : le chemin d'acces(chemin),
    indice du debut(index_debut) et fin/le nombre d'image(nb_image), un tuple pour la taille de l'image 
    et booléen pour savoir si l'image doit etre tournée ou non
    on utilisera la methode ".extend" pour remplir une liste si besoin'''
    image = []  # crée qui contiendra les images
    for i in range(index_debut, index_debut + nb_image):
        imag = Image.open(chemin + str(i) + '.png')
        if taille != None:
            imag = imag.resize(taille)
        if miroir == True:
            imag = imag.transpose(Image.FLIP_LEFT_RIGHT)
        image.append(ImageTk.PhotoImage(imag, master=fenetre))
    return image

def non_lerp(a: float, b: float, t: float) -> float:
        """Interpolation non linéaire entre a et b en fonction du temps t"""
        return ((1 - t) * a)/1.5 + (t * b)/10

# -------------------menu----------------------------

def new_game():
    '''fonction qui s'occupe de réinitialiser le jeu'''
    monde1()
    
def menu():
    '''lance le menu'''
    # ----clear----
    clear()
    try: toile.delete(visual_boss), toile.delete(boss_hp_bar)
    except:None
    try: toile.delete(visual_boss_frost), toile.delete(frost_hp_bar)
    except:None
    # ----buttons----
    menu_sign.pack(pady = 40)
    play_button.pack(pady = 20)
    settings_button.pack(pady = 20)
    quit_button.pack(pady = 20)

def settings():
    '''affiche les parametres'''
    global text_taille_fenetre,vert_slider,hori_slider,save,text_setting
    clear()
    # les ajouter à la fenêtre
    text_setting.pack()
    text_taille_fenetre.pack(pady=(100,50))
    vert_slider.pack()
    hori_slider.pack()
    save.pack()

    b.pack()

def window_size():
    '''défini la taille de la fenetre, et change la taille des éléments si besoin'''
    global fond1, largeur, hauteur
    largeur = hori_slider.get()
    hauteur = vert_slider.get()
    fenetre.geometry(str(vert_slider.get()) + 'x' + str(hori_slider.get()))
    fond1 = fond1.resize((largeur, hauteur))

def clear():
    '''fonction qui réinitialise tout (variable, élément de la fenetre)'''
    global  frost_hp, boss_frost, visual_boss_frost, fleches, monstres, cupidon, zone, flipped, score, boss, boss_hp, speed, player_atk_speed, light_calculations, boss_is_on
    boss_is_on = False
    player_atk_speed = 100
    speed = 6
    zone = 1
    flipped = False
    toile.itemconfig(light_calculations[0], image=light_calculations[1])
    score = 0
    fleches = []            # listes des flèches tirées : (direction, coo_x, coo_y, images)
    for i in range(len(monstres)):
        toile.delete(monstres[i][3])    
        monstres[i][5] = False
    for i in range(len(potion)):
        toile.delete(potion[i][2])
    monstres = []
    cupidon = [largeur//2, hauteur//2, 'gauche', 'passif']  # liste contenant les infos de cupidon : [x, y, direction("gauche" ou "droite"), action("passif", "tir" ou "mort"), image]
    menu_sign.pack_forget()
    play_button.pack_forget()
    settings_button.pack_forget()
    quit_button.pack_forget()
    toile.pack_forget()
    bouton.pack_forget()
    b.pack_forget()
    text_setting.pack_forget()
    text_taille_fenetre.pack_forget()
    vert_slider.pack_forget()
    hori_slider.pack_forget()
    save.pack_forget()
    monster_death(0)
    frost_hp = 4
    boss_hp = 4
    portal[2] == False
    toile.delete(cupidon_img)
    boss = []
    boss_frost = []

# -------------------jeu----------------------------

def game_over():
    '''fonction qui s'occupe d'afficher perdu et
    de tout arreter quand cupidon est mort'''
    if cupidon[3] == 'mort':
        pass

def switch_side():
    '''fonction qui inverse l'image de fond et téléporte cupidon du coté opposé
    lorsqu'il se trouve aux extrémités. donne une impression d'avancer dans la foret'''
    global light_calculations, cupidon, flipped, monstres, zone, particles
    for i in range(len(monstres)):
        toile.delete(monstres[i][3])
    monstres = []
    for i in range(len(potion)):
        toile.delete(potion[i][2])
    if cupidon[0] >= 990:
        if monde == 1:
            if flipped == False:
                toile.itemconfig(light_calculations[0], image=fond_flipped)
                flipped = True
                particles[0][0] = 660
                particles[1][0] = 660
            elif flipped == True:
                toile.itemconfig(light_calculations[0], image=light_calculations[1])
                flipped = False
                particles[0][0] = 340
                particles[1][0] = 340
        elif monde == 2:
            if flipped == False:
                toile.itemconfig(light_calculations[0], image=img_bg_monde2[0][0])
                flipped = True
            elif flipped == True:
                toile.itemconfig(light_calculations[0], image=img_bg_monde2[1][0])
                flipped = False
        cupidon[0] = 20
        toile.coords(cupidon, cupidon[0], cupidon[1])
        zone -= 1
    elif cupidon[0] <= 10:
        if monde == 1:
            if flipped == False:
                toile.itemconfig(light_calculations[0], image=fond_flipped)
                flipped = True
                particles[0][0] = 660
                particles[1][0] = 660
            elif flipped == True:
                toile.itemconfig(light_calculations[0], image=light_calculations[1])
                flipped = False
                particles[0][0] = 340
                particles[1][0] = 340
        elif monde == 2:
            if flipped == False:
                toile.itemconfig(light_calculations[0], image=img_bg_monde2[0][0])
                flipped = True
            elif flipped == True:
                toile.itemconfig(light_calculations[0], image=img_bg_monde2[1][0])
                flipped = False
        cupidon[0] = 980
        toile.coords(cupidon_img, cupidon[0], cupidon[1])
        zone += 1
    if score > 10 and boss_defeated == False:
        if monde == 1:
            spawn_boss()
        elif monde == 2:
            spawn_frost()
    else:
        spawn_monstre(random.randint(0, nb_monster))

def spawn_potion():
    '''fonction qui fait apparautre des potions donnant des effets au joueur.
    fonction appelée dans monster_death'''
    global potion_lootable, visual_potion
    for i in range(len(monstres)):
        # potion_lootable = random.randint(0,20)
        potion_lootable = 5
        if potion_lootable < 6 and monstres[i][5] == False:
            visual_potion = toile.create_image(monstres[i][1], monstres[i][2], image=img_potion[potion_lootable])
            potion.append([monstres[i][1], monstres[i][2], visual_potion, potion_lootable])

def potion_handler():
    '''fonction qui vérifie si le joueur touche la potion.
    le fait récupérer l'effet de la potion si la fonction est appelée.
    la fonction est appelé dans pression_touche'''
    global speed, player_atk_speed
    def thunder(i):
        '''fonction qui joue une animation d'éclair'''
        toile.itemconfigure(visual_thunder, image=img_thunder[i])
        toile.after(500, thunder, i+1)

    try :
        for i in range(len(potion)):
            if math.sqrt((cupidon[0]-potion[i][0])**2+(cupidon[1]-potion[i][1])**2) < 20:
                toile.delete(potion[i][2])
                # undefined potion
                if potion[i][3] == 0:
                    pass
                # speed potion
                if potion[i][3] == 1:
                    speed += 3
                # undefined potion
                if potion[i][3] == 2:
                    pass
                # atk speed potion
                if potion[i][3] == 4: 
                    player_atk_speed -= 50
                # slowness potion
                if potion[i][3] == 3: 
                    speed -= 3 
                # undefined potion
                if potion[i][3] == 5: 
                    visual_thunder = toile.create_image(500, hauteur, image=img_thunder[0])
                    thunder(0)
                    toile.delete(visual_thunder)   
                potion.remove(potion[i]) 
    except:None 

# -------------------mondes-------------------

def monde1():
    '''fonction qui lance le premier monde : la foret'''
    global monde
    monde = 1
    clear()
    toile.pack()
    toile.itemconfig(light_calculations[0], image=light_calculations[1])
    lucioles_spawner()
    lucioles_spawner2()
    b.pack()
    spawn_cupidon()

def monde2():
    '''fonction qui charge le 2eme monde'''
    global monde
    monde = 2
    toile.delete(visual_portal)
    clear()
    toile.pack()
    toile.itemconfig(light_calculations[0], image=img_bg_monde2[0][0])
    b.pack()
    spawn_cupidon()

def portail_vers_2():
    '''fonction qui fait apparaitre un portail qui téléporte
      le joueur vers le monde 2 à la mort du boss demon'''
    global visual_portal, portal
    if monde == 1:
        print(monde)
        visual_portal = toile.create_image(portal[0], portal[1], image = img_portal[0])
        portal[2] = True

# -------------------joueur-------------------

def spawn_cupidon():
    '''fonction qui fait apparaitre cupidon,
    utile pour le faire réapparaitre s'il meurt'''
    global cupidon_img
    toile.delete(cupidon_img)
    cupidon_img=toile.create_image(cupidon[0], cupidon[1], image =images_cupidon[0])  # on ajoute cupidon à la fenêtre
    toile.coords(cupidon_img, cupidon[0], cupidon[1])
       
def battement_daile(i):
    '''animation de battement d'aile de cupidon'''
    if cupidon[3] == 'passif':
    # s'il est passif : jouer l'animation de passif en changeant les images
        if cupidon[2]=='gauche':
            toile.itemconfig(cupidon_img, image=images_cupidon[i%4])
        if cupidon[2]=='droite':
            toile.itemconfig(cupidon_img, image=images_cupidon[i%4+13])
    
    toile.after(100,battement_daile,i+1)    # faire tourner la fonction en boucle pour donner une animation toutes les 100ms

def pression_touche(event):
    """fonction appelée à chaque fois qu'une touche est appuyée
    Cette fonction prend en compte les touches appuyés pour déplacer cupidon"""
    global KeyPressed, cupidon, Key
    Key = event.keysym  # récupère la touche appuyée
    if cupidon[3] != "mort":    # vérifie si cupidon est en vie
        # -------------------bouge cupidon-----------------
        # si la touche correspondante aux directions est pressée :
        # le fait avancer et changer de directoin si droite ou gauche
        if Key in ['q','Left']:
            cupidon[0]=cupidon[0]-speed
            cupidon[2]='gauche'
        if Key in ['d','Right']:
            cupidon[0]=cupidon[0]+speed
            cupidon[2]='droite'
        if Key in ['z','Up']:
            cupidon[1]=cupidon[1]-speed
        if Key in ['s','Down']:
            cupidon[1]=cupidon[1]+speed
        cupidon[1] += 3*math.sin(time.time()*20)            # lui donne une direction sinusoidale pour donner une impression de voler avec ses ailes
        toile.coords(cupidon_img, cupidon[0], cupidon[1])   # met à jour sa position
        # ----------------- bordures ----------------------
        # défini les bordures : s'il les dépasse, le fait reculer
        if cupidon[0] < 0:
            cupidon[0] += speed
        if cupidon[0] > largeur:
            cupidon[0] -= speed
        if cupidon[1] < 0:
            cupidon[1] += speed
        if cupidon[1] > hauteur:
            cupidon[1] -= speed
        # ---------------changer de zone------------------
        if Key == 'e':
            potion_handler()
            if cupidon[0] >= 990 or cupidon[0] <= 10:
                switch_side()
                toile.coords(cupidon_img, cupidon[0], cupidon[1])   # met à jour sa position
            if math.sqrt((cupidon[0]-portal[0])**2+(cupidon[1]-portal[1])**2) < 50 and portal[2] == True and monde == 1:
                monde2()
        # ----------------- tir -----------------------------
        if Key == 'space' and KeyPressed == False:
            KeyPressed = True   # empêche de spam l'attaque
            cupidon[3] = 'tir'  # met l'action de cupidon à 'tir' pour qu'il arrete de bouger et tirer
            tirer()            # appelle la fonction pour qu'il tire

def tirer():
    '''fonction recursive qui prend en parametre un compteur.
    La fonction va faire defiler les images de cupidon en train de tirer une fleche
    Elle va également ajouter une fleche à la liste de fleche déjà tirées'''
    global cupidon, KeyPressed, fleches
    def shoot_animation(i):
        global cupidon, KeyPressed
        if cupidon[3] == 'tir':
            if cupidon[2]=='gauche':
                toile.itemconfig(cupidon_img, image=images_cupidon[i%4+3])
            if cupidon[2]=='droite':
                toile.itemconfig(cupidon_img, image=images_cupidon[i%4+17])
        if i < 4:
            toile.after(player_atk_speed, shoot_animation, i+1)
        else:
            cupidon[3] = 'passif'
            KeyPressed = False         
    shoot_animation(0)
    if cupidon[2] == 'droite':
        fleche = toile.create_image(cupidon[0], cupidon[1], image = fleche_droite)
        fleches.append(['droite', cupidon[0], cupidon[1], None, fleche])
    if cupidon[2] == 'gauche':
        fleche = toile.create_image(cupidon[0], cupidon[1], image = fleche_gauche)
        fleches.append(['gauche', cupidon[0], cupidon[1], None, fleche])

def avancer_fleche():
    '''fonction récursive qui permt de faire avancer les flechesqui ont deja été tirées,
    la fonction supprime ensuite les fleches qui sont sorties de la fenetre'''
    def lerp(a: float, b: float, t: float) -> float:
        """Interpolation linéaire entre a et b en fonction du temps t"""
        return (1 - t) * a + t * b   
    for i in range(len(fleches)):
        if(i<len(fleches)): #permet d'éviter les problèmes issus de la suppression des flèches en dehors de l'écran
            if fleches[i][0] == 'droite':
                fleches[i][1] += 15
                fleches[i][2] -= math.sin(lerp(1.85,1.5*math.pi,(fleches[i][1]-cupidon[0])/(largeur/1.4)))*2 #modifie la position "y" des flèches pour leur donner de la gravité
                fleches[i][3] = ImageTk.PhotoImage(img_fleche_droite.rotate(lerp(10,-10,(fleches[i][1]-cupidon[0])/(largeur/1.4))), master=toile)
                fleche = toile.create_image(fleches[i][1],fleches[i][2], image = fleches[i][3])
                fleches.append(['droite', fleches[i][1], fleches[i][2], fleches[i][3], fleche])
                toile.delete(fleches[i][4])
                fleches.remove(fleches[i])
            if fleches[i][0] == 'gauche':
                fleches[i][1] -= 15
                fleches[i][2] -= math.sin(lerp(1.85,1.5*math.pi,(cupidon[0]-fleches[i][1])/(largeur/1.4)))*2 #modifie la position y des flèches pour leur donner de la gravité
                fleches[i][3] = ImageTk.PhotoImage(img_fleche_gauche.rotate(lerp(-10,10,(cupidon[0]-fleches[i][1])/(largeur/1.4))), master=toile)
                fleche = toile.create_image(fleches[i][1],fleches[i][2], image = fleches[i][3])
                fleches.append(['gauche', fleches[i][1], fleches[i][2], fleches[i][3], fleche])
                toile.delete(fleches[i][4])
                fleches.remove(fleches[i])
            if fleches[i][1] > largeur or fleches[i][1] < 0: #supprime les flèches en dehors de l'écran pour optimiser le jeu
                toile.delete(fleches[i][4])
                fleches.remove(fleches[i])    
    toile.after(25, avancer_fleche)    # faire tourner la fonction en boucle pour donner une animation toutes les 25ms

def cupidon_death():
    '''fonction qui fait mourir cupidon :
    anime puis le détruit'''
    global cupidon
    cupidon[3] = 'mort'
    def cupidon_death_animation(i):
        if cupidon[2] == 'gauche':
            toile.itemconfig(cupidon_img, image=images_cupidon[i%5+8])
        if cupidon[2] == 'droite':
            toile.itemconfig(cupidon_img, image=images_cupidon[i%5+21])
        if i < 5:
            toile.after(100,cupidon_death_animation,i+1)
        else : toile.delete(cupidon_img)
    if cupidon[3] == 'mort':
        cupidon_death_animation(0)
        game_over()
        # time.sleep(1000, lambda global cupidon: cupidon=[])

def killing_arrow():
    '''fonction qui fait que les flèches tuent les monstres'''
    for i in range(len(fleches)):
        for j in range(len(monstres)):
            if math.sqrt((monstres[j][1]-fleches[i][1])**2+(monstres[j][2]-fleches[i][2])**2) < 25:
                monstres[j][5] = 0
                monster_death(0)
    toile.after(10, killing_arrow)

# ------------------monstres----------------------

def spawn_monstre(nb):
    '''fonction qui fait spawn les monstres, 3 monstres à la fois
    lorsqu'un montre meurt : un autre respawn 
    il est le code principal des monstres où les fonctions correspondantes sont appelées'''
    global monstres, monstre
    for i in range(nb):    # crée 3 monstres
        x = random.randint(0,largeur)
        y = random.randint(0,hauteur)
        dir_monstre = random.randint(0,1)
        monstres.append([dir_monstre, x, y])    # ajoute ces monstres à la liste
        monstre = toile.create_image(monstres[i][1], monstres[i][2], image = img_monstre[0])
        monstres[i].append(monstre)     # ajoute ces monstres à la liste
        monstres[i].append(False)
        monstres[i].append(True)

def monstre_animation(i):
    '''fonction récursive qui s'occupe de l'animation 
    des monstreset est appelé dans "spawn_monstre"'''
    # répète pour chaque monstres
    for j in range(len(monstres)):
        if monstres[j][5] == 1:
            if monstres[j][0]==0:   
                toile.itemconfig(monstres[j][3], image=img_monstre[i%4])
            elif monstres[j][0]==1:
                toile.itemconfig(monstres[j][3], image=img_monstre[i%4+10])
    toile.after(100,monstre_animation,i+1)    # faire tourner la fonction en boucle pour donner une animation toutes les 100ms

def monstre_mvt_idle():
    '''fonction qui s'occupe des déplacements des montres
    lorsqu'il est loin de cupidon : bouge aléatoirement'''
    global mvt_monstre
    # répète pour chaque monstres
    for i in range(len(monstres)):
        # variable définissant quel mouvement le monstre éxecutera : 
        # 0=bouge pas; 1=droite;2=gauche; 3=haut; 4=bas
        mvt_monstre = random.randint(0,4)  
        # ----mouvements----  
        if monstres[i][4] == False and monstres[i][5] == 1:
            if mvt_monstre == 1:
                monstres[i][0] = 0
                monstres[i][1] += 15
            elif mvt_monstre == 2:
                monstres[i][0] = 1
                monstres[i][1] -= 15
            elif mvt_monstre == 3:
                monstres[i][2] += 15
            elif mvt_monstre == 4:
                monstres[i][2] -= 15
        # ----bordures----
        if monstres[i][1] < 0:
            monstres[i][1] += 15
        if monstres[i][1] > largeur:
            monstres[i][1] -= 15
        if monstres[i][2] < 0:
            monstres[i][2] += 15
        if monstres[i][2] > hauteur:
            monstres[i][2] -= 15
        toile.coords(monstres[i][3],monstres[i][1],monstres[i][2])  # met à jour les coordonnées du monstres
    
def is_agro():
    '''fonction récursive appelé dans "spawn_monstre"
    elle utilise la fonction "monstre_mvt_idle" si le monstre est loin
    et "monstre_mvt_agro" si le monstre est proche'''
    # répète pour chaque monstres
    for i in range(len(monstres)):
        # si la distance entre cupidon et un monstre est importante, le monstre en question se balade
        if math.sqrt((cupidon[0]-monstres[i][1])**2+(cupidon[1]-monstres[i][2])**2) > agro_distance and monstres[i][5] == 1:
            toile.after(2000, monstre_mvt_idle)
            monstres[i][4] = False
        # si la distance entre cupidon et un monstre est faible, le monstre en question avance vers lui
        if math.sqrt((cupidon[0]-monstres[i][1])**2+(cupidon[1]-monstres[i][2])**2) < agro_distance and monstres[i][5] == 1:
            monstres[i][4] = True
            toile.after(1, monstre_mvt_agro)
    toile.after(200, is_agro)   # faire tourner la fonction en boucle pour donner une animation toutes les 200ms

def monstre_mvt_agro():#hello sir have a good night, but look under yar bed
    '''fonction qui s'occupe des déplacements des montres
    lorsqu'il est proche : avance vers cupidon'''
    # répète pour chaque monstres
    for i in range(len(monstres)):
        # vérifie si le monstre est agro, si oui : le fait avancer vers le joueur
        if monstres[i][4]==True and monstres[i][5] == 1:
            if cupidon[0]-monstres[i][1] > 0:
                monstres[i][0] = 0
                monstres[i][1] += 10
            if cupidon[0]-monstres[i][1] < 0:
                monstres[i][0] = 1
                monstres[i][1] -= 10
            if cupidon[1]-monstres[i][2] > 0:
                 monstres[i][2] += 10
            if cupidon[1]-monstres[i][2] < 0:
                monstres[i][2] -= 10
        toile.coords(monstres[i][3],monstres[i][1],monstres[i][2])  # met à jour les coordonnées du monstres

def monster_death(j):
    '''fonction qui fait mourir le monstre'''
    global score
    # on boucle sur tout les monstres existant
    for i in range(len(monstres)):
        try:    # permet d'éviter une erreur lorsque plusieurs monstres sont tués en même temps
            if monstres[i][0] == 0 and monstres[i][5] == False:
                # joue l'animation de mort de gauche s'il regarde à gauche et il mort
                toile.itemconfig(monstres[i][3], image=img_monstre[j%7+4])
                if j < 5:
                    toile.after(100,monster_death,j+1)
                else :
                    spawn_potion()
                    toile.delete(monstres[i][3])    # retire le monstre
                    monstres.remove(monstres[i])
                    score += 1  # incrémente le score
                    print(score)    #----------------------------------TEMPORAIRE
            elif monstres[i][0] == 1 and monstres[i][5] == False:
                # joue l'animation de mort de droite s'il regarde à droite et il mort
                toile.itemconfig(monstres[i][3], image=img_monstre[j%7+13])
                if j < 5:
                    toile.after(100,monster_death,j+1)
                else :
                    spawn_potion()
                    toile.delete(monstres[i][3])    # retire le monstre
                    monstres.remove(monstres[i])
                    score += 1  # incrémente le score
                    print(score)    #----------------------------------TEMPORAIRE
        except : score += 2 # rajoute un bonus si 2 monstres sont tués en même temps

def killing_monster():
    '''fonction qui tue le joueur lorque le monstre s'approche'''
    for i in range(len(monstres)):      
        if math.sqrt((cupidon[0]-monstres[i][1])**2+(cupidon[1]-monstres[i][2])**2) < 15:
            cupidon_death()
    toile.after(2000, killing_monster)

# ------------------boss demon----------------------

def spawn_boss():
    '''fonction qui fait apparaitre le boss'''
    global boss, img_boss, visual_boss, boss_hp_bar, boss_is_on, fond1_flipped, fond_flipped
    boss.extend([900,300,"gauche","passif",False,True,False])   # pour les 3 booleens : 1 : agro| 2 : en vie| 3 : attaque
    visual_boss = toile.create_image(boss[0],boss[1], image=img_boss[1][0])
    boss.append(visual_boss)
    boss_hp_bar = toile.create_image(largeur/2, hauteur-400, image=boss_health_bar[4-boss_hp])
    boss_idle_animation(0)
    boss_is_agro()
    boss_walk_anim(0)
    boss_atk()
    boss_health()
    boss_death(0)
    boss_is_on = True
    load_fullimg()
    fond1_flipped = light_calculations[2].transpose(Image.FLIP_LEFT_RIGHT)
    fond_flipped = ImageTk.PhotoImage(fond1_flipped, master = toile)

def boss_idle_animation(i):
    '''fonction récursive lorsque le boss est en vie qui anime le boss lorsqu'il ne bouge pas'''
    try:
        if boss[5]:
            if boss[3] == "passif":
                if boss[2] == "gauche":
                    toile.itemconfig(visual_boss, image=img_boss[0][i%6])
                elif boss[2] == "droite":
                    toile.itemconfig(visual_boss, image=img_boss[1][i%6])
        toile.after(100,boss_idle_animation,i+1)    # faire tourner la fonction en boucle pour donner une animation toutes les 100ms    
    except:None

def boss_walk_anim(i):
    '''animation de marche du boss'''
    try:
        if boss[5]:
            if boss[3] == "marche":
                if boss[2] == "gauche":
                    toile.itemconfig(visual_boss, image=img_boss[0][i%11+6])
                elif boss[2] == "droite":
                    toile.itemconfig(visual_boss, image=img_boss[1][i%11+6])
        toile.after(100,boss_walk_anim, i+1)
    except:None

def boss_mvt_idle():
    '''fonction qui s'occupe des mouvements du boss lorsqu'il n'aperçoit pas le joueur'''
    global boss
    mvt_boss = random.randint(0,2)
    # variable définissant quel mouvement le boss éxecutera : 
    # 0=bouge pas; 1=droite;2=gauche
    try:
        if boss[5] == True:
            # ----mouvements----  
            if boss[4] == False:
                if mvt_boss == 0:
                    boss[3] = "passif"
                if mvt_boss == 1:
                    boss[3] = "marche"
                    boss[2] = "droite"
                    boss[0] += 15
                elif mvt_boss == 2:
                    boss[3] = "marche"
                    boss[2] = "gauche"
                    boss[0] -= 15
            # ----bordures----
            if boss[0] < 0:
                boss[0] += 15
            if boss[0] > largeur:
                boss[0] -= 15
            toile.coords(visual_boss, boss[0], boss[1])  # met à jour les coordonnées du boss
    except:None

def boss_mvt_agro():
    '''fonction qui s'occupe des mouvement du boss lorsqu'il aperçoit le joueur'''
    global boss
    try:
        if boss[5] == True:
            # ---mouvements---
            if boss[4] == True:
                if cupidon[0]-boss[0] > 15:
                    boss[0] += 15
                    boss[3] = "marche"
                    boss[2] = "droite"
                elif cupidon[0]-boss[0] < 0:
                    boss[0] -= 15
                    boss[3] = "marche"
                    boss[2] = "gauche"
                else : 
                    boss[3] = "passif"
            # ---bordures---
            if boss[0] < 0:
                boss[0] += 15
            if boss[0] > largeur:
                boss[0] -= 15
        toile.coords(visual_boss, boss[0], boss[1])  # met à jour les coordonnées du boss
    except:None

def boss_is_agro():
    '''fonction qui s'occupe de savoir si le boss voit le joueur ou non'''
    try:
        if boss[5] == True:
            if math.sqrt((cupidon[0]-boss[0])**2+(cupidon[1]-boss[1])**2) > 650:
                toile.after(2000, boss_mvt_idle)
                boss[4] = False
            # si la distance entre cupidon et un monstre est faible, le monstre en question avance vers lui
            if math.sqrt((cupidon[0]-boss[0])**2+(cupidon[1]-boss[1])**2) <= 650:
                boss[4] = True
                toile.after(2000, boss_mvt_agro)
        toile.after(200, boss_is_agro)   # faire tourner la fonction en boucle pour donner une animation toutes les 200ms
    except:None

def boss_atk_anim(i):
    '''fonction qui s'occupe de l'animation de l'attaque du boss'''
    global boss, visual_boss
    boss[3]="atk"
    boss[6] = True
    if i<=15:
        if boss[3] == "atk":
            if boss[2]=="gauche":
                toile.itemconfig(visual_boss, image=img_boss[0][i%15+18])
            elif boss[2]=="droite":
                toile.itemconfig(visual_boss, image=img_boss[1][i%15+18])
        toile.after(100, boss_atk_anim, i+1)
    else:
        boss[3] = "passif"
        boss[6] = False

def boss_atk():
    '''fonction qui s'occupe de l'attaque du boss'''
    def boss_damage():
            '''tue cupidon si trop proche de l'attaque'''
            if math.sqrt((cupidon[0]-boss[0])**2+(cupidon[1]-boss[1])**2) < 70:
                cupidon_death()
    try:
        if boss[5] == True:
            if math.sqrt((cupidon[0]-boss[0])**2+(cupidon[1]-boss[1])**2) < 70 and boss[6] == False and cupidon[3] != "mort":
                boss_atk_anim(0)
                toile.after(1000, boss_damage)
        toile.after(100,boss_atk)
    except:None

def boss_takehit_anim(i):
    '''animation du boss quand il est touché par une fleche'''
    global boss, visual_boss
    if i<= 5:
        if boss[2]=="gauche":
            toile.itemconfig(visual_boss, image=img_boss[0][i%5+55])
        elif boss[2]=="droite":
            toile.itemconfig(visual_boss, image=img_boss[1][i%5+55])
        toile.after(100, boss_takehit_anim, i+1)

def boss_health():
    '''fonction qui détermine la santé du boss'''
    global boss_hp
    def boss_hit():
        global boss_hp
        boss_hp -= 1
    try:
        for i in range(len(fleches)):
            if math.sqrt((boss[0]-fleches[i][1])**2+(boss[0]-fleches[i][2])**2) < 200 and boss_hp > 0:
                boss_takehit_anim(0)    
                toile.after(400 ,boss_hit)
        toile.itemconfig(boss_hp_bar, image=boss_health_bar[4-boss_hp])
        if boss_hp <= 0:
            boss_death(0)
        else:
            toile.after(500, boss_health)
    except : boss_health

def boss_death(i):
    '''fonction qui s'occupe de la mort du boss'''
    global boss, boss_defeated, boss_is_on
    try:
        if boss_hp <= 0 and boss[2]=="gauche":
            boss_is_on = False
            # joue l'animation de mort de gauche s'il regarde à gauche
            boss[5] = False
            toile.itemconfig(visual_boss, image=img_boss[0][i%21+33])
            if i < 21:
                toile.after(100,boss_death,i+1)
            else :
                boss_defeated = True
                toile.delete(visual_boss)    # retire le boss
                boss.remove(boss)
        elif boss_hp <= 0 and boss[2]=="droite":
            boss_is_on = False
            # joue l'animation de mort de droite s'il regarde à droite
            boss[5] = False
            toile.itemconfig(visual_boss, image=img_boss[1][i%21+33])
            if i < 21:
                toile.after(100,boss_death,i+1)
            else :
                boss_defeated = True
                toile.delete(visual_boss)    # retire le boss
                boss.remove(boss)
    except : None 

# ------------------boss frost----------------------

def spawn_frost():
    '''fonction qui fait apparaitre le boss des neiges et active toutes ses fonctions'''
    global boss_frost, img_boss_frost, frost_hp, visual_boss_frost, frost_hp_bar, boss_is_on
    boss_frost.extend([800,370,"gauche","passif",False,True,False])   # pour les 3 booleens : 1 : agro| 2 : en vie| 3 : attaque
    visual_boss_frost = toile.create_image(boss_frost[0], boss_frost[1], image=img_boss_frost[0][0])
    boss_frost.append(visual_boss_frost)
    frost_hp_bar = toile.create_image(largeur/2, hauteur-500, image=img_frost_health[4-frost_hp])
    frost_idle_animation(0)
    frost_is_agro()
    frost_walk_anim(0)
    frost_atk()
    frost_health()
    frost_death(0)
    boss_is_on = True

def frost_idle_animation(i):
    '''fonction récursive lorsque le boss est en vie qui anime le boss lorsqu'il ne bouge pas'''
    try:
        if boss_frost[5]:
            if boss_frost[3] == "passif":
                if boss_frost[2] == "gauche":
                    toile.itemconfig(visual_boss_frost, image=img_boss_frost[0][i%6])
                elif boss_frost[2] == "droite":
                    toile.itemconfig(visual_boss_frost, image=img_boss_frost[1][i%6])
        toile.after(100,frost_idle_animation,i+1)    # faire tourner la fonction en boucle pour donner une animation toutes les 100ms    
    except:None

def frost_mvt_idle():
    '''fonction qui s'occupe des mouvements du boss lorsqu'il n'aperçoit pas le joueur'''
    global boss_frost
    mvt_boss = random.randint(0,2)
    # variable définissant quel mouvement le boss éxecutera : 
    # 0=bouge pas; 1=droite;2=gauche
    try:
        if boss_frost[5] == True:
            # ----mouvements----  
            if boss_frost[4] == False:
                if mvt_boss == 0:
                    boss_frost[3] = "passif"
                if mvt_boss == 1:
                    boss_frost[3] = "marche"
                    boss_frost[2] = "droite"
                    boss_frost[0] += 15
                elif mvt_boss == 2:
                    boss_frost[3] = "marche"
                    boss_frost[2] = "gauche"
                    boss_frost[0] -= 15
            # ----bordures----
            if boss_frost[0] < 0:
                boss_frost[0] += 15
            if boss_frost[0] > largeur:
                boss_frost[0] -= 15
            toile.coords(visual_boss_frost, boss_frost[0], boss_frost[1])  # met à jour les coordonnées du boss
    except:None

def frost_walk_anim(i):
    '''animation de marche du boss'''
    try:
        if boss_frost[5]:
            if boss_frost[3] == "marche":
                if boss_frost[2] == "gauche":
                    toile.itemconfig(visual_boss_frost, image=img_boss_frost[0][i%10+6])
                elif boss_frost[2] == "droite":
                    toile.itemconfig(visual_boss_frost, image=img_boss_frost[1][i%10+6])
        toile.after(100,frost_walk_anim, i+1)
    except:None

def frost_mvt_agro():
    '''fonction qui s'occupe des mouvement du boss lorsqu'il aperçoit le joueur'''
    global boss_frost
    try:
        if boss_frost[5] == True:
            # ---mouvements---
            if boss_frost[4] == True:
                if cupidon[0]-boss_frost[0] > 15:
                    boss_frost[0] += 15
                    boss_frost[3] = "marche"
                    boss_frost[2] = "droite"
                elif cupidon[0]-boss_frost[0] < 0:
                    boss_frost[0] -= 15
                    boss_frost[3] = "marche"
                    boss_frost[2] = "gauche"
                else : 
                    boss_frost[3] = "passif"
            # ---bordures---
            if boss_frost[0] < 0:
                boss_frost[0] += 15
            if boss_frost[0] > largeur:
                boss_frost[0] -= 15
        toile.coords(visual_boss_frost, boss_frost[0], boss_frost[1])  # met à jour les coordonnées du boss
    except:None

def frost_is_agro():
    '''fonction qui s'occupe de savoir si le boss voit le joueur ou non'''
    try:
        if boss_frost[5] == True:
            if math.sqrt((cupidon[0]-boss_frost[0])**2+(cupidon[1]-boss_frost[1])**2) > 650:
                toile.after(2000, frost_mvt_idle)
                boss_frost[4] = False
            # si la distance entre cupidon et un monstre est faible, le monstre en question avance vers lui
            if math.sqrt((cupidon[0]-boss_frost[0])**2+(cupidon[1]-boss_frost[1])**2) <= 650:
                boss_frost[4] = True
                toile.after(2000, frost_mvt_agro)
        toile.after(200, frost_is_agro)   # faire tourner la fonction en boucle pour donner une animation toutes les 200ms
    except:frost_is_agro

def frost_atk_anim(i):
    '''fonction qui s'occupe de l'animation de l'attaque du boss'''
    global boss_frost, visual_boss_frost
    boss_frost[3]="atk"
    boss_frost[6] = True
    if i<=15:
        if boss_frost[3] == "atk":
            if boss_frost[2]=="gauche":
                toile.itemconfig(visual_boss_frost, image=img_boss_frost[0][i%14+17])
            elif boss_frost[2]=="droite":
                toile.itemconfig(visual_boss_frost, image=img_boss_frost[1][i%14+17])
        toile.after(100, frost_atk_anim, i+1)
    else:
        boss_frost[3] = "passif"
        boss_frost[6] = False

def frost_atk():
    '''fonction qui s'occupe de l'attaque du boss'''
    def frost_damage():
            '''tue cupidon si trop proche de l'attaque'''
            if math.sqrt((cupidon[0]-boss_frost[0])**2+(cupidon[1]-boss_frost[1])**2) < 70:
                cupidon_death()
    try:
        if boss_frost[5] == True:
            if math.sqrt((cupidon[0]-boss_frost[0])**2+(cupidon[1]-boss_frost[1])**2) < 70 and boss_frost[6] == False and cupidon[3] != "mort":
                frost_atk_anim(0)
                toile.after(1000, frost_damage)
        toile.after(100,frost_atk)
    except:frost_atk

def frost_takehit_anim(i):
    '''animation du boss quand il est touché par une fleche'''
    global boss_frost, visual_boss_frost
    if i<= 7:
        if boss_frost[2]=="gauche":
            toile.itemconfig(visual_boss_frost, image=img_boss_frost[0][i%7+46])
        elif boss_frost[2]=="droite":
            toile.itemconfig(visual_boss_frost, image=img_boss_frost[1][i%7+46])
        toile.after(100, frost_takehit_anim, i+1)

def frost_health():
    '''fonction qui détermine la santé du boss'''
    global frost_hp
    def boss_hit():
        global frost_hp
        frost_hp -= 1
    try:
        for i in range(len(fleches)):
            if math.sqrt((boss_frost[0]-fleches[i][1])**2+(boss_frost[0]-fleches[i][2])**2) < 200 and frost_hp > 0:
                frost_takehit_anim(0)    
                toile.after(400 ,boss_hit)
        toile.itemconfig(frost_hp_bar, image=boss_health_bar[4-frost_hp])
        if frost_hp <= 0:
            frost_death(0)
        else:
            toile.after(500, frost_health)
    except : frost_health

def frost_death(i):
    '''fonction qui s'occupe de la mort du boss'''
    global boss_frost, boss_defeated, boss_is_on
    try:
        if boss_hp <= 0 and boss_frost[2]=="gauche":
            boss_is_on = False
            # joue l'animation de mort de gauche s'il regarde à gauche
            boss[5] = False
            toile.itemconfig(visual_boss_frost, image=img_boss_frost[0][i%21+33])
            if i < 21:
                toile.after(100, frost_death, i+1)
            else :
                boss_defeated = True
                toile.delete(visual_boss_frost)    # retire le boss
                boss.remove(boss_frost)
        elif boss_hp <= 0 and boss_frost[2]=="droite":
            boss_is_on = False
            # joue l'animation de mort de droite s'il regarde à droite
            boss_frost[5] = False
            toile.itemconfig(visual_boss_frost, image=img_boss_frost[1][i%21+33])
            if i < 21:
                toile.after(100,frost_death,i+1)
            else :
                boss_defeated = True
                toile.delete(visual_boss_frost)    # retire le boss
                boss.remove(boss_frost)
    except : None

#-------------------décor--------------------

def lucioles_spawner():
    global startTime_lucioles
    startTime_lucioles = time.time()
    particle_system("lucioles", startTime_lucioles)
    toile.after((luciole_duration*1000)+1000,lucioles_spawner)    # faire tourner la fonction en boucle pour donner une animation toutes les 10000ms

def lucioles_spawner2():
    global startTime_lucioles2
    startTime_lucioles2 = time.time()
    particle_system("lucioles2", startTime_lucioles2)
    toile.after((luciole_duration2*1000)+1000,lucioles_spawner2)    # faire tourner la fonction en boucle pour donner une animation toutes les 10000ms  

def mvt_luciole(particle_l,i):
    for y in range(len(particle_l)):
        if math.sqrt((particles[i][0]-toile.coords(particle_l[y])[0])**2 + (particles[i][1]-toile.coords(particle_l[y])[3])**2) < 20:
            displacement_x = (speed*random.randint(-2,2))
            displacement_y = (speed*random.randint(-2,2))
            toile.coords(particle_l[y], toile.coords(particle_l[y])[0]+displacement_x, toile.coords(particle_l[y])[1]+displacement_y, toile.coords(particle_l[y])[2]+displacement_x, toile.coords(particle_l[y])[3]+displacement_y)
        else:
            displacement_x = ((particles[i][0]-toile.coords(particle_l[y])[0])*random.randint(0,3))/10
            displacement_y = ((particles[i][1]-toile.coords(particle_l[y])[3])*random.randint(0,3))/10
            toile.coords(particle_l[y], toile.coords(particle_l[y])[0]+displacement_x, toile.coords(particle_l[y])[1]+displacement_y, toile.coords(particle_l[y])[2]+displacement_x, toile.coords(particle_l[y])[3]+displacement_y)

def particle_system(name, startTime):
    for i in range(len(particles)):
        if particles[i][6] == name:
            #on met en place les particules
            timediff = (time.time()-startTime)
            if timediff <= particles[i][5]:

                if timediff > (particles[i][5]/particles[i][3]+(len(particles[i][8])*(particles[i][5]/particles[i][3]))):
                    #on bouge les particules
                    if particles[i][6] == "lucioles" or particles[i][6] == "lucioles2":
                        mvt_luciole(particles[i][8], i)
                    
                    #on en crée des nouvelles
                    particle = toile.create_rectangle(particles[i][0]-particles[i][2]/2, particles[i][1]-particles[i][2]/2, particles[i][0]+particles[i][2]/2, particles[i][1]+particles[i][2]/2, fill= particles[i][4])
                    particles[i][8].append(particle)
                toile.after(100,particle_system, name, startTime)
            else :
                #lorsqu'on a terminé, on les retires
                for y in range(len(particles[i][8])):
                    toile.delete(particles[i][8][0])
                    particles[i][8].remove(particles[i][8][0])
                # print(len(particles[i][8])) --------------------------------TEMPORAIRE-----------------------------------------

'''def load_img():
    with multiprocessing.Pool(number_of_processors) as p:
        jobs = []
        #cutting the image in 200 by 200 px parts (most optimized too)
        for x in range(0, largeur, tile_size):
            for y in range(0, hauteur, tile_size):
                jobs.append([x, y, fond2.crop((x, y, x + tile_size, y + tile_size)), tile_size, boss_is_on])
        for _x, _y, result in p.starmap(process_tile, jobs):
            # (paste the result back in the image at x/y
            light_calculations[2].paste(result, (_x, _y))
            # (update the photoimage with the current result)
            light_calculations[1] = ImageTk.PhotoImage(light_calculations[2], master = toile)
            toile.itemconfigure(light_calculations[0], image = light_calculations[1])

def process_tile(_x, _y, tile, size, boss_is_on):
    lightposes=[] #1st = xpose, 2nd = ypose, 3rd = size, 4th = intensity (inversed), 5th = colour
    #--------illumination globale---------
    lightposes.append([500, 300, 1000, 0.85, [2,2,1]])
 
    # --------light for the fireflies---------
    lightposes.append([340, 300, 75, 0, [0, 255, 0]])
    lightposes.append([340, 300, 130, 1, [0, 255, 0]])

    if boss_is_on:
        #-------boss lighting---------
        lightposes.append([400, -300, 1200, 0, [200,20,30]])
        lightposes.append([1100, 200, 2000, 0, [170,20,10]])
    else:
        #-------normal lighting-------
        lightposes.append([1400, -200, 2050, 0.82, [120,170,150]])
        lightposes.append([200, -1200, 1900, 0.01, [0,12,150]])
    # (do processing on the tile)
    def non_lerp(a: float, b: float, t: float) -> float:
        """Interpolation non linéaire entre a et b en fonction du temps t"""
        return ((1 - t) * a)/1.5 + (t * b)/10
    for x in range(size):                                # on parcourt les pixels en colonne
        for y in range(size):                            # on parcourt les pixels en ligne
            r = tile.getpixel((x, y))[0]
            v = tile.getpixel((x, y))[1]
            b = tile.getpixel((x, y))[2]
            g = int(((r+v+b))/3)
            total_light_intensites = []
            for i in range(len(lightposes)):
                distance = math.sqrt((lightposes[i][0]-(_x+x))**2+(lightposes[i][1]-(_y+y))**2)
                if distance <= lightposes[i][2]:
                    r+=lightposes[i][4][0]
                    v+=lightposes[i][4][1]
                    b+=lightposes[i][4][2]
                    pointlight_intensite = 0
                    if((distance/lightposes[i][2])+(lightposes[i][3])<=1):
                        pointlight_intensite = non_lerp(1,0.1,(distance/lightposes[i][2])+(lightposes[i][3])) 
                    total_light_intensites.append(pointlight_intensite)
            red_color,green_color,blue_color = 0,0,0
            for i in range(len(total_light_intensites)):
                red_color += int(total_light_intensites[i]*(r*g)/200)
                green_color += int(total_light_intensites[i]*(v*g)/200)
                blue_color += int(total_light_intensites[i]*(b*g)/200)
                final_pixel_color = (red_color,green_color,blue_color)
            tile.putpixel((x,y),final_pixel_color)
    return _x, _y, tile'''

def load_fullimg():
    with multiprocessing.Pool(number_of_processors) as p:
        jobs = []
        r = random.randint(0,2) #select the next room illumination
        #cutting the image in 200 by 200 px parts (most optimized too)
        for x in range(0, largeur, tile_size):
            for y in range(0, hauteur, tile_size):
                jobs.append([x, y, fond2.crop((x, y, x + tile_size, y + tile_size)), tile_size, boss_is_on, r])
        for _x, _y, result in p.starmap(process_tile_global_lighting, jobs):
            # (paste the result back in the image at x/y
            light_calculations[2].paste(result, (_x, _y))
            # (update the photoimage with the current result)
            light_calculations[1] = ImageTk.PhotoImage(light_calculations[2], master = toile)
            toile.itemconfigure(light_calculations[0], image = light_calculations[1])

def process_tile_global_lighting(_x, _y, tile, size, boss_is_on, r):
    lightposes=[] #1st = xpose, 2nd = ypose, 3rd = size, 4th = intensity (inversed), 5th = colour
    #--------illumination globale---------
    lightposes.append([500, 300, 1000, 0.85, [2,2,1]])

    # --------light for the fireflies---------
    lightposes.append([340, 300, 75, 0, [0, 255, 0]])
    lightposes.append([340, 300, 130, 1, [0, 255, 0]])

    if boss_is_on: #new img lights for the bossroom
        lightposes.append([1400, -200, 2850, 0.52, [237,0,0]])
        lightposes.append([1100, 200, 1400, 0.08, [233,56,63]])
    else: #normal lighting
        if r == 0:
            lightposes.append([1400, -200, 2050, 0.82, [120,170,150]])
            lightposes.append([200, -1200, 1900, 0.01, [0,12,150]])
        if r == 1:
            lightposes.append([100, -200, 1250, 0.72, [110,10,190]])
            lightposes.append([1100, -200, 1400, 0.06, [120,0,150]])
        if r == 2:
            lightposes.append([1400, 1200, 2050, 0.62, [0,170,150]])
            lightposes.append([200, -1200, 1900, 0.01, [20,162,150]])
    # (do processing on the tile)
    for x in range(size):                                # on parcourt les pixels en colonne
        for y in range(size):                            # on parcourt les pixels en ligne
            r = tile.getpixel((x, y))[0]
            v = tile.getpixel((x, y))[1]
            b = tile.getpixel((x, y))[2]
            g = int(((r+v+b))/3)
            total_light_intensites = []
            for i in range(len(lightposes)):
                distance = math.sqrt((lightposes[i][0]-(_x+x))**2+(lightposes[i][1]-(_y+y))**2)
                if distance <= lightposes[i][2]:
                    r+=lightposes[i][4][0]
                    v+=lightposes[i][4][1]
                    b+=lightposes[i][4][2]
                    pointlight_intensite = 0
                    if((distance/lightposes[i][2])+(lightposes[i][3])<=1):
                        pointlight_intensite = non_lerp(1,0.1,(distance/lightposes[i][2])+(lightposes[i][3])) 
                    total_light_intensites.append(pointlight_intensite)

            red_color,green_color,blue_color = 0,0,0
            for i in range(len(total_light_intensites)):
                red_color += int(total_light_intensites[i]*(r*g)/200)
                green_color += int(total_light_intensites[i]*(v*g)/200)
                blue_color += int(total_light_intensites[i]*(b*g)/200)
                final_pixel_color = (red_color,green_color,blue_color)
            tile.putpixel((x,y),final_pixel_color)
    return _x, _y, tile

# --------------------------------------------------------------------programme principal--------------------------------------------------------------------
if __name__=="__main__": #if ya don't wanna die, don't touch it (isidore to jean)
    multiprocessing.freeze_support()
# ------------------------------ éléments de la fenêtre ------------------------------
    fenetre=tk.Tk()     # on créé la fenêtre
    largeur=1000        # on définit les dimensions de la fenêtre
    hauteur=600
    bg_colour = '#7ace54'
    fenetre.geometry('1000x700')
    fenetre.configure(background=bg_colour)
    toile = tk.Canvas(fenetre, width=largeur, height=hauteur)   # on crée une "toile" dans la fen^tre dans laquelle on pourra dessiner
    bouton = tk.Button(fenetre, text='Quitter', command = fenetre.destroy)  # on crée un bouton pour quitter le jeu
    toile.pack()        # on place la toile dans la fenêtre
    bouton.pack()       # on place le bouton dans la fenêtre
    # ------------test------------------
    def test():
        global boss_hp
        boss_hp -= 1
        print(boss_hp)
    a= tk.Button(fenetre, text='monde2', command = portail_vers_2) # bouton pour tester des fonction si besoin
    a.pack()
    c = tk.Button(fenetre, text='monde1', command = monde1) # bouton pour tester des fonction si besoin
    c.pack()
    b= tk.Button(fenetre, text='menu', command = menu) # bouton pour tester des fonction si besoin
    b.pack()

# -------------------------------- images --------------------------------
    # --------------GUI--------------
    menu2 = Image.open("img/GUI/menu.png")
    menu1 = ImageTk.PhotoImage(menu2)
    menu_sign = tk.Label(fenetre, image=menu1, bg=bg_colour)
    play2 = Image.open("img/GUI/play.png")
    play1 = ImageTk.PhotoImage(play2)
    play_button = tk.Button(fenetre, image=play1, bg=bg_colour, command = new_game)
    quit2 = Image.open("img/GUI/quit.png")
    quit1 = ImageTk.PhotoImage(quit2)
    quit_button = tk.Button(fenetre, image=quit1, bg=bg_colour, command = fenetre.destroy)
    settings2 = Image.open("img/GUI/settings.png")
    settings1 = ImageTk.PhotoImage(settings2)
    settings_button = tk.Button(fenetre, image=settings1, bg=bg_colour, command = settings)
    boss_health_bar = []
    boss_health_bar.extend(charger_image('img/GUI/boss_health_', 5))
    # boutons parametres
    text_setting = tk.Label(image=settings1, bg=bg_colour)
    text_taille_fenetre = tk.Label(fenetre, text='Taille de la Fenêtre')
    vert_slider = tk.Scale(fenetre, from_=800, to=2000, orient='horizontal')
    hori_slider = tk.Scale(fenetre, from_=660, to=1020, orient='horizontal')
    save = tk.Button(fenetre, text='Sauvegarder', command = window_size)

    # ---------décor---------
    fond1 = Image.open("img/decor/monde1/fond.png")              # on ouvre l'image à modifier
    bg = ImageTk.PhotoImage(fond1)
    bg1 = tk.Label(fenetre, image=bg)
    fond1 = fond1.resize((largeur, hauteur))        # on redimensionne l'image par rapport à la taille de la fenêtre
    fond2 = fond1.copy()                            # on créé une copie de cette image
    fond3 = ImageTk.PhotoImage(fond2, master = toile)
    # on les ajoutes à la toile
    main_image = toile.create_image(largeur/2,hauteur/2, image = fond3)

    # -----------cupidon-----------
    images_cupidon=[]      # liste qui va contenir toutes les images de cupidon
    images_cupidon.extend(charger_image('img/perso/perso_', 26, None, 0))

    # ---------fleches---------
    img_fleche_gauche = Image.open('img/Fleche1.png')   # on ouvre les images des fleches
    img_fleche_droite = Image.open('img/Fleche2.png')
    fleche_gauche = ImageTk.PhotoImage( img_fleche_gauche, master=toile)    # permet de pouvoir ajouter les fleches à la toile
    fleche_droite = ImageTk.PhotoImage( img_fleche_droite, master=toile)

    #------------monstres------------
    img_monstre = []    # liste qui va contenir toutes les images des monstres
    img_monstre.extend(charger_image('img/mechant/mechant_', 19, None, 0))

    #------------boss demon------------
    img_boss = [[],[]]  # contient toutes les images du boss [0]:regarde à gauche | [1]: droite
    # images gauche
    img_boss[0].extend(charger_image('img/boss/boss_demon/demon_idle/demon_idle_', 6, (700, 420)))         # images idle 0-5
    img_boss[0].extend(charger_image('img/boss/boss_demon/demon_walk/demon_walk_', 12, (700, 420)))        # images marche 6-17
    img_boss[0].extend(charger_image('img/boss/boss_demon/demon_cleave/demon_cleave_', 15, (700, 420)))    # image attaque 18-32
    img_boss[0].extend(charger_image('img/boss/boss_demon/demon_death/demon_death_', 22, (700, 420)))      # images mort 33-54
    img_boss[0].extend(charger_image('img/boss/boss_demon/demon_take_hit/demon_take_hit_', 5, (700, 420))) # images prend des coups 55-60
    # images droite
    img_boss[1].extend(charger_image('img/boss/boss_demon/demon_idle/demon_idle_', 6, (700, 420), miroir=True))
    img_boss[1].extend(charger_image('img/boss/boss_demon/demon_walk/demon_walk_', 12, (700, 420), miroir=True))
    img_boss[1].extend(charger_image('img/boss/boss_demon/demon_cleave/demon_cleave_', 15, (700, 420), miroir=True))
    img_boss[1].extend(charger_image('img/boss/boss_demon/demon_death/demon_death_', 22, (700, 420), miroir=True))
    img_boss[1].extend(charger_image('img/boss/boss_demon/demon_take_hit/demon_take_hit_', 5, (700, 420), miroir=True))

    #------------potion------------
    img_potion = []
    img_potion_particles = []
    img_thunder = []
    img_potion.extend(charger_image('img/potion/potion_', 6,(30, 40)))
    img_potion_particles.extend(charger_image('img/potion/potion_particle_', 6,(30, 40)))
    img_thunder.extend(charger_image('img/potion/thunder/thunder_', 7))

    # -----------monde2-----------
    img_bg_monde2 = [[],[]]
    img_bg_monde2[0].extend(charger_image('img/decor/monde2/monde2_', 8, (largeur, hauteur)))
    img_bg_monde2[1].extend(charger_image('img/decor/monde2/monde2_', 8, (largeur, hauteur), miroir=True))
    img_portal = []
    img_portal.extend(charger_image('img/portal_', 1))

    #------------boss frost------------
    img_boss_frost = [[],[]]  # contient toutes les images du boss [0]:regarde à gauche | [1]: droite
    # images gauche
    img_boss_frost[0].extend(charger_image('img/boss/boss_frost/idle/idle_', 6, (700, 420)))         # image idle 0-5
    img_boss_frost[0].extend(charger_image('img/boss/boss_frost/walk/walk_', 10, (700, 420)))        # images marche 6-16
    img_boss_frost[0].extend(charger_image('img/boss/boss_frost/1_atk/1_atk_', 14, (700, 420)))      # images attaque 17-31
    img_boss_frost[0].extend(charger_image('img/boss/boss_frost/death/death_', 16, (700, 420)))      # images mort 32-48
    img_boss_frost[0].extend(charger_image('img/boss/boss_frost/take_hit/take_hit_', 7, (700, 420))) # images prend des coups 49-56
    # images droite
    img_boss_frost[1].extend(charger_image('img/boss/boss_frost/idle/idle_', 6, (700, 420), miroir=True))         # image idle 0-6
    img_boss_frost[1].extend(charger_image('img/boss/boss_frost/walk/walk_', 10, (700, 420), miroir=True))        # images marche 7-17
    img_boss_frost[1].extend(charger_image('img/boss/boss_frost/1_atk/1_atk_', 14, (700, 420), miroir=True))      # images attaque 18-32
    img_boss_frost[1].extend(charger_image('img/boss/boss_frost/death/death_', 16, (700, 420), miroir=True))      # images mort 33-49
    img_boss_frost[1].extend(charger_image('img/boss/boss_frost/take_hit/take_hit_', 7, (700, 420), miroir=True)) # images prend des coups 50-57
    # sa barre de vie
    img_frost_health = []
    img_frost_health.extend(charger_image('img/GUI/frost_health_', 4, (700,50)))

#---------------------------------------LIGHT CALCULATION HARD---------------------------------------

    #--------------calculs de la lumière--------------
    light_calculations = [main_image, fond3, fond2, fond1]
    """ attention ligthposes pour la position, taille et couleur des lumieres se trouve dans process_tile"""
    #---BOSS[LEVEL LIGHTING]---
    boss_is_on = False
    #--------------------------Multiprocessing!!!!!--------------------------

    startTime = time.time()
    number_of_processors = 8    #8 processors is the most optimised number for me, 5 for school
    tile_size = 200             #200 is the most optimized

    load_fullimg()
    fond1_flipped = light_calculations[2].transpose(Image.FLIP_LEFT_RIGHT)
    fond_flipped = ImageTk.PhotoImage(fond1_flipped, master = toile)
    print(time.time()-startTime)
    
    #----------------systeme de particle-------------------
    particles = []  # [x, y, taille de la particule, nombre de particule, couleur, durée, NOM, vitesse, EMPTY LIST]
    particles.append([340, 300, 3, 14, 'lightgreen', 12, "lucioles", 1, []])
    particles.append([340, 300, 3, 7, 'green', 4, "lucioles2", 2, []])
    # --------lucioles----------
    startTime_lucioles = 0
    luciole_duration = particles[0][5]
    lucioles_spawner()
    startTime_lucioles2 = 0
    luciole_duration2 = particles[1][5]
    lucioles_spawner2()

# ----------------------------------------------------- variables globales -----------------------------------------------------------
    monde = 1               # dans quel monde se trouve cupidon 1 ou 2
    score = 0               # variable cachée du joueur, détermine le score et active le combat de boss à 10 de score
    flipped = False         # variable qui détermine la rotation de la forêt : est changée 1/2 pour donner une impression de changer d'endroit
    zone = 0                # variable qui détermine dans qu'elle zone cupidon se trouve(-x : gauche/+x : droite)
    agro_distance = 400     # variable qui détermine la distance à laquelle le monstre apercevra le joueur
    nb_monster = 5          # variable qui détermine le nombre de monstres
    speed = 6               # vitesse de déplacement de cupidon
    player_atk_speed = 100  # vitesse des attaques de cupidon
    KeyPressed = False      # vérifie si une touche est appuyé
    boss_hp = 4             # variable qui donne la vie du boss
    frost_hp = 4            # variable qui donne la vie du boss des neiges
    boss_defeated = False   # variable qui détermine si le boss a été battu ou non
    potion_drops = True     # variable qui détermine s'il y aura des potions lors de la partie True : oui / False : non
    potion_lootable = None  # nombre alétoire : c'est la chance d'obtenir une potion (0 à 5 : oui et donne la potion correspondante/6 à 20:non )
    portal = [500, 500, False] # liste info du portail : [x, y, apparut]
    potion = []             # liste contenant les info des potions []
    fleches = []            # listes des flèches tirées : (direction, coo_x, coo_y, images)
    monstres = []           # liste qui contient les monstres : (direction : 0=gauche 1=droite, coo_x, coo_y, images, booleen True=agro False=pas agro, booleen True=vie False=mort)
    boss = []               # liste qui contient les info du boss : [x, y, direction("gauche" ou "droite"), action("passif", "marche", "atk" ou "mort"), booleen(True=agro False=pas agro), booleen(True=vie False=mort), images]
    boss_frost = []         # liste qui contient les info di boss des neiges : [x, y, direction("gauche" ou "droite"), action("passif", "marche", "atk" ou "mort"), booleen(True=agro False=pas agro), booleen(True=vie False=mort), images]
    cupidon = [largeur//2, hauteur//2, 'gauche', 'passif']    # liste contenant les infos de cupidon : [x, y, direction("gauche" ou "droite"), action("passif", "tir" ou "mort"), image]
    cupidon_img=toile.create_image(cupidon[0], cupidon[1], image =images_cupidon[0])

# ----------------------------- lancement des fonctions -----------------------------------
    menu()
    monstre_animation(0)
    is_agro()
    killing_monster()
    battement_daile(0)  # animation de cupidon
    killing_arrow()
    avancer_fleche()
    fenetre.bind('<Key>', pression_touche)
    fenetre.mainloop()  # permet à la fenêtre "d'écouter" les évènements en boucle

# ------------------------------------------BUG------------------------------------------

# les lucioles quand on change de monde : ne disparaissent pas et la fonction se relance a chaque fois (trop de lucioles + trop vite)
# hitboxes des boss

# __________________________________credits____________________________________
# boss de chierit https://chierit.itch.io/
# GUI de nectanebo https://nectanebo.itch.io/
# menu sign + monde2 bg de mmkhlv https://mmkhlv.itch.io/
# DEV : jean + Isidore

# -------------------------------idees---------------------------------------

# cinematique pour rajouter du LORE
# transitions entre les mondes : portail à la mort du premier boss pk pas
# potions temporaires / particles