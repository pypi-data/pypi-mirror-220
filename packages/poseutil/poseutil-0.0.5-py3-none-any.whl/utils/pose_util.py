import copy
import math
import numpy as np
import mediapipe as mp
import cv2


class data:
    def __init__(self, poseState, successCount, failCount):
        self.poseState = poseState
        self.successCount = successCount
        self.failCount = failCount


class metaData:
    userData = []
    def addData(self, poseState, successCount, failCount):
        self.userData.append(data(poseState=poseState,
                                  successCount=successCount,
                                  failCount=failCount))
    def clear(self):
        self.userData.clear()


class Coordinate:
    def __init__(self, x, y, z, visibility=1.0):
        self.x = x
        self.y = y
        self.z = z
        self.visibility = visibility
        self.array = np.array([x, y, z])

    def __repr__(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}"
        
    def get_distance_2d(self, coord):
        return math.sqrt((self.x - coord.x) ** 2 + (self.y - coord.y) ** 2)
    
    def get_distance_3d(self, coord):
        return math.sqrt((self.x - coord.x) ** 2 + (self.y - coord.y) ** 2 + (self.z - coord.z) ** 2)

    def cos_sim(self, coord):
        return round(np.dot(self.array, coord.array) / (np.linalg.norm(self.array) * np.linalg.norm(coord.array)) * 100, 2)
    
    def get_center_coord(self, coord):
        x = (self.x + coord.x) / 2
        y = (self.x + coord.y) / 2
        z = (self.z + coord.z) / 2
        return Coordinate(x, y, z)


class position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __int__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0


class CustomPoseData:
    poseLandmarksDataFrame = []
    poseLandmarks = []
    poseLandmark = []

    def setzerosLandmark(self):
        if len(self.poseLandmark) > 33:
            self.poseLandmark.clear()
        for i in range(33):
            self.poseLandmark.append(position(0.0, 0.0, 0.0))

    def addLandmark(self, lm):
        self.poseLandmarks.append(position(lm.x, lm.y, lm.z))

    def addDataFrame(self):
        frameData = copy.deepcopy(self.poseLandmarks)
        self.poseLandmarksDataFrame.append(frameData)

    def clear(self):
        self.poseLandmark.clear()
        self.poseLandmarks.clear()


mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
def get_holistic_data(img):
    img.flags.writeable = False
    results = holistic.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img.flags.writeable = True
    mp_drawing.draw_landmarks(
        img,
        results.face_landmarks,
        mp_holistic.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_contours_style()
    )
    
    mp_drawing.draw_landmarks(
        img,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_pose_landmarks_style()
    )
    
    mp_drawing.draw_landmarks(
        img,
        results.left_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )

    mp_drawing.draw_landmarks(
        img,
        results.right_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        pose_landmark = [Coordinate(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks]
    else:
        pose_landmark = [Coordinate(0, 0, 0, 0) for _ in range(33)]

    if results.face_landmarks:
        landmarks = results.face_landmarks.landmark
        face_landmark = [Coordinate(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks]
    else:
        face_landmark = [Coordinate(0, 0, 0, 0) for _ in range(468)]

    if results.left_hand_landmarks:
        landmarks = results.left_hand_landmarks.landmark
        left_hand_landmark = [Coordinate(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks]
    else:
        left_hand_landmark = [Coordinate(0, 0, 0, 0) for _ in range(21)]

    if results.right_hand_landmarks:
        landmarks = results.right_hand_landmarks.landmark
        right_hand_landmark = [Coordinate(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks]
    else:
        right_hand_landmark = [Coordinate(0, 0, 0, 0) for _ in range(21)]

    return pose_landmark, face_landmark, left_hand_landmark, right_hand_landmark

def get_user_coordinate(results):
    user_coordinate = []
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        pose_landmark = [Coordinate(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks]
    else:
        pose_landmark = [Coordinate(0, 0, 0, 0) for _ in range(33)]

    if results.left_hand_landmarks:
        landmarks = results.left_hand_landmarks.landmark
        left_hand_landmark = [Coordinate(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks]
    else:
        left_hand_landmark = [Coordinate(0, 0, 0, 0) for _ in range(21)]

    if results.right_hand_landmarks:
        landmarks = results.right_hand_landmarks.landmark
        right_hand_landmark = [Coordinate(landmark.x, landmark.y, landmark.z, landmark.visibility) for landmark in landmarks]
    else:
        right_hand_landmark = [Coordinate(0, 0, 0, 0) for _ in range(21)]

    return pose_landmark, [left_hand_landmark, right_hand_landmark]

def convert_pose(poses, width, height):
    pose_data = []
    zWeight = (width + height) * 0.1
    for pose in poses:
        pose_data.append([Coordinate(i.x * width, i.y * height, i.z * zWeight) for i in pose])
    return pose_data