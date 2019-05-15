import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    edges=[]
    polygons=[]
    
    print symbols
    for command in commands:
        print command
        
        op = command['op']
        args = command['args']
        
        if op=='push':
            stack.append([x[:] for x in stack[-1]])
            
        if op=='pop':
            stack.pop()
            
        if op=='move':
            t=make_translate(float(args[0]),float(args[1]),float(args[2]))
            matrix_mult(stack[-1],t)
            stack[-1]=[x[:] for x in t]

        if op=='rotate':
            theta = float(args[1]) * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(stack[-1], t)
            stack[-1] = [x[:] for x in t]

        if op=='scale':
            t=make_scale(float(args[0]),float(args[1]),float(args[2]))
            matrix_mult(stack[-1],t)
            stack[-1]=[x[:] for x in t]

        if op=='box':
            add_box(polygons,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(stack[-1], polygons)
            if command['constants']:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []
            
        if op=='sphere':
            add_sphere(polygons,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult(stack[-1], polygons)
            if command['constants']:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []


        if op=='torus':
            add_torus(polygons,
                          float(args[0]), float(args[1]), float(args[2]),
                          float(args[3]), float(args[4]), step_3d)
            matrix_mult(stack[-1], polygons)
            if command['constants']:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []

            
        if op=='line':
            add_edge( edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult(stack[-1], edges)
            draw_lines(edges, screen, zbuffer, color)
            edges = []

        if op=='save':
            save_extension(screen, args[0] + ".png")

        if op=='display':
            display(screen)
