
import cv2
import torch

import numpy as np  
import torchvision.transforms as T  

from pathlib import Path
from matplotlib.colors import ListedColormap

# Load deeplab model from torchvision as dummy model
from torchvision.models.segmentation import deeplabv3_resnet101, DeepLabV3_ResNet101_Weights
import pandas as pd


cdict = {
    'background':            [  0,   0,   0],
    'argonbeamer':           [ 60,  50,  50],
    'clip_applicator':       [  0,   0, 255],
    'drainage':              [255,   0,   0],
    'grasper':               [255, 130,   0],
    'hf_coagulation_probe':  [255,   0, 153],
    'needle_probe':          [204, 153, 153],
    'palpation_probe':       [255, 102, 255],
    'pe_forceps':            [ 30, 144,   1],
    'scissor':               [255, 255,   0],
    'suction_rod':           [153,   0, 204],
    'trocar_tip':            [153, 102,   0],
}

cmap = ListedColormap(name="phakir", colors=[np.array(c)/255. for c in cdict.values()], N=len(cdict))


def get_transforms():
    '''
        Here you can define the transformations that will be applied to the frames 
        before feeding them to the model.

        Feel free to change the normalization values.
    '''
    return T.Compose([
        T.ToTensor(),
        T.Normalize(
                mean=[0.485, 0.456, 0.406], # imagenet normalization
                std=[0.229, 0.224, 0.225]) 
    ])

def load_model(device:torch.device=torch.device('cuda')) -> torch.nn.Module:
    '''
        Here you can initialize the model and load the weights.
        Feel free to change the model architecture or the weights.

        Parameters:
            device: Device to run the model on. Default is GPU.
    '''
    # The evaluation will be done offline.
    # You have to copy the model and the weights into your docker image.
    model = deeplabv3_resnet101(weights=None,weights_backbone=None)
    model.classifier[4] = torch.nn.Conv2d(256, 11, kernel_size=(1, 1), stride=(1, 1))
    model = model.to(device)
    model.eval()

    return model

def evaluate(video_path:Path='/input', output_path:Path='/output', 
             device:torch.device=torch.device('cuda')):
    '''
        This function will be called for each video folder in the input path.
        The default implementation will load the model, apply the transformations 
        to the frames and save the segmentation masks.

        Parameters:
            video_path: Path to the video folder containing the frames.
            output_path: Path where the segmentation masks will be saved.
            device: Device to run the model on. Default is GPU.
    '''

    # You can use the cut_frames_df DataFrame to perform various operations on the data
    # A cut defines a position where some frames were removed.
    cut_frames_df = pd.read_csv(f'{video_path}/{video_path.stem}_Cuts.csv')

    model      = load_model(device)
    transforms = get_transforms()

    num_subdirs = len(list(video_path.glob('*/')))
    frame_nr    = 0

    for subdir in range(num_subdirs):
        (output_path/f'{subdir*1000}').mkdir(parents=True, exist_ok=True)
        for _ in range(1000):
            # Get the frame name and path
            frame_name = f'frame_{frame_nr:06d}'
            frame_path = f'{video_path}/Frames/{subdir*1000}/{frame_name}.png'
            frame_nr += 1   

            if(not Path(frame_path).exists()):
                break
            # Read the frame and convert to RGB
            frame = cv2.imread(str(frame_path))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Apply transformations to the frame and move to device 
            frame_tensor = transforms(frame)
            frame_tensor = frame_tensor.unsqueeze(0)
            frame_tensor = frame_tensor.to(device)

            # Apply the model to the frame
            with torch.no_grad():
                output = model(frame_tensor)

            # Get the segmentation mask
            logits = output['out']
            prediction = torch.argmax(logits, dim=1).squeeze(0).cpu().numpy()
            prediction_c = (cmap(prediction)*255).astype(np.uint8)

            # Save the segmentation mask
            prediction_c = cv2.cvtColor(prediction_c, cv2.COLOR_RGBA2BGR)
            cv2.imwrite(f'{output_path}/{subdir*1000}/{frame_name}.png', prediction_c)



def main():
    # The input path should contain the frames of the videos
    # The output path will contain the task dependent outputs e.g. instance 
    # segmentation masks or phase detection results.
    # Default paths are /input and /output and should NOT be changed
    input_path  = Path('/phakir/inputs')
    output_path = Path('/phakir/outputs')

    # Use GPU if available
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    # Iterate over all video folders in the input path
    for video_path in input_path.glob('Video_*'):
        print(f'Processing {video_path} ...')
        evaluate(video_path, output_path, device)



# Run the main function
if __name__ == '__main__':
    main()


