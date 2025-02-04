# adapted from:  https://machinelearningspace.com/object-tracking-python/
import numpy as np


class KalmanFilter(object):
    """Kalman Filter class keeps track of the estimated state of
    the system and the variance or uncertainty of the estimate.
    Predict and Correct methods implement the functionality
    Code adapted from https://machinelearningspace.com/object-tracking-python/
    """

    def __init__(self, dt, u_x, u_y, std_acc, x_std_meas, y_std_meas, initial_state):
        """
        :param dt: sampling time (time for 1 cycle)
        :param u_x: acceleration in x-direction
        :param u_y: acceleration in y-direction
        :param std_acc: process noise magnitude
        :param x_std_meas: standard deviation of the measurement in x-direction
        :param y_std_meas: standard deviation of the measurement in y-direction
        :param initial_state: initial location [x,y] of track
        """

        # Define sampling time
        self.dt = dt

        # Define the  control input variables
        self.u = np.matrix([[u_x], [u_y]])

        # Intial State
        self.x = np.matrix([initial_state[0], initial_state[1], [0], [0]])

        # Define the State Transition Matrix A
        self.A = np.matrix([[1, 0, self.dt, 0],
                            [0, 1, 0, self.dt],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

        # Define the Control Input Matrix B
        self.B = np.matrix([[(self.dt ** 2) / 2, 0],
                            [0, (self.dt ** 2) / 2],
                            [self.dt, 0],
                            [0, self.dt]])

        # Define Measurement Mapping Matrix
        self.H = np.matrix([[1, 0, 0, 0],
                            [0, 1, 0, 0]])

        # Initial Process Noise Covariance
        self.Q = np.matrix([[(self.dt ** 4) / 4, 0, (self.dt ** 3) / 2, 0],
                            [0, (self.dt ** 4) / 4, 0, (self.dt ** 3) / 2],
                            [(self.dt ** 3) / 2, 0, self.dt ** 2, 0],
                            [0, (self.dt ** 3) / 2, 0, self.dt ** 2]]) * std_acc ** 2

        # Initial Measurement Noise Covariance
        self.R = np.matrix([[x_std_meas ** 2, 0],
                            [0, y_std_meas ** 2]])

        # Initial Covariance Matrix
        self.P = np.eye(self.A.shape[1])

    def predict(self):
        # Refer to :Eq.(9) and Eq.(10)
        # in https://machinelearningspace.com/object-tracking-python/
        # Update time state
        # x_k =Ax_(k-1) + Bu_(k-1)     Eq.(9)
        self.x = np.dot(self.A, self.x) + np.dot(self.B, self.u)
        # Calculate error covariance
        # P= A*P*A' + Q               Eq.(10)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.x[0:2]

    def update(self, z, flag):
        # Refer to :Eq.(11), Eq.(12) and Eq.(13)  in
        # https://machinelearningspace.com/object-tracking-python/
        # S = H*P*H'+R
        if not flag:
            # use prediction of previous
            z = self.x[0:2]  # + (self.dt * self.x[:2])

        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R
        # Calculate the Kalman Gain
        # K = P * H'* inv(H*P*H'+R)
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))  # Eq.(11)
        self.x = np.round(self.x + np.dot(K, (z - np.dot(self.H, self.x))))  # Eq.(12)
        I = np.eye(self.H.shape[1])
        # Update error covariance matrix
        self.P = (I - (K * self.H)) * self.P  # Eq.(13)
        return self.x[0:2]
