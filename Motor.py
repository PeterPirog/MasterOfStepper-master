# Moduł silnika
import pyfirmata2
import multitasking
import time
import random
import signal


class Motor:
    def __init__(self, port, steps_per_rev, dir_pin, step_pin, low_alert_pin, high_alert_pin, min_delay=2000, ):
        self.stepsPerRevolution = steps_per_rev
        self.minDelay = min_delay
        self.isRunning: bool = False

        try:
            self.board = pyfirmata2.Arduino(port, baudrate=115200)
        except:
            print('Błąd otwarcia portu Arduino')
        else:
            # Konfiguracja Arduino
            self.tempString = 'd:' + str(step_pin) + ':o'
            self.stepPin = self.board.get_pin('d:' + str(step_pin) + ':o')
            self.tempString = str('d:' + str(dir_pin) + ':o')
            self.dirPin = self.board.get_pin(self.tempString)
            self.tempString = str('d:' + str(low_alert_pin) + ':i')
            self.lowAlertPin = self.board.get_pin(self.tempString)
            self.tempString = str('d:' + str(high_alert_pin) + ':i')
            self.highAlertPin = self.board.get_pin(self.tempString)

            self.it = pyfirmata2.Iterator(self.board)
            self.it.start()

            print('Board init OK')

    def is_alert(self):
        if self.is_high_alert() or self.is_low_alert():
            return 1
        else:
            return 0

    def is_high_alert(self):
        if self.highAlertPin.read():
            return 1
        else:
            return 0

    def is_low_alert(self):
        if self.lowAlertPin.read():
            return 1
        else:
            return 0

    def is_running(self):
        if self.isRunning:
            return 1
        else:
            return 0

    def calculate_steps2deg(self, step):
        return 360 * step / self.stepsPerRevolution

    def calculate_steps2rotations(self, step):
        return step / self.stepsPerRevolution

    def moveRightSteps(self, steps, delay):
        if self.is_high_alert():
            print("High Alert - Nie można kręcić w prawo!")
        elif self.isRunning:
            print("SILNIK NIE ZAKONCZYL POPRZEDNIEJ KOMENDY! Nie wykonano: moveRightSteps " + str(steps))
        else:
            self.dirPin.write(1)
            self.motorMove(steps, self.is_high_alert, delay)

    def moveLeftSteps(self, steps, delay):
        if self.is_low_alert():
            print("Low Alert - Nie można kręcić w lewo!")
        elif self.isRunning:
            print("SILNIK NIE ZAKONCZYL POPRZEDNIEJ KOMENDY! Nie wykonano: moveLeftSteps " + str(steps))
        else:
            self.dirPin.write(0)
            self.motorMove(steps, self.is_low_alert, delay)

    def moveRightRev(self, revolutions, delay):
        if self.is_high_alert():
            print("High Alert - Nie można kręcić w prawo!")
        elif self.isRunning:
            print("SILNIK NIE ZAKONCZYL POPRZEDNIEJ KOMENDY! Nie wykonano: moveRightRev " + str(revolutions))
        else:
            self.dirPin.write(1)
            self.motorMove(revolutions * self.stepsPerRevolution, self.is_high_alert, delay)

    def moveLeftRev(self, revolutions, delay):
        if self.is_low_alert():
            print("Low Alert - Nie można kręcić w lewo!")
        elif self.isRunning:
            print("SILNIK NIE ZAKONCZYL POPRZEDNIEJ KOMENDY! Nie wykonano: moveLeftRev " + str(revolutions))
        else:
            self.dirPin.write(0)
            self.motorMove(revolutions * self.stepsPerRevolution, self.is_low_alert, delay)

    @multitasking.task
    def motorMove(self, steps, break_function, delay=2000):
        self.isRunning = True
        print("Wykonuje: " + str(steps)+" steps")
        for i in range(0, steps):
            #print(".")
            if not break_function():
                self.stepPin.write(1)
                for j in range(0, delay):
                    pass
                # time.sleep(1 / 1000000)

                self.stepPin.write(0)
                for j in range(0, delay):
                    pass
            else:
                print("ALERT at " + str(i) + " step.")
                break
        self.isRunning = False
        print("OVER")
# time.sleep(10 / 1000000)
