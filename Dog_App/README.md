## Process:

### Gathering Data:
- Used BeautifulSoup to parse an HTML page containing a list of the 190 most popular dog breeds
- Used google_images_download API to scrape the web for pictures of these dogs

### Prepping Data:
- Some of the images that are downloaded were corrupted
    - Identified problem files using exception handling and removed
- Cleaned the files so that only .jpg and .jpeg remained and removed white space
    - Some png files were transparent, which doesn't work well with ML libraries
- Fixed the names of the directories containing the dog images
    - Each dog breed has its own directory
    - The name of the dirs are the search string I used with the API
        - I added "dog" to each breed name as some breed names can be ambiguous (such as Pointer)
    - Replaced white space with underscore because otherwise there are errors with certain packages I use for modeling
- Partitioned the breed directories into train/valid/test directories

### Creating Model:
I used the Resnet50 CNN to conduct transfer learning and trained my model to recognize the dog breeds in my dataset. This means that we are using the trained weights for the parameters of its hidden layers prior to the final fully connected layers so that we have the benefit of utilizing the previous layers' ability to detect general things like lines, shapes, etc

The CNN architecture works well for image recognition because it retains spatial information while also accounting for processing time and in-memory storage.

For the sake of time, I added a global average pooling layer to reduce the dimensions of each of the filter maps, which increases processing speed and decreases the amount of data we must hold in memory. I also added in a batch normalization layer to mitigate internal covariate shift.  Finally, I added in a fully connected layer with a softmax function to return probabilities of dog breed.

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
Used a Flask app to create a simple UI to service my ML predictions.
The default web servers provided by popular web frameworks like Django or Flask are optimized for development but perform poorly on production.
When interfacing with the real world, you must account for slow clients, scalability, asynchronous I/O, and other optimizations.
That is what Nginx and Gunicorn are for - making Python web apps production ready.

Backend has a 3 tier architecture:
    1) Nginx = outermost layer
    2) Gunicorn = middle layer
    3) Database/Python app that connects to DB = inner layer

I don't have a dedicated server so I used Vagrant and VirtualBox to emulate a server from my local.

nginx = server that accepts requests and forwards them to the application
    responsible for serving static content and HTTP stuff
    load balancer, cache, proxy, reverse proxy, etc.
gunicorn = production web server for Python applications
    Interfaces w/ nginx and python code to serve dynamic content
    
Typically, nginx will serve HTTP requests, but if the url is dynamic, nginx forwards the request to gunicorn (this way, slower clients can be served differently)

Gunicorn returns a response to nginx which in turn sends the response to the client

#### Data Storage:
I store the results of my predictions to get an idea of how well my app is doing in production in a MongoDB database (responses are stored as json)

### Front End:
Utilized HTML, CSS, Javascript, AJAX, Bootstrap to make the website more user friendly

