import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.VGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

# The image will be warped such that the following points become the new:
#
#   (0,   0)
#   (w-1, 0)
#   (w-1, h-1)
#   (0,   h-1)
#
# Try setting the points below to the corners of a quadrilateral
# (in clock-wise order) in the field-of-view. You can get points
# on the image by clicking and dragging on the frame buffer and
# recording the values shown in the histogram widget.

w = sensor.width()
h = sensor.height()

TARGET_POINTS = [(0,   0),   # (x, y) CHANGE ME!
                 (w-200, 75),   # (x, y) CHANGE ME!
                 (w-100, h+90), # (x, y) CHANGE ME!
                 (40,   h-20)] # (x, y) CHANGE ME!

# Degrees per frame to rotate by...
X_ROTATION_DEGREE_RATE = 5
Y_ROTATION_DEGREE_RATE = 0.5
Z_ROTATION_DEGREE_RATE = 0
X_OFFSET = 0
Y_OFFSET = 0

ZOOM_AMOUNT = 1 # Lower zooms out - Higher zooms in.
FOV_WINDOW = 25 # Between 0 and 180. Represents the field-of-view of the scene
                # window when rotating the image in 3D space. When closer to
                # zero results in lines becoming straighter as the window
                # moves away from the image being rotated in 3D space. A large
                # value moves the window closer to the image in 3D space which
                # results in the more perspective distortion and sometimes
                # the image in 3D intersecting the scene window.

z_rotation_counter = 1.5 # Get this using the apriltag 

while(True):
    clock.tick()

    img = sensor.snapshot().rotation_corr(z_rotation = z_rotation_counter, corners = TARGET_POINTS)

    print(clock.fps())
