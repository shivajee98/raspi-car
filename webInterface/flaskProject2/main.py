import time
from flask import Flask, render_template
import RPi.GPIO as GPIO

# Setup Flask app
app = Flask(__name__)

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for L298N
ENA = 18
IN1 = 6
IN2 = 25
ENB = 23
IN3 = 17
IN4 = 27

# Setup GPIO pins for L298N
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.LOW)

# Setup PWM for speed control
pwm_a = GPIO.PWM(ENA, 1000)  # Initialize PWM on ENA with 1kHz frequency
pwm_b = GPIO.PWM(ENB, 1000)  # Initialize PWM on ENB with 1kHz frequency

pwm_a.start(0)  # Start PWM with 0% duty cycle
pwm_b.start(0)  # Start PWM with 0% duty cycle

# Speed level global variable
speed_level = 0

def debug_state():
    state = {
        'IN1': GPIO.input(IN1),
        'IN2': GPIO.input(IN2),
        'IN3': GPIO.input(IN3),
        'IN4': GPIO.input(IN4),
        'ENA': GPIO.input(ENA),
        'ENB': GPIO.input(ENB),
    }
    print(f"Current GPIO State: {state}")

def set_speed(level):
    global speed_level
    speed_level = level
    duty_cycle = level * 25  # Map speed level (1-4) to duty cycle (25%, 50%, 75%, 100%)
    pwm_a.ChangeDutyCycle(duty_cycle)
    pwm_b.ChangeDutyCycle(duty_cycle)
    print(f"Speed set to level {level} with duty cycle {duty_cycle}%")
    debug_state()

def forward(in1, in2, in3, in4):
    print("Executing forward")
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    debug_state()

def backward(in1, in2, in3, in4):
    print("Executing backward")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    debug_state()

def left(in1, in2, in3, in4):
    print("Executing left")
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    debug_state()

def right(in1, in2, in3, in4):
    print("Executing right")
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    debug_state()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_command/<direction>')
def send_command(direction):
    if direction == 'F':  # Forward
        print('F')
        forward(IN1, IN2, IN3, IN4)
    elif direction == 'B':  # Backward
        backward(IN1, IN2, IN3, IN4)
    elif direction == 'L':  # Left
        left(IN1, IN2, IN3, IN4)
    elif direction == 'R':  # Right
        right(IN1, IN2, IN3, IN4)
    elif direction == 'S':  # Stop
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
        print("Executing stop")
        debug_state()
    elif direction == '1':  # Speed Level 1
        set_speed(1)
    elif direction == '2':  # Speed Level 2
        set_speed(2)
    elif direction == '3':  # Speed Level 3
        set_speed(3)
    elif direction == '4':  # Speed Level 4
        set_speed(4)
    return f'Sent command: {direction}'

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80)
    finally:
        pwm_a.stop()  # Stop PWM
        pwm_b.stop()  # Stop PWM
        GPIO.cleanup()
