import gyro

class FSM:
    def __init__(self):
        #initializing states
        self.start = self._create_start()
        self.moveCloser = self._create_moveCloser()
        self.moveForward = self._create_moveForward()
        self.parking = self._create_parking()

        # setting current state of the system
        self.current_state = self.start

        self.stopped = False

    def send(self, tilt, velocity, gyro):
        try:
            self.current_state.send(tilt, velocity, gyro)
        except StopIteration:
            self.stopped = True
    
    
    def _create_moveCloser(self):
        while True:
            tilt = yield
            velocity = yield
            gyro = yield

            # some condition here to set the next state
            """
            if tilt > ________:
                self.current_state = self.moveCloser
            else:
                break
            """
    
    def _create_moveForward(self):
        while True:
            tilt = yield
            velocity = yield
            gyro = yield

            # some condition here to set the next state


    def _create_parking(self):
        while True:
            tilt = yield
            velocity = yield
            gyro = yield

            # some condition here to set the next state
    

    def _create_start(self):
        while True:
            tilt = yield
            velocity = yield
            gyro = yield

            # some condition here to set the next state
        
    


