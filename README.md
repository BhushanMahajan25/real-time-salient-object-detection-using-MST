# Real-Time Salient Object Detection with a Minimum Spanning Tree

## Why did you choose this project?
  - The goal of salient object detection is to identify most important objects in a scene. There are mainly two exisiting methods to detect a salient object:
    - Supervised learning with high level of imformation.
    - Classic image processing techniques based on low-level features such as color, gradient or contrast. 
  - The reason to choose this project was to explore and implement the novel approach to detect salient objects by representing an image into Minimum Spanning Tree (MST) as, MST inherently reveals the object geometry information in a scene.
  - This project implements core algorithm as proposed in the paper ___"Real-Time Salient Object Detection with a Minimum Spanning Tree"___ authored by _Tu, Wei Chih and He, Shengfeng and Yang, Qingxiong and Chien, Shao Yi_. More details about this paper can be found here. <!-- <link of the paper> -->

## What is the problem?
  - Because background areas are usually related to image borders, prominent objects can be recovered by calculating the distances between them. However, efficiently assessing picture border connectivity is a difficult task.
  - To decrease processing units, existing techniques either use superpixel representation or estimate the distance transform.
  - Most of the methodologies for salient object detection use bottom-up approach i.e., classic low-level image processing techniques due their task-free nature and efficient computation over top-down approach i.e., supervised learning.
  - Furthermore, many existing methodologies utilize shortest-path geodesic distance towards the background region which limits the efficient saliency computation.
  - However, (Y. Qin et al <!--link-->) proposes new method of saliency optimization based on Cellular Automata by leverage the background prior to compute a global color distinction map as well as a spatial distance map. However, the over-segmentation stage is often a processing barrier, preventing these approaches from being used in real-time applications.

## How are you solving it?
  - The paper puts emphasis on usage of minimum barrier distance instead of geodesic distance.
  - Instead of computing distance on image the paper calculates distance between pixels on a minimum spanning tree.
  - This tree representation of an image helps to largely reduces the search space of shortest paths, resulting an efficient and high quality distance transform algorithm. And hence allows the distance measure on a tree able to distinguish important objects in a scene.
  - In the end the paper implements a boundary dissimilarity measure to compliment the shortage of distance transform for salient object detection. 

## Project Description
### What does your code do (file descripiton, flows, and in general idea of how the code works)?
  - The very first step is to take user input from command-line menu in which user selects an image for salient object detection. The image is then read using cv2's imread function.
  - The image is converted into a standard 4-connected, undirected planar graph with nodes being all image pixels and the edges between adjacent pixels being weighted by color differences.
  - A weight between two adjacent pixels $s$ and $r$ can be computed by the below formula:
    >$w(s, r) = w(r, s) = |I(s) − I(r)|$
  - A minimum spanning tree is constructed based on approach specified by (Bao et al.<!--link-->) which uses `Prim's Algorithm` with time complexity of $O(n)$.
  - The shortest path on MST is then calculated which consists of two passes:
      1. Bottom-up traversal:
         - The distance values from child nodes to parent nodes, starting from leaf nodes untils root node is visited, are updated by implementing *Breadth First Serach* with the formula:
            >  $D(p) = min(D(p), f(\pi_v \cup p))$
            >
            > where $p$ denotes the parent node of $v$, $\pi_v$ denotes the current optimal path connecting $v$ to its nearest seed node and $\pi_v \cup p$ denotes the same path plus one step further to reach its parent $p$. 
      2. Top-down traversal :
        - The traversal starts from root of the tree and terminates when leaf node is visited. The distance values between parent-child nodes is updated using following formula:
          >  $D(v) = min(D(v), f(\pi_p \cup v))$
    - The bottom-up pass is computed first since a splitting node should store the ideal distance value from one of its branches after the bottom-up pass. The optimal solution will be transmitted down to other branches later in the top-down pass.
    - The overall time complexity till above step is in linear time.



## Project implementation details
### How to install dependencies : 
    python3 -m pip install -r requirements.txt

### How to run the code : 
    python3 src/main.py

- The program asks user to select the image for salient object detection from menu. After the choice is given by user, prgram start detecting the salient object the input image.

### Libraries used
- `cv2`==4.5.5: To perform read and write operations on images.
- `numpy`==1.22.3: To effectively deal with 2d and 3d matrices.


### Development environment
- System: Apple Macbook Air (Apple Silicon-M1)
- Programming language: Python==3.9.8
- Text editor: MS-VS Code
- Time execution: 

### Project directories
- input_images <!--link-->: Directory of input images. User sees these input images on command line menu.
- results <!--link-->: Directory in which final synthesized image is stored.
- src <!--link-->: Directory containing python source code.
- requrements.txt <!--link-->: File containing dependencies required for the file

### How to interpret the output : 
The output image will be generated inside `results` directory.

## Results








