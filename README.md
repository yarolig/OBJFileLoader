# OBJFileLoader

A library from pygame wiki https://www.pygame.org/wiki/OBJFileLoader


# How to use it with pygame and old OpenGL

Right now this library requires pygame, PyOpenGL and OpenGL compatibility profile (or OpenGL 2.0).

Copy OBJFileLoader into your project.

Import it:

    from OBJFileLoader import OBJ

After you initialise pygame and PyOpenGL you can load objects.

    box = OBJ('path/to/box.obj')
    
Material and texture files should be inside 'path/to' directory.
    
To draw the object position it where you want and call render().

    glPushMatrix()
    glTranslatef(box_x, box_y, box_z)
    box.render()
    glPopMatrix()
   
If you need to change behavior of texture loading or use VBO instead of lists create a subclass and override loadTexture() or generate().

# Viewer

To view an OBJ-file run:

    python OBJFileLoader/objviewer.py path/to/model.obj
