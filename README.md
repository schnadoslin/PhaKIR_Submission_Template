# PhaKIR Submission Template 
![PhaKIR](https://phakir.re-mic.de/wp-content/uploads/2024/02/Phakir-Logo-1.png)

Welcome to the submission and evaluation instructions for our [PhaKIR - Challenge: **Pha**se, **K**eypoint and **I**nstrument **R**ecognition](https://phakir.re-mic.de/)! In this challenge, you are required to provide a Docker image. The resulting container processes data from an input directory and writes the results to an output directory. We have provided a `docker-compose.yml` file to simulate the evaluation environment and test resource limitations.

You can use this repository as an evaluation template for all three [PhaKIR-Tasks:](https://phakir.re-mic.de/tasks/)

- Surgical Procedure Phase Recognition
- Surgical Instrument Keypoint Estimation
- Surgical Instrument Instance Segmentation

This repository will help you with the submission and evaluation of your method to our challenge. 
You will find information about the [Data](#data) structure for both training and submission.
To participate in the challenge, you have to provide a Docker image to process the data provided. You can find information about the requirements for the Docker environment in the [Docker](#docker) section.
The [Testing and Constraints](#testing-and-constraints) section provides information about the constraints of the evaluation environment.
The [Submission](#submission) section describes important submission formalities, and the [Evaluation](#evaluation) section provides information about the evaluation process and the metrics used.

# Table of Contents
1. [Repository Structure](#repository-structure)
2. [Data](#data)
     1. [Structure](#structure)
     2. [Outputs](#outputs)
          1. [Surgical Procedure Phase Recognition](#surgical-procedure-phase-recognition)
          2. [Surgical Instrument Keypoint Estimation](#surgical-instrument-keypoints-estimation)
          3. [Surgical Instrument Instance Segmentation](#surgical-instrument-instance-segmentation)
3. [Docker](#docker)
     1. [Image](#image)
     2. [Testing and Constraints](#testing-and-constraints)
4. [Submission](#submission)
5. [Evaluation](#evaluation)
     1. [Metrics](#metrics)
          1. [Surgical Procedure Phase Recognition](#metrics-phase)
          2. [Surgical Instrument Keypoint Estimation](#metrics-kp)
          3. [Surgical Instrument Instance Segmentation](#metrics-ins)


## Repository Structure

The structure of the repository is shown below, which you are welcome to change for your application in order to adapt it to your requirements.
Keep in mind that the `my_code` and `my_model` directories are copied to the `/phakir` directory in the container. If you change the directory structure, please adjust the `Dockerfile` accordingly.

```bash
PhaKIR_Submission_Template
├─── README.md
├─── Dockerfile          # Dockerfile to create the Docker image
├─── docker-compose.yml  # Docker-compose file to simulate the evaluation environment
│
├─── inputs
│    ├─── Video_01
│    │    ├─── Frames
│    │    │   ├─── frame_000000.png
│    │    │   ├─── frame_000001.png
│    │    │   └─── ...
│    │    └─── Video_01_Cuts.csv
│    │
│    ├─── Video_02
│    │    ├─── Frames
│    │    └─── Video_02_Cuts.csv
│    │
│    └───...
│   
├─── outputs
│    ├─── Video_01
│    └─── ...
│
├─── my_code
│    │   # Your code goes here
│    │   # You can add additional directories and files as needed
│    │   # this directory will be copied to the container (see Dockerfile)
│
└─── my_model
     │   # Your model goes here (e.g. weights, config, etc.)
     │   # You can add additional directories and files as needed
     │   # this directory will be copied to the container (see Dockerfile)
```



## Data

In the following, the structure of the data as well as the desired output format for each of the three tasks are specified.

### Structure

The data for this challenge is organized in a specific manner, please note the [Data Descriptions and Labeling Instructions](https://phakir.re-mic.de/wp-content/uploads/2024/07/PhaKIR_Data_Description_and_Labeling_Instructions_v2.pdf). You will find the data mounted in the `inputs` directory. The results of your processing should be written to the `outputs` directory.

In the **submission phase**, the video data is already split into frames and available in the `/Frames` directory. In addition, the video cuts are provided.
The data is organized as follows:

```bash
inputs
│
├─── Video_01
│    ├─── Frames
│    │    ├─── frame_000000.png
│    │    ├─── frame_000001.png
│    │    └─── ...
│    └─── Video_01_Cuts.csv
│
├─── Video_02
│    ├─── Frames
│    │    ├─── frame_000000.png
│    │    ├─── frame_000001.png
│    │    └─── ...
│    └─── Video_02_Cuts.csv
```

You have to process each video in the `inputs/data` directory and write the results to the `outputs` directory. The results have to meet the requirements of the specific task.

### Outputs

Whether you participate in one, two or all tasks, you have to ensure, that your results are written in the output directory in the correct structure.
The output structure for each task is provided below.
For example, if you participate in the two tasks Surgical Procedure Phase Recognition and Surgical Instrument Keypoint Estimation, make sure that for Video `XX`, both files `Video_XX_Phases.csv` and `Video_XX_Keypoints.json` are available in the `outputs` directory. **Note:** The format of your results must be identical to the format of the ground truth of the training data provided.

#### Surgical Procedure Phase Recognition

If you participate in this task, please provide the phase information for every frame.
Details can be found in the [Data Description and Labeling Instructions](https://phakir.re-mic.de/wp-content/uploads/2024/07/PhaKIR_Data_Description_and_Labeling_Instructions_v2.pdf).
Compare the format of your results with the format of the provided ground truth from the training data.

```bash
outputs
│
├─── Video_01
│    └─── Video_01_Phases.csv
│
└─── Video_02
     └─── Video_02_Phases.csv
```

#### Surgical Instrument Keypoint Estimation

If you participate in this task, please provide the keypoints for every 25th frame in the required encoding.
Details can be found in the [Data Description and Labeling Instructions](https://phakir.re-mic.de/wp-content/uploads/2024/07/PhaKIR_Data_Description_and_Labeling_Instructions_v2.pdf).
Compare the format of your results with the format of the provided ground truth from the training data.

```bash
outputs
│
├─── Video_01
│    └─── Video_01_Keypoints.json
│
└─── Video_02
     └─── Video_02_Keypoints.json
```

#### Surgical Instrument Instance Segmentation

If you participate in this task, please provide every 25th mask in the required encoding for each frame.
Details can be found in the [Data Description and Labeling Instructions](https://phakir.re-mic.de/wp-content/uploads/2024/07/PhaKIR_Data_Description_and_Labeling_Instructions_v2.pdf).
Compare the format of your results with the format of the provided ground truth from the training data.

```bash
outputs
│
├───Video_01
│   └─── Video_01_Masks
│        ├─── 0
│        │    ├─── frame_000000.png
│        │    ├─── frame_000025.png
│        │    ├─── frame_000050.png
│        │    └─── ...
│        │ 
│        ├─── 1000
│        │    ├─── frame_001000.png
│        │    ├─── frame_001025.png
│        │    └─── ...
│
├───Video_02
│   └─── Video_02_Masks
│        ├─── 0
│        │    ├─── frame_000000.png
│        │    ├─── frame_000025.png
│        │    ├─── frame_000050.png
│        │    └─── ...
│        │ 
│        ├─── 1000
│        │    └─── ...
```

## Docker

You are required to provide a Docker image for submission. A container created out of this image is used to process the provided data. Your Docker container should be configured to read data from the `inputs` directory and write the results to the `outputs` directory.

### Image

To create a Docker image, you can use the provided `Dockerfile`. The given `Dockerfile` is configured to install the necessary dependencies and copy the contents of your project (code and model, `my_code/` and `my_model/` folders, respectively) to the `/phakir` directory in the container. You can modify the `Dockerfile` to suit your requirements.

### Testing and Constraints

A `docker-compose.yml` file is provided to simulate the evaluation environment, including resource limitations. Please ensure your solution works within these constraints.
The constraints are as follows:

- Shared memory size (`shm_size`): 40G
- :zap: Network mode: none &rarr; the container **will not** have network access, so be sure that all dependencies are added / copied during [image creation](#image). This prohibits downloading any additional weights or models.
- Memory limit: 32G
- GPU access: Yes &rarr; the container will have access to an NVIDIA RTX 3090 with 24G VRAM

| :zap:        Note: This limitations are only for the evaluation environment.
|-----------------------------------------|

As the training process is performed locally at your research facilities, you are free to use whatever you like to train the models. You are only required to use the provided `docker-compose.yml` file with the given restrictions to verify that your submission is conformant to the PhaKIR Challenge environment.

Note that the container must be able to process the data without any further input. The container must be able to process the data from the `inputs` directory and write the results to the `outputs` directory.

For testing just use the following command:

```bash
docker-compose up --build
```

You may only submit **one** Docker image. If you wish to participate in multiple tasks, you must submit a single Docker image that can handle these tasks and generate the appropriate files for each task.

| :zap:        It is your own responsibility to ensure that the Docker container works as expected.   |
|-----------------------------------------|

## Submission

You can create your Docker Image using the provided `Dockerfile` or by providing a pre-built image. 
Make sure your Docker container is properly configured to read from the `inputs` directory and write to the `outputs` directory.

Check the participation part of the PhaKIR website (https://phakir.re-mic.de/participation) for further details.

## Evaluation

Your submission will be evaluated according to a variety of metrics listed below, depending on the tasks submitted. Please ensure your solution works within the [resource constraints](#testing-and-constraints) defined in the `docker-compose.yml` file.

### Metrics

For the tasks `Surgical Instrument Keypoint Estimation` and `Surgical Instrument Instance Segmentation`, we calculate the metrics mentioned below for each class in a frame, and average the results across all classes to get a final result for the single frame. 
We carry out this procedure for all images in a video to get a per-video result and average the results over all videos in the test dataset.
For the `Surgical Procedure Phase Recognition` task, we additionally average the per-phase results over all phases in a video to ensure that an unbalanced number of frames between phases does not affect the overall result. Since our challenge consists of three different tasks, and participants do not necessarily have to take part in all tasks, we carry out a separate evaluation and obtain three result lists at the end. For each task, we calculate all below mentioned metrics and average the corresponding ranks in order to determine the final task-specific rank.

<h4 id="metrics-phase">Surgical Procedure Phase Recognition</h4>

The classification of the surgical phases is evaluated using the `Balanced Accuracy (BA)` as the multi-class counting metric, the `F1-score` as the harmonic mean of precision of recall as the per-class counting metric, and the `Area under the Receiver Operating Characteristic Curve (AUROC)` as the threshold-based metric.

<h4 id="metrics-kp">Surgical Instrument Keypoint Estimation</h4>

The evaluation of the `Keypoint Accuracy` is analogous to the calculation of the `COCO mAP`, whereby the `Object Keypoint Similarity (OKS)` is used instead of the mIoU [4]. The `OKS` is calculated using the Euclidean distance between a predicted and a ground truth point, which is passed through an unnormalized Gaussian distribution where the standard deviation corresponds to the square root of the size of the segmentation area multiplied by a per-keypoint constant. We use the tuned version of the `OKS` proposed by COCO, which is based on a per-keypoint standard deviation with respect to the object scale and an adjusted constant. A more detailed description of OKS and the tuned version is given in [4].

<h4 id="metrics-ins">Surgical Instrument Instance Segmentation</h4>

For the instance segmentation of the surgical instruments, three metrics are employed. For localization, the `mean Average Precision (mAP)` is applied, whereby the `Mask Intersection over Union (IoU)` is used as the localization criterion. The calculation of the `mAP` is analogous to that of the Common Objects in Context (COCO) dataset [2], i.e., the `mAP` is computed for `IoU` thresholds between 0.50 and 0.95 with an interval of 0.05 and the results are averaged for the final `mAP` [3]. As a per-class counting metric, the `F1-score` is applied, and the `95% Hausdorff-Distance (HD)` serves as the boundary-based metric. For the assignment strategy of predictions to ground truth segmentations, the `Hungarian Maximum Matching Algorithm` is utilized.

[1] A. P. Twinanda, S. Shehata, D. Mutter, J. Marescaux, M. de Mathelin, and N. Padoy, “EndoNet: A Deep Architecture for Recognition Tasks on Laparoscopic Videos”, in IEEE Transactions on Medical Imaging, vol. 36, no. 1, pp. 86-97, 2017, doi: https://doi.org/10.1109/TMI.2016.2593957. 

[2] T. Lin, M. Maire, S. Belongie, J. Hays, P. Perona, D. Ramanan, P. Dollár and C. L. Zitnick. “Microsoft COCO: Common Objects in Context”, in European Conference on Computer Vision,  vol. 8693, 2014, doi: https://doi.org/10.1007/978-3-319-10602-1_48. 

[3]: Common Objects in Context – Detection Evaluation. https://cocodataset.org/detection-eval. Accessed: 14 November 2023.

[4]: Common Objects in Context – Keypoint Evaluation. https://cocodataset.org/keypoints-eval. Accessed: 14 November 2023.

Check the [PhaKIR - Challenge: **Pha**se, **K**eypoint and **I**nstrument **R**ecognition](https://phakir.re-mic.de/) for new updates.

Have Fun and Good Luck! :rocket:
