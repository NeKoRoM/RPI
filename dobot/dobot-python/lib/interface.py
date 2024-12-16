import serial
import threading
from lib.message import Message

class Interface:
    """
    Klasa Interface do obsługi komunikacji z urządzeniem za pomocą portu szeregowego.

    Atrybuty:
        serial (serial.Serial): Obiekt pySerial do obsługi komunikacji.
        lock (threading.Lock): Blokada do zapewnienia bezpiecznych operacji wątkowych.
    """

    def __init__(self, port):
        """
        Inicjalizuje obiekt Interface z określonym portem szeregowym.

        Args:
            port (str): Nazwa portu szeregowego, do którego ma się podłączyć urządzenie.
        """
        threading.Thread.__init__(self)  # Niepotrzebne, jeśli klasa nie dziedziczy po Thread.
        self.lock = threading.Lock()  # Blokada do synchronizacji dostępu do portu szeregowego.

        # Inicjalizacja połączenia szeregowego.
        self.serial = serial.Serial(
            port=port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

    def send(self, message):
        """
        Wysyła wiadomość do urządzenia i odbiera odpowiedź.

        Args:
            message (Message): Wiadomość do wysłania.

        Returns:
            list: Parametry z odpowiedzi wiadomości.
        """
        self.lock.acquire()  # Blokada na czas operacji wysyłania/odbioru.
        self.serial.write(message.package())  # Wysyłanie zapakowanej wiadomości.
        self.serial.flush()  # Zapewnienie natychmiastowego przesłania danych.
        response = Message.read(self.serial)  # Odczyt odpowiedzi z urządzenia.
        self.lock.release()  # Zwolnienie blokady.
        return response.params

    def connected(self):
        """
        Sprawdza, czy port szeregowy jest otwarty.

        Returns:
            bool: True, jeśli połączenie jest otwarte; False w przeciwnym razie.
        """
        return self.serial.isOpen()

    # Metody dotyczące informacji o urządzeniu
    def get_device_serial_number(self):
        """
        Pobiera numer seryjny urządzenia.

        Returns:
            str: Numer seryjny urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 0, False, False, [], direction='out')
        return self.send(request)

    def set_device_serial_number(self, serial_number):
        """
        Ustawia numer seryjny urządzenia.

        Args:
            serial_number (str): Nowy numer seryjny urządzenia.

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 0, True, False, [serial_number], direction='out')
        return self.send(request)

    def get_device_name(self):
        """
        Pobiera nazwę urządzenia.

        Returns:
            str: Nazwa urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 1, False, False, [], direction='out')
        return self.send(request)

    def set_device_name(self, device_name):
        """
        Ustawia nazwę urządzenia.

        Args:
            device_name (str): Nowa nazwa urządzenia.

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 1, True, False, [device_name], direction='out')
        return self.send(request)

    def get_device_version(self):
        """
        Pobiera wersję urządzenia.

        Returns:
            dict: Informacje o wersji urządzenia (major, minor, revision).
        """
        request = Message([0xAA, 0xAA], 2, 2, False, False, [], direction='out')
        return self.send(request)

    def set_sliding_rail_status(self, enable, version):
        """
        Ustawia status szyny przesuwnej.

        Args:
            enable (bool): True, aby włączyć, False, aby wyłączyć.
            version (int): Wersja szyny przesuwnej.

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 3, True, False, [enable, version], direction='out')
        return self.send(request)

    def get_device_time(self):
        """
        Pobiera czas pracy urządzenia w milisekundach od uruchomienia.

        Returns:
            int: Czas w milisekundach.
        """
        request = Message([0xAA, 0xAA], 2, 4, False, False, [], direction='out')
        return self.send(request)

    def get_device_id(self):
        """
        Pobiera identyfikator urządzenia.

        Returns:
            str: Identyfikator urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 5, False, False, [], direction='out')
        return self.send(request)

    # Metody dotyczące pozycji i orientacji
    def get_pose(self):
        """
        Pobiera aktualną pozycję urządzenia.

        Returns:
            dict: Pozycja i orientacja w przestrzeni (x, y, z, r).
        """
        request = Message([0xAA, 0xAA], 2, 10, False, False, [], direction='out')
        return self.send(request)

    def reset_pose(self, manual, rear_arm_angle, front_arm_angle):
        """
        Resetuje pozycję urządzenia.

        Args:
            manual (bool): Czy resetować ręcznie (True) czy automatycznie (False).
            rear_arm_angle (float): Kąt tylnego ramienia (w trybie manualnym).
            front_arm_angle (float): Kąt przedniego ramienia (w trybie manualnym).

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 11, True, False, [manual, rear_arm_angle, front_arm_angle], direction='out')
        return self.send(request)

    # Obsługa alarmów
    def get_alarms_state(self):
        """
        Pobiera stan alarmów urządzenia.

        Returns:
            list: Lista aktywnych alarmów.
        """
        request = Message([0xAA, 0xAA], 2, 20, False, False, [], direction='out')
        return self.send(request)

    def clear_alarms_state(self):
        """
        Czyści wszystkie stany alarmowe urządzenia.

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 20, True, False, [], direction='out')
        return self.send(request)


    def get_homing_parameters(self):
        """
        Pobiera parametry funkcji homing.

        Returns:
            dict: Parametry homingu, w tym pozycje x, y, z, r.
        """
        request = Message([0xAA, 0xAA], 2, 30, False, False, [], direction='out')
        return self.send(request)

    def set_homing_parameters(self, x, y, z, r, queue=True):
        """
        Ustawia parametry funkcji homing.

        Args:
            x (float): Współrzędna X pozycji homing.
            y (float): Współrzędna Y pozycji homing.
            z (float): Współrzędna Z pozycji homing.
            r (float): Współrzędna R (obrót) pozycji homing.
            queue (bool): Czy dodać komendę do kolejki (domyślnie True).

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 30, True, queue, [x, y, z, r], direction='out')
        return self.send(request)

    def set_homing_command(self, command, queue=True):
        """
        Wysyła polecenie uruchomienia funkcji homing.

        Args:
            command (int): Komenda do wykonania homingu.
            queue (bool): Czy dodać komendę do kolejki (domyślnie True).

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 31, True, queue, [command], direction='out')
        return self.send(request)

    def get_end_effector_params(self):
        """
        Pobiera parametry efektora końcowego.

        Returns:
            dict: Parametry przesunięcia efektora końcowego (bias_x, bias_y, bias_z).
        """
        request = Message([0xAA, 0xAA], 2, 60, False, False, [], direction='out')
        return self.send(request)

    def set_end_effector_params(self, bias_x, bias_y, bias_z):
        """
        Ustawia parametry efektora końcowego.

        Args:
            bias_x (float): Przesunięcie efektora w osi X.
            bias_y (float): Przesunięcie efektora w osi Y.
            bias_z (float): Przesunięcie efektora w osi Z.

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 60, True, False, [bias_x, bias_y, bias_z], direction='out')
        return self.send(request)

    def set_end_effector_laser(self, enable_control, enable_laser, queue=True):
        """
        Włącza lub wyłącza laser efektora końcowego.

        Args:
            enable_control (bool): Czy kontrolować laser (True lub False).
            enable_laser (bool): Czy włączyć laser (True lub False).
            queue (bool): Czy dodać komendę do kolejki (domyślnie True).

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 61, True, queue, [enable_control, enable_laser], direction='out')
        return self.send(request)

    def set_end_effector_suction_cup(self, enable_control, enable_suction, queue=True):
        """
        Włącza lub wyłącza przyssawkę efektora końcowego.

        Args:
            enable_control (bool): Czy kontrolować przyssawkę (True lub False).
            enable_suction (bool): Czy włączyć przyssawkę (True lub False).
            queue (bool): Czy dodać komendę do kolejki (domyślnie True).

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 62, True, queue, [enable_control, enable_suction], direction='out')
        return self.send(request)

    def set_end_effector_gripper(self, enable_control, enable_grip, queue=True):
        """
        Włącza lub wyłącza chwytak efektora końcowego.

        Args:
            enable_control (bool): Czy kontrolować chwytak (True lub False).
            enable_grip (bool): Czy zamknąć chwytak (True) lub go otworzyć (False).
            queue (bool): Czy dodać komendę do kolejki (domyślnie True).

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 63, True, queue, [enable_control, enable_grip], direction='out')
        return self.send(request)
    # TODO bad documantetion not implemented
    def set_jog_command(self, jog_type, command, queue=True):
        """
        Wysyła polecenie JOG do urządzenia.

        Args:
            jog_type (int): Typ ruchu JOG.
            command (int): Komenda JOG.
            queue (bool): Czy dodać komendę do kolejki (domyślnie True).

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 73, True, queue, [jog_type, command], direction='out')
        return self.send(request)

    def get_sliding_rail_jog_params(self):
        """
        Pobiera parametry ruchu JOG dla szyny przesuwnej.

        Returns:
            dict: Parametry ruchu, w tym prędkość i przyspieszenie.
        """
        request = Message([0xAA, 0xAA], 2, 74, False, False, [], direction='out')
        return self.send(request)

    def set_sliding_rail_jog_params(self, velocity, acceleration, queue=True):
        """
        Ustawia parametry ruchu JOG dla szyny przesuwnej.

        Args:
            velocity (float): Prędkość ruchu.
            acceleration (float): Przyspieszenie ruchu.
            queue (bool): Czy dodać komendę do kolejki (domyślnie True).

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 74, True, queue, [velocity, acceleration], direction='out')
        return self.send(request)

    def get_point_to_point_joint_params(self):
        """
        Pobiera parametry ruchu PTP dla osi stawowych.

        Returns:
            dict: Parametry ruchu, w tym prędkości i przyspieszenia dla każdej osi.
        """
        request = Message([0xAA, 0xAA], 2, 80, False, False, [], direction='out')
        return self.send(request)

    def set_point_to_point_joint_params(self, velocity, acceleration, queue=True):
        """
        Ustawia parametry ruchu PTP dla osi stawowych.

        Args:
            velocity (list[float]): Lista prędkości dla każdej osi.
            acceleration (list[float]): Lista przyspieszeń dla każdej osi.
            queue (bool): Czy dodać komendę do kolejki (domyślnie True).

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 80, True, queue, velocity + acceleration, direction='out')
        return self.send(request)

    def get_point_to_point_coordinate_params(self):
        """
        Pobiera parametry ruchu PTP w układzie współrzędnych kartezjańskich.

        Returns:
            dict: Parametry ruchu, w tym prędkość i przyspieszenie dla współrzędnych kartezjańskich.
        """
        request = Message([0xAA, 0xAA], 2, 81, False, False, [], direction='out')
        return self.send(request)

    def set_point_to_point_coordinate_params(self, coordinate_velocity, effector_velocity, coordinate_acceleration, effector_acceleration, queue=True):
        """
        Ustawia parametry ruchu PTP w układzie współrzędnych kartezjańskich.

        Args:
            coordinate_velocity (float): Prędkość ruchu współrzędnych kartezjańskich.
            effector_velocity (float): Prędkość ruchu efektora końcowego.
            coordinate_acceleration (float): Przyspieszenie współrzędnych kartezjańskich.
            effector_acceleration (float): Przyspieszenie efektora końcowego.
            queue (bool): Czy dodać komendę do kolejki (domyślnie True).

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 81, True, queue, [coordinate_velocity, effector_velocity, coordinate_acceleration, effector_acceleration], direction='out')
        return self.send(request)

    def get_point_to_point_common_params(self):
        """
        Pobiera wspólne parametry ruchu PTP.

        Returns:
            dict: Współczynnik prędkości i przyspieszenia dla ruchu PTP.
        """
        request = Message([0xAA, 0xAA], 2, 83, False, False, [], direction='out')
        return self.send(request)

    def set_point_to_point_common_params(self, velocity_ratio, acceleration_ratio, queue=True):
        """
        Ustawia wspólne parametry ruchu PTP.

        Args:
            velocity_ratio (float): Współczynnik prędkości.
            acceleration_ratio (float): Współczynnik przyspieszenia.
            queue (bool): Czy dodać komendę do kolejki (domyślnie True).

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 83, True, queue, [velocity_ratio, acceleration_ratio], direction='out')
        return self.send(request)

    def set_point_to_point_command(self, mode, x, y, z, r, queue=True):
        """
        Wysyła polecenie PTP do urządzenia.

        Args:
            mode (int): Tryb ruchu PTP.
            x (float): Pozycja X.
            y (float): Pozycja Y.
            z (float): Pozycja Z.
            r (float): Obrót R.
            queue (bool): Czy dodać komendę do kolejki (domyślnie True).

        Returns:
            Any: Odpowiedź od urządzenia.
        """
        request = Message([0xAA, 0xAA], 2, 84, True, queue, [mode, x, y, z, r], direction='out')
        return self.send(request)

        
    def get_point_to_point_sliding_rail_params(self):
        request = Message([0xAA, 0xAA], 2, 85, False, False, [], direction='out')
        return self.send(request)

    def set_point_to_point_sliding_rail_params(self, velocity, acceleration, queue=True):
        request = Message([0xAA, 0xAA], 2, 85, True, queue, [velocity, acceleration], direction='out')
        return self.send(request)

    def set_point_to_point_sliding_rail_command(self, mode, x, y, z, r, l, queue=True):
        request = Message([0xAA, 0xAA], 2, 86, True, queue, [mode, x, y, z, r, l], direction='out')
        return self.send(request)

    def get_point_to_point_jump2_params(self):
        request = Message([0xAA, 0xAA], 2, 87, False, False, [], direction='out')
        return self.send(request)

    def set_point_to_point_jump2_params(self, start_height, end_height, z_limit, queue=True):
        request = Message([0xAA, 0xAA], 2, 87, True, queue, [start_height, end_height, z_limit], direction='out')
        return self.send(request)

    # TODO: Reference is ambigious here - needs testing
    def set_point_to_point_po_command(self, mode, x, y, z, r, queue=True):
        request = Message([0xAA, 0xAA], 2, 88, True, queue, [mode, x, y, z, r], direction='out')
        return self.send(request)

    # TODO: Reference is ambigious here - needs testing
    def set_point_to_point_sliding_rail_po_command(self, ratio, address, level, queue=True):
        request = Message([0xAA, 0xAA], 2, 89, True, queue, [ratio, address, level], direction='out')
        return self.send(request)

    def get_continous_trajectory_params(self):
        request = Message([0xAA, 0xAA], 2, 90, False, False, [], direction='out')
        return self.send(request)

    def set_continous_trajectory_params(self, max_planned_acceleration, max_junction_velocity, acceleration, queue=True):
        request = Message([0xAA, 0xAA], 2, 90, True, queue, [max_planned_acceleration, max_junction_velocity, acceleration, 0], direction='out')
        return self.send(request)

    def set_continous_trajectory_real_time_params(self, max_planned_acceleration, max_junction_velocity, period, queue=True):
        request = Message([0xAA, 0xAA], 2, 90, True, queue, [max_planned_acceleration, max_junction_velocity, period, 1], direction='out')
        return self.send(request)

    def set_continous_trajectory_command(self, mode, x, y, z, velocity, queue=True):
        request = Message([0xAA, 0xAA], 2, 91, True, queue, [mode, x, y, z, velocity], direction='out')
        return self.send(request)

    def set_continous_trajectory_laser_engraver_command(self, mode, x, y, z, power, queue=True):
        request = Message([0xAA, 0xAA], 2, 92, True, queue, [mode, x, y, z, power], direction='out')
        return self.send(request)

    def get_arc_params(self):
        request = Message([0xAA, 0xAA], 2, 100, False, False, [], direction='out')
        return self.send(request)

    def set_arc_params(self, coordinate_velocity, effector_velocity, coordinate_acceleration, effector_acceleration, queue=True):
        request = Message([0xAA, 0xAA], 2, 100, True, queue, [coordinate_velocity, effector_velocity, coordinate_acceleration, effector_acceleration], direction='out')
        return self.send(request)

    def set_arc_command(self, circumference_point, ending_point, queue=True):
        request = Message([0xAA, 0xAA], 2, 101, True, queue, circumference_point + ending_point, direction='out')
        return self.send(request)

    def wait(self, milliseconds, queue=True):
        request = Message([0xAA, 0xAA], 2, 110, True, queue, [milliseconds], direction='out')
        return self.send(request)

    def set_trigger_command(self, address, mode, condition, threshold, queue=True):
        request = Message([0xAA, 0xAA], 2, 120, True, queue, [address, mode, condition, threshold], direction='out')
        return self.send(request)

    def get_io_multiplexing(self):
        request = Message([0xAA, 0xAA], 2, 130, False, False, [], direction='out')
        return self.send(request)

    def set_io_multiplexing(self, address, multiplex, queue=True):
        request = Message([0xAA, 0xAA], 2, 130, True, queue, [address, multiplex], direction='out')
        return self.send(request)

    def get_io_do(self):
        request = Message([0xAA, 0xAA], 2, 131, False, False, [], direction='out')
        return self.send(request)

    def set_io_do(self, address, level, queue=True):
        request = Message([0xAA, 0xAA], 2, 131, True, queue, [address, level], direction='out')
        return self.send(request)

    def get_io_pwm(self):
        request = Message([0xAA, 0xAA], 2, 132, False, False, [], direction='out')
        return self.send(request)

    def set_io_pwm(self, address, frequency, duty_cycle, queue=True):
        request = Message([0xAA, 0xAA], 2, 132, True, queue, [address, frequency, duty_cycle], direction='out')
        return self.send(request)

    def get_io_di(self):
        request = Message([0xAA, 0xAA], 2, 133, False, False, [], direction='out')
        return self.send(request)

    def get_io_adc(self):
        request = Message([0xAA, 0xAA], 2, 134, False, False, [], direction='out')
        return self.send(request)

    def set_extended_motor_velocity(self, index, enable, speed, queue=True):
        request = Message([0xAA, 0xAA], 2, 135, True, queue, [index, enable, speed], direction='out')
        return self.send(request)

    def get_color_sensor(self, index):
        request = Message([0xAA, 0xAA], 2, 137, False, False, [], direction='out')
        return self.send(request)

    def set_color_sensor(self, index, enable, port, version, queue=True):
        request = Message([0xAA, 0xAA], 2, 137, True, queue, [enable, port, version], direction='out')
        return self.send(request)

    def get_ir_switch(self, index):
        request = Message([0xAA, 0xAA], 2, 138, False, False, [], direction='out')
        return self.send(request)

    def set_ir_switch(self, index, enable, port, version, queue=True):
        request = Message([0xAA, 0xAA], 2, 138, True, queue, [enable, port, version], direction='out')
        return self.send(request)

    def get_angle_sensor_static_error(self, index):
        request = Message([0xAA, 0xAA], 2, 140, False, False, [], direction='out')
        return self.send(request)

    def set_angle_sensor_static_error(self, index, rear_arm_angle_error, front_arm_angle_error):
        request = Message([0xAA, 0xAA], 2, 140, True, False, [rear_arm_angle_error, front_arm_angle_error], direction='out')
        return self.send(request)

    def get_wifi_status(self):
        request = Message([0xAA, 0xAA], 2, 150, False, False, [], direction='out')
        return self.send(request)

    def set_wifi_status(self, index, enable):
        request = Message([0xAA, 0xAA], 2, 150, True, False, [enable], direction='out')
        return self.send(request)

    def get_wifi_ssid(self):
        request = Message([0xAA, 0xAA], 2, 151, False, False, [], direction='out')
        return self.send(request)

    def set_wifi_ssid(self, index, ssid):
        request = Message([0xAA, 0xAA], 2, 151, True, False, [ssid], direction='out')
        return self.send(request)

    def get_wifi_password(self):
        request = Message([0xAA, 0xAA], 2, 152, False, False, [], direction='out')
        return self.send(request)

    def set_wifi_password(self, index, ssid):
        request = Message([0xAA, 0xAA], 2, 152, True, False, [ssid], direction='out')
        return self.send(request)

    def get_wifi_address(self):
        request = Message([0xAA, 0xAA], 2, 153, False, False, [], direction='out')
        return self.send(request)

    # 192.168.1.1 = a.b.c.d
    def set_wifi_address(self, index, use_dhcp, a, b, c, d):
        request = Message([0xAA, 0xAA], 2, 153, True, False, [use_dhcp, a, b, c, d], direction='out')
        return self.send(request)

    def get_wifi_netmask(self):
        request = Message([0xAA, 0xAA], 2, 154, False, False, [], direction='out')
        return self.send(request)

    # 255.255.255.0 = a.b.c.d
    def set_wifi_netmask(self, index, a, b, c, d):
        request = Message([0xAA, 0xAA], 2, 154, True, False, [a, b, c, d], direction='out')
        return self.send(request)

    def get_wifi_gateway(self):
        request = Message([0xAA, 0xAA], 2, 155, False, False, [], direction='out')
        return self.send(request)

    # 192.168.1.1 = a.b.c.d
    def set_wifi_gateway(self, index, use_dhcp, a, b, c, d):
        request = Message([0xAA, 0xAA], 2, 155, True, False, [use_dhcp, a, b, c, d], direction='out')
        return self.send(request)

    def get_wifi_dns(self):
        request = Message([0xAA, 0xAA], 2, 156, False, False, [], direction='out')
        return self.send(request)

    # 192.168.1.1 = a.b.c.d
    def set_wifi_dns(self, index, use_dhcp, a, b, c, d):
        request = Message([0xAA, 0xAA], 2, 156, True, False, [use_dhcp, a, b, c, d], direction='out')
        return self.send(request)

    def get_wifi_connect_status(self):
        request = Message([0xAA, 0xAA], 2, 157, False, False, [], direction='out')
        return self.send(request)

    def set_lost_step_params(self, param):
        request = Message([0xAA, 0xAA], 2, 170, True, False, [param], direction='out')
        return self.send(request)

    def set_lost_step_command(self):
        request = Message([0xAA, 0xAA], 2, 171, True, False, [], direction='out')
        return self.send(request)

    def start_queue(self):
        request = Message([0xAA, 0xAA], 2, 240, True, False, [], direction='out')
        return self.send(request)

    def stop_queue(self, force=False):
        request = Message([0xAA, 0xAA], 2, 242 if force else 241, True, False, [], direction='out')
        return self.send(request)

    def start_queue_download(self, total_loop, line_per_loop):
        request = Message([0xAA, 0xAA], 2, 243, True, False, [total_loop, line_per_loop], direction='out')
        return self.send(request)

    def stop_queue_download(self):
        request = Message([0xAA, 0xAA], 2, 244, True, False, [], direction='out')
        return self.send(request)

    def clear_queue(self):
        request = Message([0xAA, 0xAA], 2, 245, True, False, [], direction='out')
        return self.send(request)

    def get_current_queue_index(self):
        request = Message([0xAA, 0xAA], 2, 246, True, False, [], direction='out')
        return self.send(request)
