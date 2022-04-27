# Find Line Segments Example
#
# This example shows off how to find line segments in the image. For each line object
# found in the image a line object is returned which includes the line's rotation.

# find_line_segments() finds finite length lines (but is slow).
# Use find_line_segments() to find non-infinite lines (and is fast).

enable_lens_corr = False # turn on for straighter lines...

import sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE) # grayscale is faster
sensor.set_framesize(sensor.VGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

# All lines also have `x1()`, `y1()`, `x2()`, and `y2()` methods to get their end-points
# and a `line()` method to get all the above as one 4 value tuple for `draw_line()`.

ROI = (273, 149, 233, 255)

ROI_CIRCLE = (355, 261,63, 41) 
ROI_CIRCLE_LARGE = (257, 145,255, 265) 

# Lines
min_degree = 0
max_degree = 179


while(True):
    clock.tick()
    img = sensor.snapshot().gamma_corr(gamma = 0.5, contrast = 6.0, brightness = 0.0)
    img.laplacian(2, sharpen=True)
   
    #if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...

    # `merge_distance` controls the merging of nearby lines. At 0 (the default), no
    # merging is done. At 1, any line 1 pixel away from another is merged... and so
    # on as you increase this value. You may wish to merge lines as line segment
    # detection produces a lot of line segment results.

    # `max_theta_diff` controls the maximum amount of rotation difference between
    # any two lines about to be merged. The default setting allows for 15 degrees.

    #Find line segments
    #for l in img.find_line_segments(ROI, merge_distance = 35, max_theta_diff = 5):         
         #if (l.length() > 100):
            #img.draw_line(l.line(), color = (255, 150, 150))
            #print(l.length())
            #print(l)

    # Draw axes
    img.draw_line(x0, y0, x0, 100, color = (255, 255, 255), thickness =1)
    
    
    ## Fine lines
    for l in img.find_lines(ROI, threshold = 2500, theta_margin = 25, rho_margin = 25):
        if (min_degree <= l.theta()) and (l.theta() <= max_degree):
            img.draw_line(l.line(), color = (255, 0, 0))
            dy = l.y2() - l.y1()
            dx = l.x2() - l.x1()
            th = math.atan2(dy, dx)
            th *= 180/math.pi
            print(l)
            print(th)

    
    # Find circles
    for c in img.find_circles(ROI_CIRCLE, threshold = 3000, x_margin = 10, y_margin = 10, r_margin = 10,
            r_min = 2, r_max = 100, r_step = 2):
        img.draw_circle(c.x(), c.y(), c.r(), color = (255, 250, 250))
        print(c)        


    for i in range(0, 360, 3):
        x = int(round(math.cos(i) * radius + x0))
        y = int(round(math.sin(i) * radius + y0))

        #x0 = 384
        #y0 = 279
        #x1 = (pyb.rng() % (2*img.width())) - (img.width()//2)
        #y1 = (pyb.rng() % (2*img.height())) - (img.height()//2)
        r = (pyb.rng() % 127) + 128
        g = (pyb.rng() % 127) + 128
        b = (pyb.rng() % 127) + 128

        # If the first argument is a scaler then this method expects
        # to see x0, y0, x1, and y1. Otherwise, it expects a (x0,y0,x1,y1) tuple.
        img.draw_line(x0, y0, x, y, color = (255, 1, 1), thickness =1)


    print("FPS %f" % clock.fps())
