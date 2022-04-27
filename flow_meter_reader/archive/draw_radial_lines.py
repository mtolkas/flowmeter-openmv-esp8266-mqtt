# Line Drawing
#
# This example shows off drawing lines on the OpenMV Cam.

import sensor, image, time, pyb, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # or GRAYSCALE...
sensor.set_framesize(sensor.VGA) # or QQVGA...
sensor.skip_frames(time = 2000)
clock = time.clock()

x0 = 384
y0 = 279
radius = 100
ROI_CIRCLE = (360, 258,66, 41) 
ROI = (266, 151,245, 257) 
min_degree = 0
max_degree = 179

#degrees = range(360)
#x = cos(degrees) * radius + x0
#y = sin(degrees) * radius + y0


while(True):
    clock.tick()

    #img = sensor.snapshot()
    img = sensor.snapshot().gamma_corr(gamma = 0.5, contrast = 6.0, brightness = 0.0)
    img.laplacian(2, sharpen=True)

    center = None

    for c in img.find_circles(ROI_CIRCLE, threshold = 3000, x_margin = 10, y_margin = 10, r_margin = 10, r_min = 2, r_max = 100, r_step = 2):
        img.draw_circle(c.x(), c.y(), c.r(), color = (255, 250, 250))
    
        #img.draw_line(x0, y0, x, y, color = (255, 1, 1), thickness =1)
    
         
        # Axes
        img.draw_line(c.x(), c.y(), c.x(), 130, color = (255, 0, 0), thickness =1) # Top
        img.draw_line(c.x(), c.y(), c.x(), 430, color = (0, 0, 255), thickness =1) # Bottom
        img.draw_line(c.x(), c.y(), 240, c.y(), color = (0, 255, 0), thickness =1) # Left
        img.draw_line(c.x(), c.y(), 501, c.y(), color = (255, 0, 255), thickness =1) # Right        

        # Draw radial lines
        for i in range(0, 360, 5):
            x = int(round((math.cos(i) * radius) + x0))
            y = int(round((math.sin(i) * radius) + y0))
            img.draw_line(c.x(), c.y(), x, y, color = (255, 1, 1), thickness =1)
        #print("i: " + str(int(i)))


        #print("x: " + str(int(x))+" | y: " + str(int(y)))

        #x0 = 384
        #y0 = 279
        #x1 = (pyb.rng() % (2*img.width())) - (img.width()//2)
        #y1 = (pyb.rng() % (2*img.height())) - (img.height()//2)

        # If the first argument is a scaler then this method expects
        # to see x0, y0, x1, and y1. Otherwise, it expects a (x0,y0,x1,y1) tuple.
        #img.draw_line(x0, y0, x0, 130, color = (255, 0, 0), thickness =1) # Top
        #img.draw_line(x0, y0, x0, 430, color = (0, 0, 255), thickness =1) # Bottom
        #img.draw_line(x0, y0, 240, y0, color = (0, 255, 0), thickness =1) # Left
        #img.draw_line(x0, y0, 501, y0, color = (255, 0, 0), thickness =1)
        #img.draw_line(x0, y0, x, y, color = (255, 1, 1), thickness =1)
  

        ## Angle between the white and one that is 90 degrees
        #dy = y - y0
        #print("dy:" + str(int(dy)))
        #dx = x - x0
        #print("dx:" + str(int(dx)))
        #th = math.atan2(dy, dx)
        #th *= 180/math.pi
        #print("th:" + str(int(th)))
        #if ((90- th) < 90):
        #img.draw_line(x0, y0, x, y, color = (255, 1, 1), thickness =1)
        #time.sleep_ms(100)

        #for l in img.find_lines(ROI, threshold = 2500, theta_margin = 25, rho_margin = 25):
            #if (min_degree <= l.theta()) and (l.theta() <= max_degree):
                #img.draw_line(l.line(), color = (255, 0, 0))
                #dy = l.y2() - l.y1()
                #dx = l.x2() - l.x1()
                #th = math.atan2(dy, dx)
                #th *= 180/math.pi
                #print(l)
                #print(th)
        
        #for l in img.find_line_segments(ROI, merge_distance = 35, max_theta_diff = 5):         
             #if (l.length() > 100):
                #img.draw_line(l.line(), color = (255, 150, 150))
                #print(l.length())
                #print(l)

    #time.sleep_ms(1000)

    #print(clock.fps())
