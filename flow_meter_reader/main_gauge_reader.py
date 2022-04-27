import sensor, image, time, math, rpc

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # RGB565 or GRAYSCALE...
sensor.set_framesize(sensor.VGA) # or QQVGA...
sensor.skip_frames(time = 2000)
clock = time.clock()

##################################
# Application-specific constants #
##################################

# ROI for the frame (corner to corner of the flow meter's screen)
ROI_FRAME = (157, 100, 330, 346)

# ROI for detecting the circle. Select one that is enough for the circle only to avoid false positives
ROI_GAUGE_CENTER = (283, 250, 67, 50)

GAMMA = 0.4

# Rotation correction only. For detailed calibration perform perspective correction using the file with the same name.
Z_ROTATION_DEGREES = 1.5

# Only return needle-tracing lines of this range of length
LINE_MIN = 125
LINE_MAX = 200



# The [x,y] of the center around which the needle spins
CENTER_X = None
CENTER_Y = None

def points_distance(x1, y1,x2, y2):
    return math.sqrt( ( (x1-x2)**2) + ((y1-y2)**2) )

# Printing helper. Input is a line
def print_line_points(l):
    print("Line points")
    print("[x1, y1]: [" + str(l.x1()) + ", " + str(l.y1()) + "]")
    print("[x2, y2]: [" + str(l.x2()) + ", " + str(l.y2()) + "]")
    print("Length: " + str(l.length()))
    print(l)

# Gets the angle between two lines via the arctangent
def arctangent(x1, y1, x2, y2):
    dy =  y1 -y2 # Here we do y1 - y2 because the coordinate system starts from top-left (common in computer graphics) and not in a cartesian system
    #print("dy:" + str(int(dy)))
    dx = x2 - x1
    th = math.atan2(dy, dx)
    th *= 180/math.pi
    th_90 = 90 - int(th) #Rotate by 90 counter clockwise so top of flow meter corresponds to 0 degrees for convenience
    th_final = th_90 if th_90 > 0 else (360 + th_90) # if th_90 is negative subtract from 360 to compensate for
    #print("final angle:" + str(th_final))
    return th_final

# Multiplier to map the gauge's output to 0-360 degrees angle
def angle_output_mapping(angle):
    factor = 0.0277
    return angle * factor

while(True):
    clock.tick()
    img = sensor.snapshot()

    # Preprocess image for gamma and contrast correction, as well as sharpness
    img.gamma_corr(gamma = GAMMA, contrast = 3, brightness = 0.0)
    img.laplacian(2, sharpen=True)

    # Rotate the image. Get the angle via april tag or trial and error. This rotate the image in-place counter-clockwise
    img.rotation_corr(z_rotation = Z_ROTATION_DEGREES )

    # Find center around which the needle rotate. We do this by taking advantange of the circle on the needle.
    # Parameters such as threshold etc. made sense while developing the prototype. This is application- and environment-specific so will need adjustment.
    for c in img.find_circles(ROI_GAUGE_CENTER, threshold = 3900, x_margin = 10, y_margin = 10, r_margin = 10, r_min = 2, r_max = 100, r_step = 2):
        img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))
        CENTER_X = c.x()
        CENTER_Y = c.y()
        #print("Center point: [" + str(CENTER_X) + ", " + str(CENTER_Y) + "]")

        # Draw axes using the center for convenience. Static numbers used arbitrarily for visual convenience.
        #img.draw_line(c.x(), c.y(), c.x(), 130, color = (255, 0, 0), thickness =1) # Top
        #img.draw_line(c.x(), c.y(), c.x(), 430, color = (0, 0, 255), thickness =1) # Bottom
        #img.draw_line(c.x(), c.y(), 240, c.y(), color = (0, 255, 0), thickness =1) # Left
        #img.draw_line(c.x(), c.y(), 501, c.y(), color = (255, 0, 255), thickness =1) # Right

        # Find needle lines segment. # Only care for lines that are long enough to correspond to the needle. Smaller ones might be just number labels and are irrelevant. This is resolution dependent.
        # Parameters such as merge_distance etc. made sense while developing the prototype. This is application- and environment-specific so will need adjustment.
        large_lines = [li for li in img.find_line_segments(ROI_FRAME, merge_distance = 35, max_theta_diff = 5)
            if (li.length() > LINE_MIN and li.length() < LINE_MAX)]

        for l in large_lines:
            # For each [x, y] of the line detected, plot a line with the center point and get its length.
            # The longer one should be where the needle is pointing because the bottom part is significantly shorter.

            # Line arrow for center and x1y1
            center_line1_distance = points_distance(CENTER_X, CENTER_Y, l.x1(), l.y1())
            #img.draw_arrow(CENTER_X, CENTER_Y, l.x1(), l.y1(), color = (255, 0, 0), thickness =1)
            #print("center_line1_distance: " + str(center_line1_distance))

            # Line arrow for center and x2y2
            center_line2_distance = points_distance(CENTER_X, CENTER_Y, l.x2(), l.y2())
            #img.draw_arrow(CENTER_X, CENTER_Y, l.x2(), l.y2(), color = (0, 0, 255), thickness =1)
            #print("center_line2_distance: " + str(center_line2_distance))

            # Define the needle line and direction by chosing the line segment with the longest distance from the center
            needle_point = None
            if (center_line1_distance > center_line2_distance):
                needle_point = [l.x1(), l.y1()]
            else:
                needle_point = [l.x2(), l.y2()]

            # Draw the arrow line of the line segment that corresponds to the needle
            img.draw_arrow(CENTER_X, CENTER_Y, needle_point[0], needle_point[1], color = (255, 0, 0), thickness =1)

            # Get the angle between the needle line and the center-top axes.
            # Note that we are rotating the coordination system by 90 degrees counter-clockwise so that output = 0 corresponds to angle = 0 for convenience.
            angle = arctangent(CENTER_X, CENTER_Y, needle_point[0], needle_point[1])

            # Map angle to output
            output = angle_output_mapping(angle)

            # Show angle and output on the framebuffer
            img.draw_string(140, 0, "Angle: " + str(angle), scale=2, color=(255,0,0) ,mono_space = False)
            img.draw_string(140, 25, "Output: " + str(output), scale=2, color=(255,0,0) ,mono_space = False)
            print("Output:" + str(output))

    print(clock.fps())
