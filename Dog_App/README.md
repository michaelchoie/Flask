Process:

Gathering Data:
Used BeautifulSoup to parse HTML page and retrieve list of 190 most popular dog breeds
Used google_images_download API to scrape google images for pictures of these dogs

Prepping Data:
With the API, all the data is stored in a downloads folder and in a directory based on the string used to search for the images.
I added "dog" to each breed name to make sure i only got pictures of dogs as some breed names can be ambiguous (such as Pointer)
I then cleaned the names of the breed directors to remove dog and replaced white space with underscore because otherwise there are errors with certain packages I use for modeling
I cleaned the files so that only .jpg, .jpeg, and .png remained and removed white space
Finally, I partitioned the images into train/valid/test directories

Creating Model:
I used the Resnet50 CNN to conduct transfer learning and train my model to recognize the dog breeds in my dataset

[TODO]

Productionalizing Model:
Used a Flask app to create a simple UI to service my ML predictions

Data Storage:
I store the results of my predictions to get an idea of how well my app is doing in production in a SQLite database



