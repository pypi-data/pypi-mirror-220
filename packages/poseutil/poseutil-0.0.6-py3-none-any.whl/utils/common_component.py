import os
import shutil
import time
import glob
import gzip, pickle
from utils.const import *
import numpy as np
import cv2
import re, json
import tensorflow as tf
from utils.poseMeasure import PoseMeasure
from utils.normarlize import getPoseEmbeddingList
from utils.version import VersionCaster
import struct, itertools
import matplotlib.pyplot as plt

def get_dance_audio_list():
    audio_list_path = DANCE_AUDIO_PATH
    sorted_list = sorted(os.listdir(audio_list_path))
    if 'common' in sorted_list:
        sorted_list.remove('common')
    return sorted(sorted_list)

def get_dance_audio(audio, speed=1.0):
    selected_auido = f"{audio}_{speed}.mp3"
    return f"{DANCE_AUDIO_PATH}/{audio}/{selected_auido}"

def dump_json_data(json_path, data):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent="\t")

def get_json_data_all(json_path):
    with open(json_path, 'r') as f:
        data =  json.load(f)
    return data

def get_json_data(json_path, audio_name):
    with open(json_path, 'r') as f:
        data =  json.load(f)
    return data[audio_name]

def write_json_data(json_path, data):
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
    
def get_audio_name(audio_path):
    return audio_path.split("/")[-1].split(".")[0].split("_")[0]
    
def add_infomation_circle(img, text):
    mask = img.copy()
    cv2.circle(mask, (150,150), 150, (0, 0, 0), -1)
    cv2.putText(mask, text, (60, 220), cv2.FONT_HERSHEY_SIMPLEX, 8, (255, 255, 255), 5)
    return cv2.addWeighted(img, 0.3, mask, 0.7, 0)

def get_speed(audio_path):
    p = re.compile("[0-9].[0-9]*")
    audio_speed = float(p.findall(audio_path)[0]) if p.findall(audio_path) else 1
    return audio_speed

def current_milli_time():
    return round(time.time() * 1000)

def sort_list_dir(path):
    dir_list = os.listdir(path)
    dir_list.sort()
    return dir_list

def time_jpg_priority(x):
    return int(x.split('/')[-1].split('.')[0])
    
def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            shutil.rmtree(directory)
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def get_sync_time(origin_time, video_time):
    x = 0
    while origin_time != (video_time + x):
        if origin_time > video_time:
            x += 1
        else:
            x -= 1
    print(x)
    return x

def load_pickle_dance(name):
    with gzip.open(f"{DANCE_PICKLE_PATH}/{name}.pickle") as f:
        pickle_data = pickle.load(f)
    return pickle_data

def load_pickle_path(path):
    with gzip.open(path) as f:
        pickle_data = pickle.load(f)
    return pickle_data

def load_img_list(name):
    img_list = sorted(glob.glob(f"{DANCE_IMG_PATH}/{name}/*.jpg"), key=lambda x: int(x.split("/")[-1].replace(".jpg", "")))
    return img_list
    
def search_timetable(origin_timetable, compare_timetable, origin_num, compare_num):
    sync_num = 0
    origin_time = origin_timetable[origin_num]
    compare_time = compare_timetable[compare_num]
    while origin_time >= compare_time:
        sync_num += 1
        compare_time = compare_timetable[compare_num + sync_num]
    
    prev_compare_time = compare_timetable[compare_num + sync_num -1]

    if abs(origin_time - compare_time) < abs(origin_time - prev_compare_time):
        return int(compare_num + sync_num), compare_time
    else :
        return int(compare_num + sync_num - 1), prev_compare_time

def rewind_search_timetable(origin_timetable, compare_timetable, origin_num, compare_num):
    sync_num = 0
    origin_time = origin_timetable[origin_num]
    compare_time = compare_timetable[compare_num]
    while origin_time <= compare_time:
        sync_num -= 1
        compare_time = compare_timetable[compare_num + sync_num]
    
    prev_compare_time = compare_timetable[compare_num + sync_num + 1]

    if abs(origin_time - compare_time) < abs(origin_time - prev_compare_time):
        return int(compare_num + sync_num), compare_time
    else :
        return int(compare_num + sync_num + 1), prev_compare_time
    
def load_tflite_model(path):
    model = tf.lite.Interpreter(model_path=path)
    model.allocate_tensors()
    input_index = model.get_input_details()[0]['index']
    output_index = model.get_output_details()[0]['index']

    return model, input_index, output_index

def inference_tflite_model(model, input, input_index, output_index):
    model.set_tensor(input_index, input)
    model.invoke()
    return model.get_tensor(output_index)

def get_input_for_mlp(pose, embedding, side, standardJoint=None, standardCoord=None, standardEquation=None):
    poseMeasure = PoseMeasure(pose)
    if side:
        if poseMeasure.getCoord(pose[eval(standardJoint)], standardCoord) < poseMeasure.getCoord(pose[eval(standardJoint)+1], standardCoord):
            if standardEquation == "MINUS":
                inputs = getPoseEmbeddingList(pose, embedding.upper() + "LEFT")
            else:
                inputs = getPoseEmbeddingList(pose, embedding.upper() + "RIGHT")
        else:
            if standardEquation == "MINUS":
                inputs = getPoseEmbeddingList(pose, embedding.upper() + "RIGHT")
            else:
                inputs = getPoseEmbeddingList(pose, embedding.upper() + "LEFT")
    else:
        inputs = getPoseEmbeddingList(pose, embedding.upper())
    return np.expand_dims(np.array(inputs).astype(np.float32), axis=0)

def get_emaSmoothing_for_mlp(history, window_size, factor, ratio):
    results = history[-window_size:]
    emaSmoothing = {"U": 0, "M": 0, "D": 0}
    for i in results[::-1]:
        emaSmoothing[i] = round(emaSmoothing[i] + factor, 2)
        factor *= ratio
    return sorted(emaSmoothing.items(), key=lambda x: x[1], reverse=True)[0][0], emaSmoothing

def process(file):
    unpack_data = []
    with open(file, "rb") as f:
        data = f.read()

    for cell in range(0, int(len(data)), 4):
        unpack_data.append(struct.unpack('i', data[cell: cell+4])[0])
    
    return unpack_data

def pop_header(data):
    casting_data = []
    header = data.pop(0)
    version = VersionCaster(header)
    line = version.get_version_casting_line()
    for line_cnt in range(0, len(data), line):
        casting_data.append(data[line_cnt : line_cnt + line])
    return casting_data, header

def get_bin_data(file):
    bin_data = process(file)
    header = bin_data.pop(0)
    versionCaster = VersionCaster(header)

    data = np.array(bin_data)
    info_data = versionCaster.get_data(data)
    return info_data

def plot_confusion_matrix(cm, model_path, target_names=None, cmap=None, normalize=True, labels=True, title='Confusion matrix'):
    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        
    plt.figure(figsize=(8, 8))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    
    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names)
        plt.yticks(tick_marks, target_names)
    
    if labels:
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            if normalize:
                plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                         horizontalalignment="center",
                         color="white" if cm[i, j] > thresh else "black")
            else:
                plt.text(j, i, "{:,}".format(cm[i, j]),
                         horizontalalignment="center",
                         color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.savefig(f"{model_path}/confusion_matrix.png")
