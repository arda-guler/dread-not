import numpy as np
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import time
import keyboard as kbd
from screeninfo import get_monitors
import ctypes
import random
import mouse

from scenery_objects import *
from terrain import *
from ship import *
from cannon import *
from graphics import *
from wavefront import *
from camera import *
from sound import *

def hide_cursor():
    ctypes.windll.user32.ShowCursor(False)

def show_cursor():
    ctypes.windll.user32.ShowCursor(True)

def main():
    def window_resize(window, width, height):
        try:
            # glfw.get_framebuffer_size(window)
            glViewport(0, 0, width, height)
            glLoadIdentity()
            gluPerspective(fov, width/height, near_clip, far_clip)
            glRotatef(np.rad2deg(main_cam.yaw), 0, 1, 0)
            glRotatef(-np.rad2deg(main_cam.pitch), np.cos(main_cam.yaw), 0, np.sin(main_cam.yaw))
            glTranslate(main_cam.pos[0], main_cam.pos[1], main_cam.pos[2])
            #player.orient = np.eye(3)
        except ZeroDivisionError:
            # if the window is minimized it makes height = 0, but we don't need to update projection in that case anyway
            pass

    # SCENE SETUP

    # terrain
    terrain_model = Wavefront3D("terrain", "soil")
    terrain = SceneryObject(terrain_model, np.array([0, 0, 0]))

    water_model = Wavefront3D("water", "water")
    water = SceneryObject(water_model, np.array([0, 0, 0]))

    scenery_objects = [terrain, water]

    # initial ships
    ship_model = Wavefront3D("ship", "gray")
    ship1 = Ship(ship_model, np.array([0,    0, 11.5e3]), np.array([0, 0, -8]))
    ship2 = Ship(ship_model, np.array([150,  0, 12.5e3]), np.array([0, 0, -8]))
    ship3 = Ship(ship_model, np.array([-150, 0, 12.5e3]), np.array([0, 0, -8]))
    ships = [ship1, ship2, ship3]

    # player cannon
    cannon_base_model = Wavefront3D("cannon_base", "gray")
    cannon_barrel_model = Wavefront3D("cannon_barrel", "green")
    cannon = Cannon(np.array([6300, 563.75, -4000]), cannon_base_model, cannon_barrel_model,
                     700, 150 - 143, [np.deg2rad(-4), np.deg2rad(30)])
    cannon.rotate(-np.deg2rad(90) * 10, 0)

    # cannon shells
    shells = []

    # ship smoke clouds
    smokes = []

    # shell splash animations
    splash_model = Wavefront3D("splash", "splash")
    splashes = []

    # SOUND
    print("Intializing sound (pygame.mixer)...")
    init_sound()
    play_bgm("industrial_revolution")

    # GRAPHICS
    print("Initializing graphics (OpenGL, glfw)...")
    window_x, window_y = 1600, 900
    fov = 60
    near_clip = 0.1
    far_clip = 10e6
    
    glfw.init()
    window = glfw.create_window(window_x, window_y, "Dread Not", None, None)
    glfw.set_window_pos(window, 100, 100)
    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)

    gluPerspective(fov, window_x/window_y, near_clip, far_clip)
    glClearColor(0.2, 0.3, 0.6, 1)

    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_POINT_SMOOTH)

    for o in ships:
        if o.model.texture_path:
            o.texture_id = loadTexture(o.model.texture_path)

    for o in scenery_objects:
        if o.model.texture_path:
            o.texture_id = loadTexture(o.model.texture_path)
            
    cannon.base_texture_id   = loadTexture(cannon.model_base.texture_path)
    cannon.barrel_texture_id = loadTexture(cannon.model_barrel.texture_path)

    splash_texture_id = loadTexture(splash_model.texture_path)

    # camera
    cam_pos = np.array([-10e3, -3500, -3e3-15])
    cam_orient = np.array([[1, 0, 0],
                           [0, 1, 0],
                           [0, 0, 1]])
    main_cam = Camera("main_cam", cam_pos, cam_orient, True)
    main_cam.lock_to_target(cannon)
    main_cam.offset_amount = np.array([0, 5, 15])

    zoom = False

    def move_cam(movement):
        main_cam.move(movement)

    def rotate_cam(rotation):
        main_cam.rotate(rotation)

    rotate_cam([0, np.deg2rad(-120), 0])

    monitor = get_monitors()[0]
    screen_x = monitor.width
    screen_y = monitor.height

    # PLAYER CONTROLS SETUP
    key_left = "A"
    key_right = "D"
    key_up = "W"
    key_down = "S"
    key_plus = "R"
    key_minus = "F"
    key_fire = "X"

    key_switch_cam_cannon = "Y"
    key_switch_cam_ship = "U"
    key_switch_cam_shell = "O"

    print("Controls:")
    print(key_left, key_right, key_up, key_down, " --> Rotate Battery")
    print(key_plus, key_minus, " --> Load/Unload Propellant Charge")
    print(key_fire, " --> Fire!")
    print(key_switch_cam_cannon, key_switch_cam_ship, key_switch_cam_shell, " --> Cannon, Ship, Shell Camera")
    print("Shift + Mouse to rotate camera.")

    # MAIN LOOP
    dt = 0
    game_running = True
    game_time = 0
    while not glfw.window_should_close(window):
        t_cycle_start = time.perf_counter()
        glfw.poll_events()

        # cannon controls
        d_az = 0
        d_el = 0
        d_charge = 0
        shoot = False

        cannon_is_moving = False
        
        if kbd.is_pressed(key_left):
            d_az -= 1
            cannon_is_moving = True
        elif kbd.is_pressed(key_right):
            d_az += 1
            cannon_is_moving = True
        elif kbd.is_pressed(key_up):
            d_el += 1
            if cannon.el < cannon.limit_el[1]:
                cannon_is_moving = True
        elif kbd.is_pressed(key_down):
            d_el -= 1
            if cannon.el > cannon.limit_el[0]:
                cannon_is_moving = True
        elif kbd.is_pressed(key_plus):
            d_charge = 1
        elif kbd.is_pressed(key_minus):
            d_charge = -1
        elif kbd.is_pressed(key_fire):
            shoot = True

        if kbd.is_pressed(key_switch_cam_ship):
            if len(ships) > 0:
                main_cam.lock_to_target(ships[0])
                main_cam.offset_amount = np.array([0, 15, 300])
                main_cam.yaw_limits = [-80, 2]
                
        elif kbd.is_pressed(key_switch_cam_cannon):
            main_cam.lock_to_target(cannon)
            main_cam.offset_amount = np.array([0, 5, 15])
            main_cam.yaw_limits = [-80, 15]

        elif kbd.is_pressed(key_switch_cam_shell):
            if len(shells):
                main_cam.lock_to_target(shells[0])
                main_cam.offset_amount = np.array([0, 0, 30])
                main_cam.yaw_limits = [-80, 80]

        if cannon_is_moving:
            if not get_channel_busy(2):
                play_sfx("cannon_rotate", -1, 2, 1)
        else:
            if get_channel_busy(2):
                fade_out_channel(2, 300)

        # camera controls
        mouse_sensitivity = 0.3
        if kbd.is_pressed("Shift"):
            m_pos = mouse.get_position()
            rotate_cam([((m_pos[1] - screen_y*0.5) / screen_y) * mouse_sensitivity,
                        ((m_pos[0] - screen_x * 0.5) / screen_x) * mouse_sensitivity,
                        0])
            
            mouse.move(screen_x * 0.5, screen_y * 0.5, True)

        # physics and game mechanics
        if shoot and cannon.load_state >= 1:
            shell_mass = 215
            shell_diam = 240e-3
            shell_pos = cannon.pos + np.array([0, 2.7, 0])
            shell_pos += -cannon.barrel_orient[2] * 9
            shell_vel = -cannon.barrel_orient[2] * 700 * cannon.charges / cannon.max_charges
            shell_Cd = 0.005
            
            new_shell = Shell(shell_mass, shell_diam, shell_pos, shell_vel, shell_Cd)
            shells.append(new_shell)

            play_sfx("cannon_fire", 0, 1, 1)
            
        cannon.update(d_az, d_el, d_charge, shoot, dt)

        for s in shells:
            s.update(dt)

            # todo: check for terrain hits too maybe
            if s.pos[1] <= 0:
                # print(np.linalg.norm(s.pos - cannon.pos))

                ship_hit = False
                
                for ship in ships:
                    if np.linalg.norm(s.pos - ship.pos) < 150: # generous 150 meter hit radius
                        ship.state = 1

                if not ship_hit:
                    new_splash = Splash(np.array([s.pos[0], 0, s.pos[2]]), splash_model)
                    new_splash.texture_id = splash_texture_id
                    splashes.append(new_splash)
                
                shells.remove(s)
                del s

        # new ship generation
        if len(ships) < 3:
            ship_start_pos = np.array([0, 0, 12.5e3])
            rand_x = random.uniform(-500, 500)
            rand_z = random.uniform(-100, 100)
            rand_offset = np.array([rand_x, 0, rand_z])
            ship_init_vel = np.array([0, 0, -8])
            new_ship = Ship(ship_model, ship_start_pos + rand_offset, ship_init_vel)
            new_ship.texture_id = loadTexture(ship.model.texture_path)
            ships.append(new_ship)

        # ship hits mine
        for ship in ships:
            if ship.pos[2] < -150:
                ship.state = 1

        # remove sunk ships
        ships = [ship for ship in ships if ship.pos[1] >= -10]

        # move ships
        for ship in ships:
            if ship.state == 0:
                ship.pos += ship.vel * dt
            else:
                ship.pos += np.array([0, -0.5, 0]) * dt

        # create smoke from ships
        for ship in ships:
            if ship.state == 0:
                if len(ship.smokes) < 3 and game_time - ship.last_smoke_time > 5:
                    new_smoke = ShipSmoke(ship)
                    ship.smokes.append(new_smoke)
                    ship.last_smoke_time = game_time
                    smokes.append(new_smoke)
                    
            else: # create more smoke if sinking
                if len(ship.smokes) < 20 and game_time - ship.last_smoke_time > 1:
                    new_smoke = ShipSmoke(ship)
                    ship.smokes.append(new_smoke)
                    ship.last_smoke_time = game_time
                    smokes.append(new_smoke)

        for smoke in smokes:
            smoke.update(dt)
            if smoke.state > smoke.time_end:
                smoke.ship.smokes.remove(smoke)
                smokes.remove(smoke)
                del smoke
                continue

        # update shell splashes
        for s in splashes:
            s.update(dt)

            if s.state > s.time_end:
                splashes.remove(s)
                del s
                continue

        # bgm
        if not is_music_playing():
            play_random_bgm()
        
        # graphics
        main_cam.move_with_lock(dt)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width, height = glfw.get_framebuffer_size(window)
        if not zoom:
            gluPerspective(fov, width/height, near_clip, far_clip)
        else:
            gluPerspective(fov / 5, width/height, near_clip, far_clip)

        glRotatef(np.rad2deg(main_cam.yaw), 0, 1, 0)
        glRotatef(-np.rad2deg(main_cam.pitch), np.cos(main_cam.yaw), 0, np.sin(main_cam.yaw))
        glTranslate(main_cam.pos[0], main_cam.pos[1], main_cam.pos[2])
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        drawScene(main_cam, cannon, ships, shells, scenery_objects, smokes, splashes, game_time, height)

        glfw.swap_buffers(window)
        dt = time.perf_counter() - t_cycle_start
        game_time += dt

    # POST-GAME
    glfw.destroy_window(window)
    fade_out_bgm()

main()

for i in range(8):
    stop_channel(i)

