# -*- coding: utf-8 -*-

import unittest
from core.parameter import *
from core.fakedevice import *
from util.log import Logger
from core.rgbd_segmentation import RGBDSegmentation
from core.parameter import Parameter
from core.frame import *
import os
import glob
import os.path as osp
from pathlib import Path
import psutil
from datetime import datetime
import time
import nvidia_smi

os.makedirs('results', exist_ok=True)
f = open("results/run_" + str(int(round(time.time() * 1000))) + ".txt", "w+")
f.write('=== Start time: ' + str(datetime.now()) + '\n')

p = psutil.Process(os.getpid())
nvidia_smi.nvmlInit()
handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)

parameter = Parameter(Segmentation.GRAPH_CANNY, scale=2)
seg = RGBDSegmentation(parameter)

print('Starting list image files')
filesCount = 0

files = glob.glob("datasets/mestrado/**/rgb/*.png", recursive=True)
files.extend(glob.glob("datasets/mestrado/**/rgb/*.jpg", recursive=True))
cpuTimes = [0.0, 0.0, 0.0, 0.0]

gpuTimes = 0.0
gpuMemTimes = 0.0
maxNumThreads = 0
memUsageTimes = 0

for imagePath in files:
    print('imagePath: ' + imagePath)
    pathRgb = Path(imagePath)
    datasetName = osp.basename(str(pathRgb.parent.parent))
    # print('datasetName: ' + datasetName)
    parentDatasetDir = str(pathRgb.parent.parent)
    # print('parentDatasetDir: ' + parentDatasetDir)
    depthImageName = os.path.basename(imagePath).replace('jpg', 'png')

    frame = RGBDFrame(RGBFrame(parentDatasetDir+'/rgb/', os.path.basename(imagePath)), DepthFrame(parentDatasetDir+'/depth/', depthImageName))
    seg.process(frame, datasetName)
    res = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
    mem_res = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
    curGpuTime = res.gpu
    # curGpuMemTime = res.memory #(in percent)
    curGpuMemTime = mem_res.used / 1e+6
    gpuTimes += curGpuTime
    gpuMemTimes += curGpuMemTime
    f.write('GPU Usage Percent: ' + str(curGpuTime) + '\n')
    f.write('GPU Mem Usage (MB)): ' + str(curGpuMemTime) + '\n')

    curProcessCpuPerU = p.cpu_percent()
    curCpusPerU = psutil.cpu_percent(interval=None, percpu=True)

    # gives a single float value
    for i in range(len(cpuTimes)):
        curProcessCpu = curProcessCpuPerU
        curCpu = curCpusPerU[i]
        cpuTimes[i] += curCpu
        f.write('Process CPU Percent: ' + str(curProcessCpu) + ' --- CPU Percent: ' + str(curCpu) + '\n')

    # you can convert that object to a dictionary
    memInfo = dict(p.memory_full_info()._asdict())
    curMemUsage = memInfo['uss']
    memUsageTimes += curMemUsage

    f.write('Process memory usage: ' + str(curMemUsage / 1e+6) + '\n')
    f.write('Memory information: ' + str(memInfo) + '\n')

    if maxNumThreads < p.num_threads():
        maxNumThreads = p.num_threads()

    # print('############## Index: ')
    # print(index)
    os.makedirs('results/' + datasetName, exist_ok=True)
    seg.write_labels_to_file('results/' + datasetName + '/' + depthImageName, True)
    seg.finish()
    filesCount = filesCount + 1
nvidia_smi.nvmlShutdown()

start = time.time()
for imagePath in files:
    pathRgb = Path(imagePath)
    datasetName = osp.basename(str(pathRgb.parent.parent))
    parentDatasetDir = str(pathRgb.parent.parent)
    depthImageName = os.path.basename(imagePath).replace('jpg', 'png')

    frame = RGBDFrame(RGBFrame(parentDatasetDir+'/rgb/', os.path.basename(imagePath)), DepthFrame(parentDatasetDir+'/depth/', depthImageName))
    seg.process(frame, datasetName)
    seg.finish()
end = time.time()

f.write('=== Mean GPU Usage Percent: ' + str(gpuTimes / filesCount) + '\n')
f.write('=== Mean GPU Mem Usage (MB): ' + str(gpuMemTimes / filesCount) + '\n')
for i in range(len(cpuTimes)):
    f.write("=== Mean cpu" + str(i) + " usage: " + str(cpuTimes[i] / filesCount) + '\n')
f.write("=== Mean memory usage (MB): " + str((memUsageTimes / filesCount) / 1e+6) + '\n')

f.write("=== Total image predicted: " + str(filesCount) + '\n')
f.write("=== Seconds per image: " + str(((end - start) / filesCount)) + '\n')
f.write("=== Max num threads: " + str(maxNumThreads) + '\n')

f.write('=== End time: ' + str(datetime.now()) + '\n')
f.close()