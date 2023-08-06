import json
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import math
import matplotlib.gridspec as gridspec
from collections import Counter

class analysis:

    #init
    def __init__(self,Dir):

        self.dir = Dir
        #validate dir is a string and ends with a slash
        if not isinstance(self.dir, str):
            raise TypeError("dir must be a string")
        if not self.dir.endswith("/"):
            raise ValueError("dir must end with a slash")

    # THIS FUNCTION WILL GENERATE A HEATMAP FOR EACH CATEGORY IN THE DATASET SHOWING THE DISTRIBUTION OF OBJECTS IN THE IMAGE FRAME.

    #performs spatial analysis on a dataset containing bounding box annotations of objects. 
    #The goal is to create heatmaps representing the distribution of object centers across 
    # different categories within the dataset.

    def spatial_analysis(self):
        # Load JSON data
        with open(self.dir + 'coco_annotations.json') as f:
            data = json.load(f)

        # Prepare a map from category_id to category_name and initialize storage for object centers
        id_to_category = {category["id"]: category["name"] for category in data["categories"]}
        object_centers = defaultdict(list)  # This will create a new list for a key if it doesn't exist

        # Compute the center of each bounding box
        for annotation in data["annotations"]:
            bbox = annotation['bbox']
            center = [(bbox[0] + bbox[2] / 2), (bbox[1] + bbox[3] / 2)]  # normalized x and y centers
            category = id_to_category[annotation["category_id"]]
            object_centers[category].append(center)

        # Compute the number of categories
        num_categories = len(object_centers)

        # Create a new figure with a subplot for each category
        fig = plt.figure(figsize=(10, num_categories*5))

        # Create a gridspec for layout control
        gs = gridspec.GridSpec(num_categories, 2, width_ratios=[20, 1])

        # Create a heat map for each category
        for i, (category, centers) in enumerate(object_centers.items()):
            heatmap, xedges, yedges = np.histogram2d(*zip(*centers), bins=50)  # adjust bins for different resolution
            extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

            # Plot the heat map
            ax = plt.subplot(gs[i, 0])
            im = ax.imshow(heatmap.T, extent=extent, origin='lower', cmap='hot')
            ax.set_title(category)

            # Add a colorbar for this heatmap in the second column of the grid
            cbax = plt.subplot(gs[i, 1])
            plt.colorbar(im, cax=cbax)

        plt.tight_layout()
        plt.savefig('heatmaps.png', bbox_inches='tight')  # Save the plot as a PNG file


        #analyzes a dataset containing object annotations and generates a bar plot 
        # representing the distribution of different classes (categories) present in the dataset. 

    def class_distribution(self):

        def get_class_distribution(json_file):
            # Load JSON data
            with open(json_file) as f:
                data = json.load(f)

            # Extract categories from the data
            id_to_category = {category["id"]: category["name"] for category in data["categories"]}

            # Count the occurrences of each category in the annotations
            counter = Counter(annotation["category_id"] for annotation in data["annotations"])

            # Convert category ids to names and count
            class_distribution = {id_to_category[id]: count for id, count in counter.items()}

            return class_distribution

        def plot_class_distribution(class_distribution, output_file):
            # Prepare data for plotting
            classes = list(class_distribution.keys())
            counts = list(class_distribution.values())

            # Create bar plot
            plt.figure(figsize=(10, 6))
            plt.barh(classes, counts, color='skyblue')
            plt.xlabel("Count")
            plt.ylabel("Classes")
            plt.title("Class Distribution")
            plt.tight_layout()

            # Save the plot as a PNG file
            plt.savefig(output_file)

        json_file = self.dir + "coco_annotations.json"
        output_file = "class_distribution.png"

        distribution = get_class_distribution(json_file)
        plot_class_distribution(distribution, output_file)


    #performs relative size analysis on a dataset containing object annotations 
    # with bounding box information. The goal is to analyze the relative size 
    # of objects within each category and visualize the distribution of relative 
    # sizes using histograms.

    def relative_scale(self):

        # Load JSON data
        with open(self.dir + 'coco_annotations.json') as f:
            data = json.load(f)

        # Prepare a dictionary to hold relative sizes per category
        relative_sizes = {category['id']: [] for category in data['categories']}

        # Iterate over annotations
        for annotation in data['annotations']:
            # Get bounding box dimensions
            box_width = annotation['bbox'][2]
            box_height = annotation['bbox'][3]

            # Get image dimensions
            for image in data['images']:
                if image['id'] == annotation['image_id']:
                    img_width = image['width']
                    img_height = image['height']
                    break

            # Compute relative size and add it to the list
            relative_sizes[annotation['category_id']].append((box_width * box_height) / (img_width * img_height))

        # Compute the layout for the subplots (as a square grid, or as close to a square as possible)
        num_categories = len(data['categories'])
        grid_size = math.ceil(math.sqrt(num_categories))
        fig, axs = plt.subplots(grid_size, grid_size, figsize=(15, 15))

        # Plot a histogram of relative sizes for each category
        for i, category in enumerate(data['categories']):
            row = i // grid_size
            col = i % grid_size
            axs[row, col].hist(relative_sizes[category['id']], bins=50)
            axs[row, col].set_title(category["name"])

        # Remove any unused subplots
        for j in range(i+1, grid_size*grid_size):
            fig.delaxes(axs.flatten()[j])

        plt.tight_layout()
        plt.savefig('relative_sizes.png', bbox_inches='tight')  # Save the plot as a PNG file


    #analyzes a dataset containing object annotations with bounding box information. 
    # The goal is to compute the areas of bounding boxes for each object category and 
    # visualize the distribution of these areas using histograms.

    def bounding_box_areas(self):
            
        # Load JSON data
        with open(self.dir + 'coco_annotations.json') as f:
            data = json.load(f)

        # Prepare a map from category_id to category_name and initialize storage for bbox areas
        id_to_category = {category["id"]: category["name"] for category in data["categories"]}
        bbox_areas = defaultdict(list)  # This will create a new list for a key if it doesn't exist

        # Compute bounding box areas
        for annotation in data["annotations"]:
            bbox = annotation['bbox']
            bbox_area = bbox[2] * bbox[3]  # width * height
            category = id_to_category[annotation["category_id"]]
            bbox_areas[category].append(bbox_area)

        # Create histogram
        num_categories = len(bbox_areas)
        fig, axs = plt.subplots(num_categories, 1, figsize=(10, 6 * num_categories))  # Create a subplot for each category

        # Create histogram for each category
        for (category, areas), ax in zip(bbox_areas.items(), axs.flatten()):
            if areas:  # Check if areas list is not empty
                ax.hist(areas, bins=np.linspace(0, max(areas), 50), color='blue', alpha=0.5)
                ax.set_title(category)
                ax.set_xlabel("Area")
                ax.set_ylabel("Frequency")

        fig.tight_layout()  # Adjusts subplot params so that subplots are nicely fit in the figure area
        plt.savefig('bbox_areas.png', bbox_inches='tight')  # Save the plot as a PNG file


    #performs aspect ratio analysis on a dataset containing object annotations with bounding box information. 
    # The goal is to calculate the aspect ratio of bounding boxes for each object category and visualize 
    # the distribution of these aspect ratios using histograms.

    def aspect_ratio_distribution(self):
            
        # Load JSON data
        with open(self.dir + 'coco_annotations.json') as f:
            data = json.load(f)

        # Prepare a map from category_id to category_name and initialize storage for annotations
        id_to_category = {category["id"]: category["name"] for category in data["categories"]}
        annotations = defaultdict(list)

        # Group annotations by category
        for annotation in data["annotations"]:
            category = id_to_category[annotation["category_id"]]
            annotations[category].append(annotation)

        # Create a subplot for each category
        num_categories = len(annotations)
        fig, axs = plt.subplots(num_categories, 1, figsize=(10, num_categories*5))

        for ax, (category, category_annotations) in zip(axs, annotations.items()):
            # Prepare storage for aspect ratios
            aspect_ratios = []

            # Calculate aspect ratio for each bounding box
            for annotation in category_annotations:
                bbox = annotation['bbox']
                # Check for zero width or height to avoid division by zero
                if bbox[2] > 0 and bbox[3] > 0:
                    aspect_ratio = bbox[2] / bbox[3]  # assuming bbox format is [xmin, ymin, width, height]
                    aspect_ratios.append(aspect_ratio)

            # Create a histogram of the aspect ratios
            ax.hist(aspect_ratios, bins=50)
            ax.set_title(f'Distribution of Aspect Ratios for {category}')
            ax.set_xlabel('Aspect Ratio (width/height)')
            ax.set_ylabel('Frequency')

        plt.tight_layout()
        plt.savefig('aspect_ratio_distribution.png')
