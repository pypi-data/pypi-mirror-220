from dataclasses import dataclass
import numpy as np
from utils.pose_util import Coordinate
from utils.const import *


body_setting_id = [NOSE, LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_KNEE, RIGHT_KNEE,
                   LEFT_ELBOW, LEFT_WRIST, LEFT_ANKLE,  
                   RIGHT_ELBOW, RIGHT_WRIST, RIGHT_ANKLE,
                   RIGHT_HIP, LEFT_HIP]

body_setting_id_right = [RIGHT_SHOULDER, RIGHT_KNEE,
                         RIGHT_ELBOW, RIGHT_WRIST, RIGHT_ANKLE,
                         RIGHT_HIP]

body_setting_id_left = [LEFT_SHOULDER, LEFT_KNEE,
                        LEFT_ELBOW, LEFT_WRIST, LEFT_ANKLE,
                        LEFT_HIP]

foot_setting_id = [LEFT_FOOT_INDEX, LEFT_HEEL, RIGHT_FOOT_INDEX, RIGHT_HEEL]
foot_setting_id_left = [LEFT_FOOT_INDEX, LEFT_HEEL]
foot_setting_id_right = [RIGHT_FOOT_INDEX, RIGHT_HEEL]
hand_setting_id_left = [LEFT_THUMB, LEFT_PINKY, LEFT_INDEX]
hand_setting_id_right = [RIGHT_THUMB, RIGHT_PINKY, RIGHT_INDEX]




# ============= version 1.0 info ==================
dataclass
class Version1010:
    header = 1010
    prefix = 2
    suffix = 1
    row_len = 42
    status_kind = ["UP", "DOWN"]
    info_index = {"time": 0, "status": 1, "pose": (2, 41), "reps": 41}
    body_list = [NOSE, LEFT_SHOULDER, RIGHT_SHOULDER, 
            LEFT_ELBOW, RIGHT_ELBOW, LEFT_WRIST, RIGHT_WRIST, 
            LEFT_HIP, RIGHT_HIP, LEFT_KNEE, RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE]
    landmark_range = len(body_list) * 3
    z_weight = 1
# ============= version 1.0 info ==================

# ============= version 1.1 info ==================
dataclass
class Version1110:
    header = 1110
    prefix = 2
    suffix = 1
    row_len = 42
    status_kind = ["UP", "DOWN"]
    info_index = {"time": 0, "status": 1, "pose": (2, 41), "reps": 41}
    body_list = [NOSE, LEFT_SHOULDER, RIGHT_SHOULDER, 
            LEFT_ELBOW, RIGHT_ELBOW, LEFT_WRIST, RIGHT_WRIST, 
            LEFT_HIP, RIGHT_HIP, LEFT_KNEE, RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE]
    landmark_range = len(body_list) * 3
    z_weight = 1
# ============= version 1.1 info ==================

# ============= version 1.11 info ==================
dataclass
class Version1111:
    header = 1111
    prefix = 2
    suffix = 1
    info_index = {"time": 0, "status": 1, "pose": (2, 41), "reps": 41}
    row_len = 42
    status_kind = ["UP", "DOWN", "RESTING"]
    body_list = [NOSE, LEFT_SHOULDER, RIGHT_SHOULDER, 
            LEFT_ELBOW, RIGHT_ELBOW, LEFT_WRIST, RIGHT_WRIST, 
            LEFT_HIP, RIGHT_HIP, LEFT_KNEE, RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE]
    landmark_range = len(body_list) * 3
    z_weight = 1

class Version2113:
    header = 2113
    prefix = 3
    suffix = 0
    info_index = {"time": 0, "status": 1, "reps": 2, "pose": (3, 69)}
    row_len = 69
    status_kind = ["UP", "MIDDLE", "DOWN", "RESTING"]
    body_list = [
        LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_ELBOW, RIGHT_ELBOW, LEFT_WRIST, RIGHT_WRIST, 
        LEFT_PINKY, RIGHT_PINKY, LEFT_INDEX, RIGHT_INDEX, LEFT_THUMB, RIGHT_THUMB, 
        LEFT_HIP, RIGHT_HIP, LEFT_KNEE, RIGHT_KNEE, LEFT_ANKLE, RIGHT_ANKLE,
        LEFT_HEEL, RIGHT_HEEL, LEFT_FOOT_INDEX, RIGHT_FOOT_INDEX,]
    landmark_range = len(body_list) * 3
    z_weight = 1
    

