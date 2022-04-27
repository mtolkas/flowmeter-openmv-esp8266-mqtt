import sensor, image, time, math, rpc

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE) # RGB565 or GRAYSCALE...
sensor.set_framesize(sensor.VGA) # or QQVGA...
sensor.skip_frames(time = 2000)

interface = rpc.rpc_uart_slave(baudrate=115200)

# ROI for the frame (corner to corner of the flow meter's screen)
ROI_FRAME = (157, 100, 330, 346)

# ROI for detecting the circle. Select one that is enough for the circle only to avoid false positives
ROI_GAUGE_CENTER = (283, 250, 67, 50)

GAMMA = 0.4

# Rotation correction only. For detailed calibration perform perspective correction using the file with the same name.
Z_ROTATION_DEGREES = 1.5

# Only return needle-tracing lines of this range of length
LINE_MIN = 130
LINE_MAX = 220


def points_distance(x1, y1,x2, y2):
    return math.sqrt( ( (x1-x2)**2) + ((y1-y2)**2) )

# Gets the angle between two lines via the arctangent
def arctangent(x1, y1, x2, y2):
    dy =  y1 -y2 # Here we do y1 - y2 because the coordinate system starts from top-left (common in computer graphics) and not in a cartesian system
    #print("dy:" + str(int(dy)))
    dx = x2 - x1
    th = math.atan2(dy, dx)
    th *= 180/math.pi
    th_90 = 90 - int(th) #Rotate by 90 counter clockwise so top of flow meter corresponds to 0 degrees for convenience
    th_final = th_90 if th_90 > 0 else (360 + th_90) # if th_90 is negative subtract from 360 to compensate for
    return th_final

# Multiplier to map the gauge's output to 0-360 degrees angle
def angle_output_mapping(angle):
    factor = 0.0277
    return angle * factor

def get_gauge_center(img):
    circles = img.find_circles(ROI_GAUGE_CENTER, threshold = 3000, x_margin = 10, y_margin = 10, r_margin = 10, r_min = 2, r_max = 100, r_step = 2)
    center = max(circles, key = lambda c: c.r()) if circles else None
    #img.draw_circle(center.x(), center.y(), center.r(), color = (255, 250, 250))
    return None if not center else center

def get_needle_pointer(img):
    lines_segments = img.find_line_segments(ROI_FRAME, merge_distance = 35, max_theta_diff = 5)
    useful_lines = [i for i in lines_segments if (i.length() > LINE_MIN and i.length() < LINE_MAX)]
    return useful_lines[0] if useful_lines else None

def get_snapshop():
    img = sensor.snapshot()
    img.rotation_corr(z_rotation = Z_ROTATION_DEGREES )
    img.gamma_corr(gamma = GAMMA, contrast = 3.0, brightness = 0.0)
    img.laplacian(2, sharpen=True)
    return img

def flow_meter_read(data):
    img = get_snapshop()

    center = get_gauge_center(img)
    if center is None: return bytes()

    needle_line = get_needle_pointer(img)
    if needle_line is None: return bytes()

    center_line1_distance = points_distance(center.x(), center.y(), needle_line.x1(), needle_line.y1())
    center_line2_distance = points_distance(center.x(), center.y(), needle_line.x2(), needle_line.y2())

    needle_point = None
    if (center_line1_distance > center_line2_distance):
        needle_point = [needle_line.x1(), needle_line.y1()]
    else:
        needle_point = [needle_line.x2(), needle_line.y2()]

    angle = arctangent(center.x(), center.y(), needle_point[0], needle_point[1])

    output = angle_output_mapping(angle)

    print('output \n')
    print(output)

    if not output: return bytes()
    return str(output).encode()

interface.register_callback(flow_meter_read)
interface.loop()
