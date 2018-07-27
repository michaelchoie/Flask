## Process:

### Gathering Data:
- Used BeautifulSoup to parse an HTML page containing a list of the 190 most popular dog breeds
- Used google_images_download API to scrape the web for pictures of these dogs

### Prepping Data:
- Some of the images that are downloaded were corrupted
    - Identified problem files using exception handling and removed
- Cleaned the files so that only .jpg, .jpeg, and .png remained and removed white space
- Some png files were transparent, which doesn't work well with ML libraries
    - Converted these files into jpg
- Fixed the names of the directories containing the dog images
    - Each dog breed has its own directory
    - The name of the dirs are the search string I used with the API
        - I added "dog" to each breed name as some breed names can be ambiguous (such as Pointer)
    - Replaced white space with underscore because otherwise there are errors with certain packages I use for modeling
- Partitioned the breed directories into train/valid/test directories

### Creating Model:
I used the Resnet50 CNN to conduct transfer learning and trained my model to recognize the dog breeds in my dataset. This means that we are using the trained weights for the parameters of its hidden layers prior to the final fully connected layers so that we have the benefit of utilizing the previous layers' ability to detect general things like lines, shapes, etc

The CNN architecture works well for image recognition because it retains spatial information while also accounting for processing time and in-memory storage.

Each of our convolutional layers use the "elu" activation function as these are fast, account for vanishing gradients, and resolve the issue of ReLU not returning a mean activation function of 0. For every convolutional layer added, we add a pooling layer to reduce the dimensions of each of the filter maps (pool_size = 2 means that we are reducing height and width by 50%), which increases processing speed and decreases the amount of data we must hold in memory. We also add in batch normalization layers to mitigate problems from internal covariate shifts. For the purposes of performing a quick classification on the data, we add a global average pooling layer to reduce the dimensionality even more prior to the fully connected layers to increase the speed at which we can process the images. We finally add in a fully connected layer with a softmax function to return probabilities of dog breed.

### Training Model:
I noticed that the train time on my mac was extremely slow - one epoch would take over an hour.
However, my accuracy rate on the test set after only one epoch was ~35%, which showcases how well the transfer learning model does straight out of the box.

Decided to instantiate an AWS EC2 cluster and ssh into it to parallelize my training process.
Afterwards I transferred my completed model from the cluster to my local using SCP (secure copy)

Choose an AMI (Amazon Machine Image) which defines the OS of the instance and contains the environment files/drivers needed to train on a GPU

EC2 - p2.xlarge instances for GPU instances [GPU Compute]

Will receieve an authentication key pair

ssh -i YourKeyName.pem ubuntu@X.X.X.X
X.X.X.X = ipv4 public ip

Used vim in order to edit files in SSH

### Productionalizing Model:
Used a Flask app to create a simple UI to service my ML predictions

### Data Storage:
I store the results of my predictions to get an idea of how well my app is doing in production in a SQLite database

### Front End:
Utilized HTML, CSS, Javascript, Bootstrap to make the website more user friendly

