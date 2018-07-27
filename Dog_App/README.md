## Process:

### Gathering Data:
- Used BeautifulSoup to parse an HTML page containing a list of the 190 most popular dog breeds
- Used google_images_download API to scrape the web for pictures of these dogs

### Prepping Data:
- Some of the images that are downloaded were corrupted
    - Identified problem files using exception/warning handling and removed
- Fixed the names of the directories containing the dog images
    - Each dog breed has its own directory
    - The name of the dirs are the search string I used with the API
        - I added "dog" to each breed name as some breed names can be ambiguous (such as Pointer)
    - Replaced white space with underscore because otherwise there are errors with certain packages I use for modeling
- Cleaned the files so that only .jpg, .jpeg, and .png remained and removed white space
- Partitioned the breed directories into train/valid/test directories

### Creating Model:
I used the Resnet50 CNN to conduct transfer learning and train my model to recognize the dog breeds in my dataset

[TODO]

### Productionalizing Model:
Used a Flask app to create a simple UI to service my ML predictions

### Data Storage:
I store the results of my predictions to get an idea of how well my app is doing in production in a SQLite database



