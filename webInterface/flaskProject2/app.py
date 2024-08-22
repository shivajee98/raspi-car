from flask import Flask, render_template
import RPi.GPIO as GPIO
import time
import threading

# Setup Flask app
app = Flask(__name__)

# GPIO setup
GPIO.setwarnings(False)  # Disable warnings
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


# Enable pins as PWM
pwmA = GPIO.PWM(ENA, 100)
pwmB = GPIO.PWM(ENB, 100)
pwmA.start(25)
pwmB.start(25)

def forward(in1, in2, in3, in4, pwmA, pwmB, speed):
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)


def backward(in1, in2, in3, in4, pwmA, pwmB, speed):
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

def left(in1, in2, in3, in4, pwmA, pwmB, speed):
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

def right(in1, in2, in3, in4, pwmA, pwmB, speed):
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

@app.route('/')
def index():
     return render_template('index.html')

@app.route('/send_command/<direction>')
def send_command(direction):
    if direction == 'F':  # Forward
        forward(IN1, IN2, IN3, IN4, pwmA, pwmB, 100)
    elif direction == 'B':  # Backward
        backward(IN1, IN2, IN3, IN4, pwmA, pwmB, 100)
    elif direction == 'L':  # Left
        left(IN1, IN2, IN3, IN4, pwmA, pwmB, 100)
    elif direction == 'R':  # Right
        right(IN1, IN2, IN3, IN4, pwmA, pwmB, 100)
    elif direction == 'S':  # Stop
        pwmA.ChangeDutyCycle(0)
        pwmB.ChangeDutyCycle(0)
    elif direction == 'W':  # Stop from Radar
        pwmA.ChangeDutyCycle(0)
        pwmB.ChangeDutyCycle(0)
    return f'Sent command: {direction}'

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80)
    finally:
        pwmA.stop()
        pwmB.stop()
        GPIO.cleanup()
