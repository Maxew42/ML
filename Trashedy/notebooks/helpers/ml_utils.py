import numpy as np
import matplotlib.pyplot as plt
import json
import torch.nn.functional as func
from PIL import Image
from torch.utils.data import DataLoader, Dataset
import torch
import os
import pandas as pd

class ObjectDetectionDataset(Dataset):
    """
    Custom PyTorch Dataset Class to facilitate loading data for the Object Detection Task
    """
    def __init__(self, 
                 path_to_dataset,  
                 mapping = None, 
                 mode = 'train', 
                 transform = None,refactor_some_classes = True): 
        """ 
        Args:
            annotations: The path to the annotations CSV file. Format: file_name, classes, xmin, ymin, xmax, ymax
            train_test_valid_split: The path to the tags CSV file for train, test, valid split. Format: file_name, tag
            mapping: a dictionary containing mapping of class name and class index. Format : {'class_name' : 'class_index'}, Default: None
            mode: Mode in which to instantiate class. Default: 'train'
            transform: The transforms to be applied to the image data

        Returns:
            image : Torch Tensor, target: Torch Tensor, file_name : str
        """
        self.mapping = mapping
        self.transform = transform
        self.mode = mode

        self.path_to_images = path_to_dataset
        # Loading the annotation file (same format as Remo's)
        
        #my_data = pd.read_csv(annotations)
        
        # Here we append the file path to the filename. 
        # If dataset.export_annotations_to_file was used to create the annotation file, it would feature by default image file paths
        
        #my_data['file_name'] = my_data['file_name'].apply(lambda x : os.path.abspath(f'{self.path_to_images}{x}'))
        #my_data = my_data.set_index('file_name')
        
        annotations_file_path = os.path.join(path_to_dataset, 'annotations.json')
        data = read_file(annotations_file_path)
        my_data  = extractDataSetFromCOCO(data,path_to_dataset)
        if refactor_some_classes:
            my_data.loc[(my_data['classes'] == 'eps-polystyrene-'),'classes']='other'
            #my_data[my_data['classes']=='eps-polystyrene-'] = 'other'
        my_data['file_name'] = path_to_dataset +  my_data['file_name']
        # Loading the train/test split file (same format as Remo's)
        #my_data['tag'] = pd.read_csv(train_test_valid_split, index_col='file_name')
        
        #my_data = my_data.reset_index()
        # Load only Train/Test/Split depending on the mode
        #my_data = my_data.loc[my_data['tag'] == mode].reset_index(drop=True)
        self.data = my_data

        self.file_names = self.data['file_name'].unique()

    def __len__(self) -> int:
        return self.file_names.shape[0]

    def __getitem__(self, index: int):

        file_name = self.file_names[index]
        records = self.data[self.data['file_name'] == file_name].reset_index()       
        image = np.array(Image.open(file_name), dtype=np.float32)
        image /= 255.0

        if self.transform:
            image = self.transform(image)  

        # here we are assuming we don't have labels for the test set
        if self.mode != 'test':
            boxes = records[['xmin', 'ymin', 'xmax', 'ymax']].values
            area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
            area = torch.as_tensor(area, dtype=torch.float32)

            if self.mapping is not None:
                labels = np.zeros((records.shape[0],))

                for i in range(records.shape[0]):
                    labels[i] = self.mapping[records.loc[i, 'classes']]

                labels = torch.as_tensor(labels, dtype=torch.int64)

            else:
                labels = torch.ones((records.shape[0],), dtype=torch.int64)

            iscrowd = torch.zeros((records.shape[0],), dtype=torch.int64)

            target = {}
            target['boxes'] = boxes
            target['labels'] = labels
            target['image_id'] = torch.tensor([index])
            target['area'] = area
            target['iscrowd'] = iscrowd 
            target['boxes'] = torch.stack(list((map(torch.tensor, target['boxes'])))).type(torch.float32)

            return image, target, file_name
        else:
            return image, file_name

def collate_fn(batch):
    return tuple(zip(*batch))

def read_file(path_to_file):
    # Read annotations
    with open(path_to_file, 'r') as f:
        dataset = json.loads(f.read())
    return dataset

def extractDataSetFromCOCO(dataset,imagePath):
    """ 
    Args:
        dataset : a parsed JSON file countaining the annotations, must be COCO format.
        imagePath : Path to a file with all the dataSet images.
    Returns:
        df : A pandas dataFrame with the annotations and the image file name
    """
    df = pd.DataFrame()
    categories = [row['name'] for row in dataset['categories']]
    images = [row['file_name'] for row in dataset['images']]
    df['classes'] = [row['category_id'] for row in dataset['annotations']]
    df['file_name'] = [row['image_id'] for row in dataset['annotations']]
    df['file_name'] = [images[i] for i in df['file_name']]
    df['classes'] = [categories[i] for i in df['classes']]
    ## A DELETE ALED
    #df['image'] = [ img_to_array(load_img(imagePath + '/' + fil, target_size=(224, 224))) for fil in df['file_name']] #Très sale, à voir pour faire mieux
    
    df['xmin'] = [row['bbox'][0] for row in dataset['annotations']]
    df['ymin'] = [row['bbox'][1] for row in dataset['annotations']]
    df['xmax'] = [row['bbox'][0]+row['bbox'][2] for row in dataset['annotations']]
    df['ymax'] = [row['bbox'][1]+row['bbox'][3] for row in dataset['annotations']]
    return df

def evaluate(data_loader,device,cat_to_index): 
    """ 
    Args:
        data_loader : A Pytorch dataloader with the images we want to perform detection on.
        device : A Pytorch device, CPU or GPU.
        cat_to_index : A dictionnary linking labels to a int.
    Returns:
        results : List of dictionnary with the bounding boxes, the labels and the scores. It can be easely saved as csv or json.
    """
    mapping = { value : key for (key, value) in cat_to_index.items()}
    detection_threshold = 0.3
    results = []
    model.eval()
    data_loader = tqdm.tqdm(data_loader)

    with torch.no_grad():
        for images, image_ids in data_loader:

            images = list(image.to(device) for image in images)
            outputs = model(images)
            for i, image in enumerate(images):

                boxes = outputs[i]['boxes'].data.cpu().numpy()
                scores = outputs[i]['scores'].data.cpu().numpy()
                boxes = boxes[scores >= detection_threshold].astype(np.int32)
                scores = scores[scores >= detection_threshold]
                image_id = image_ids[i]

                for box, labels,score in zip(boxes, outputs[i]['labels'],scores):
                    results.append({'file_name' : os.path.basename(image_id), 
                                    'classes'   : mapping[labels.item()], 
                                    'xmin'      : box[0],
                                    'ymin'      : box[1],
                                    'xmax'      : box[2],
                                    'ymax'      : box[3],
                                    'scores'    : score})
    return results