# ============= version 1.1 info ==================

# =============     Full info    ==================
class VersionDefault:
    header = 0
    prefix = 1
    suffix = 0
    body_list = [i for i in range(0, 33)]
    landmark_range = ALL * 3
    z_weight = 0.6

# =============     Full info    ==================
# =============     Full info    ==================
class VersionDefault_1:
    header = 0
    prefix = 1
    suffix = 0
    row_len = 42
    body_list = [i for i in range(0, 33)]
    landmark_range = ALL * 3
    z_weight = 0.6
# =============     Full info    ==================

# =============     Full info    ==================
class VersionDefault_live:
    header = 0
    prefix = 1
    suffix = 0
    row_len = 42
    body_list = [i for i in range(0, 33)]
    landmark_range = ALL * 3
    z_weight = 0.6
# =============     Full info    ==================

version_list = [Version1010, Version1110, Version1111, Version2113, VersionDefault, VersionDefault_1]

class VersionCaster:
    def __init__(self, header, direct=None):
        version_dict = {
            1010: Version1010(),
            1110: Version1110(),
            1111: Version1111(),
            2113: Version2113(),
            }
        self.version = version_dict[header]
        self.prefix = version_dict[header].prefix
        self.suffix = version_dict[header].suffix
        self.landmark_range = version_dict[header].landmark_range
        self.z_weight = version_dict[header].z_weight

    def get_data(self, frame_data):
        frame_data = np.reshape(frame_data, (-1, self.version.row_len))
        info_index = self.version.info_index
        info_data = {i: [] for i in info_index.keys()}
        for frame in frame_data:
            for key in info_index.keys():
                if key == "pose":
                    zip_pose = frame[info_index[key][0]: info_index[key][1]]
                    zip_idx = 0
                    pose = []
                    for idx in range(33):
                        if idx in self.version.body_list:
                            pose.append(Coordinate(zip_pose[zip_idx * 3], zip_pose[zip_idx * 3 + 1], zip_pose[zip_idx * 3 + 2]))
                            zip_idx += 1
                        else:
                            pose.append(Coordinate(0, 0, 0))
                    info_data[key].append(pose)
                elif key == "status":
                    info_data[key].append(self.version.status_kind[frame[info_index[key]]])
                else:
                    info_data[key].append(frame[info_index[key]])
        return info_data

    # 바이너리 데이터 에서 프레임 데이터 한줄씩 자르는 루틴
    def get_version_casting_line(self):
        return self.version.prefix + self.version.suffix + self.version.landmark_range

    def get_version_casting_convert_pose_data_live(self, frame, z_weight=None, frame_weight=1):
        if z_weight == None:
            z_weight = self.z_weight
        body_list = self.version.body_list
        line = []
        cnt = self.prefix
        for body in range(0, 33):
            if body in body_list:
                x = frame[cnt] / frame_weight
                y = frame[cnt+1] / frame_weight
                z = (frame[cnt+2] * z_weight) / frame_weight
                line.append(Coordinate(x, y, z))
                cnt += 3
            else :
                line.append(Coordinate(0,0,0))
        return line

    def get_version_casting_convert_pose_data(self, frame_data, z_weight = None, frame_weight = 1):
        if frame_data[0][0] == "up" or frame_data[0][0] =="down":
            self.prefix = 1
            z_weight = 1
        if z_weight == None:
            z_weight = self.z_weight
        body_list = self.version.body_list
        result = []
        for frame in frame_data:
            line = []
            cnt = self.prefix
            for body in range(0, 33):
                if body in body_list:
                    x = frame[cnt] / frame_weight
                    y = frame[cnt+1] / frame_weight
                    z = (frame[cnt+2] * z_weight) / frame_weight
                    line.append(Coordinate(x, y, z, 0))
                    cnt += 3
                else :
                    line.append(Coordinate(0,0,0, 0))
            result.append(line)
        return result

    def get_version_casting_convert_pose_data_normalize(self, frame_data, z_weight = None):
        if frame_data[0][0] == "up" or frame_data[0][0] =="down":
            self.prefix = 1
            z_weight = 1
        if z_weight == None:
            z_weight = self.z_weight
        body_list = self.version.body_list
        result = []
        for frame in frame_data:
            line = []
            cnt = self.prefix
            for body in range(0, 33):
                if body in body_list:
                    x = frame[cnt]
                    y = frame[cnt+1]
                    z = frame[cnt+2] * z_weight
                    line.append(Coordinate(x, y, z))
                    cnt += 3
                else :
                    line.append(Coordinate(0,0,0))
            result.append(line)
        
        X, Y, Z = self.makeNormalize(result)
        
        result_normalize = []
        for line in result:
            line_normalize = []
            cnt = self.prefix
            for bodyNum, body in enumerate(line):
                y = self.footPointSetting(bodyNum, body, Y)
                z = self.bodyPointSetting(bodyNum, body, Z)
                line_normalize.append(Coordinate(body.x, y, z))
            result_normalize.append(line_normalize)
            
        return result_normalize


    def bodyPointSetting(self, bodyNum, body, Z):
        if bodyNum in body_setting_id:
            return (body.z - (Z[bodyNum]))
        elif bodyNum in foot_setting_id_right:
            return (body.z - Z[RIGHT_ANKLE])
        elif bodyNum in foot_setting_id_left:
            return (body.z - Z[LEFT_ANKLE])
        elif bodyNum in hand_setting_id_right:
            return (body.z - Z[RIGHT_WRIST])
        elif bodyNum in hand_setting_id_left:
            return (body.z - Z[LEFT_WRIST])
        else:
            return body.z

    def footPointSetting(self, bodyNum, body, Y):
        normalize_foot_left_y = (Y[LEFT_FOOT_INDEX] - Y[LEFT_HEEL]) / 2
        normalize_foot_right_y = (Y[RIGHT_FOOT_INDEX] - Y[RIGHT_HEEL]) / 2

        if normalize_foot_left_y > 0:
            if bodyNum is LEFT_FOOT_INDEX:
                return body.y - normalize_foot_left_y
            elif bodyNum is LEFT_HEEL:
                return body.y + normalize_foot_left_y
            elif bodyNum is RIGHT_FOOT_INDEX:
                return body.y - normalize_foot_right_y
            elif bodyNum is RIGHT_HEEL:
                return body.y + normalize_foot_right_y
            else:
                return body.y
        else:
            if bodyNum is LEFT_FOOT_INDEX:
                return body.y + normalize_foot_left_y
            elif bodyNum is LEFT_HEEL:
                return body.y - normalize_foot_left_y
            elif bodyNum is RIGHT_FOOT_INDEX:
                return body.y + normalize_foot_right_y
            elif bodyNum is RIGHT_HEEL:
                return body.y - normalize_foot_right_y
            else:
                return body.y

    def makeNormalize(self, data_set, maxFrameNum = 150, passFrameNum = 100):
        body_normalize_X = [0.0 for i in range(33)]
        body_normalize_Y = [0.0 for j in range(33)]
        body_normalize_Z = [0.0 for k in range(33)]
        frameNum = 0
        originFrameNum = maxFrameNum - passFrameNum

        for frameData in data_set:
            bodyNum = 0
            if frameNum >= passFrameNum:
                for cell in frameData:
                    body_normalize_X[bodyNum] += cell.x
                    body_normalize_Y[bodyNum] += cell.y
                    body_normalize_Z[bodyNum] += cell.z
                    bodyNum += 1

            frameNum += 1
            if frameNum >= maxFrameNum:
                break

        for i in range(0, 33, 1):
            body_normalize_X[i] = body_normalize_X[i] / (originFrameNum*1.5)
            body_normalize_Y[i] = body_normalize_Y[i] / (originFrameNum*1.5) 
            body_normalize_Z[i] = body_normalize_Z[i] / (originFrameNum*1.5)
        
        return body_normalize_X, body_normalize_Y, body_normalize_Z