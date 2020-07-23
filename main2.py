import Motor
import time

# Wykorzystanie biblioteki Motor

# Nowy obiekt typu motor. Parametry konstruktora (PortCOM, ilość kroków na pełny obrót, pin kierunku w Arduino,
# pin kroku, pin low alert, pin hgh alert, min delay = 2000 (parametr opcjonalny)
motor1 = Motor.Motor('COM8', 800, 10, 11, 2, 3)

# Test asynchronicznej funkcji obrotu silnikiem
motor1.moveLeftRev(2.5, 2000)

# Jakieś zadanie z równoczesnym monitorowaniem zmiennej isRuninng obiektu motor
for i in range(0, 50):
    time.sleep(0.1)
    print("Wywolanie f. no. " + str(i) + " Running status: " + str(motor1.isRunning))

# Dostepne metody:
# moveLeftRev(ilosc obrotów, opoznienie pomiedzy krokami)
motor1.moveLeftRev(10, 2000)
time.sleep(0.5)
motor1.moveRightRev(9, 2000)
motor1.moveLeftSteps(800, 2000)

time.sleep(10)
# Jeśli silnik nie pracuje, zakreś w prawo o 842 kroki, opóznienie 5000. Im większe opźnienie, tym wolniej się kręci
if not motor1.isRunning: motor1.moveRightSteps(842, 5000)


