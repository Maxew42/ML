import matplotlib.pyplot as plt
import random
random.seed(4)
import numpy as np

def convert_points_to_box(points, color = 'red', alpha = 0.09):
    '''
        Helper Function : return two pyplot.Rectangle for the purpous of plotting bboxes. One is the border and one is the fill color.
    '''
    upper_left_point = (points[0], points[1])
    width = points[2] - points[0]
    height = points[3] - points[1]
    return (plt.Rectangle(upper_left_point, width, height, ec=color,fc=color, alpha=1,facecolor='none',fill = False),plt.Rectangle(upper_left_point, width, height, ec=color,fc=color, alpha=alpha))

def show_bounding_boxes(img,l_boxes,l_scores = None,labels = None,fontsize = 16,color_map = None ):
    '''
        Show the bounding boxes in l_boxes for a specified image img in np.array format. 
    '''
    fig = plt.figure(figsize=(25, 10))
    colors = ['red','blue']
    ax = plt.gca()
    colors_idx = [random.randint(0, len(colors)-1) for i in l_boxes]
    plt.imshow(img)
    for i,box in enumerate(l_boxes):
        if color_map and labels:
            contour,texture = convert_points_to_box(box, color_map[labels[i]], 0.1)
        else : 
            contour,texture = convert_points_to_box(box, colors[colors_idx[i]], 0.1)
        ax.add_patch(contour)
        ax.add_patch(texture)
        if labels and l_scores:
            if color_map:
                plt.text(box[0] -2,box[1]-6,labels[i] + " : "+ str(np.round_(100*l_scores[i], decimals=2))+ " %",fontsize=fontsize,color = color_map[labels[i]] )

            else:
                plt.text(box[0] -2,box[1]-6,labels[i] + " : "+ str(np.round_(100*l_scores[i], decimals=2))+ " %",fontsize=fontsize,color = colors[colors_idx[i]] )

    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    plt.show()
    
def show_result(results,path_to_dataset,file_name,color_map = None):
    '''
        Show the bounding boxes in l_boxes for a specified image img in np.array format. 
    '''
    img = plt.imread(path_to_dataset + "/" + file_name)
    l_boxes = []
    l_labels = []
    l_scores = []
    for row in results:
        if row['file_name'] == file_name:
            l_boxes.append([row['xmin'],row['ymin'],row['xmax'],row['ymax']])
            l_labels.append(row['classes'])
            l_scores.append(row['scores'])
    print("Nombre de déchets identifiés : ", len(l_boxes))
    show_bounding_boxes(img,l_boxes,l_scores = l_scores,labels = l_labels,color_map=color_map)

def moving_average(x, w):
    '''
        Helper function that computes the moving average on np.array or list x with period w 
    '''
    return np.convolve(x, np.ones(w), 'valid') / w

def plot_loss_summary(l_losses,len_dataset,num_epochs):
    '''
        Plot a summary of the evolution of losses during training for the fasterRCNN model.
    '''
    plt.figure(figsize=(12, 6))
    ax1 = plt.subplot(2,4,1)
    ax2 = plt.subplot(2,4,2)
    ax3 = plt.subplot(2,4,3)
    ax4 = plt.subplot(2,4,4)
    ax5 = plt.subplot(2,1,2)

    ax1.set_title("Loss classifier")
    ax2.set_title("Loss box reg")
    ax3.set_title("Loss objectness")
    ax4.set_title("Loss rpn box reg")
    ax5.set_title("Total Loss")
    
    if num_epochs != 1: 
        ax1.plot(moving_average(l_losses['loss_classifier'],len_dataset))
        ax2.plot(moving_average(l_losses['loss_box_reg'],len_dataset))
        ax3.plot(moving_average(l_losses['loss_objectness'],len_dataset))
        ax4.plot(moving_average(l_losses['loss_rpn_box_reg'],len_dataset))
        ax5.plot(moving_average(np.array(l_losses['loss_classifier'])+np.array(l_losses['loss_box_reg'])+ np.array(l_losses['loss_rpn_box_reg']) + np.array(l_losses['loss_objectness']),len_dataset))
    else : 
        ax1.plot(l_losses['loss_classifier'])
        ax2.plot(l_losses['loss_box_reg'])
        ax3.plot(l_losses['loss_objectness'])
        ax4.plot(l_losses['loss_rpn_box_reg'])
        ax5.plot(np.array(l_losses['loss_classifier'])+np.array(l_losses['loss_box_reg'])+ np.array(l_losses['loss_rpn_box_reg']) + np.array(l_losses['loss_objectness']))
