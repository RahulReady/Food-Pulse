# Food-Pulse

**Goal:** Obtain a real time analysis for the top food items (via Google reviews) of a particular restaurant. <br><br>
**"The Investor Pitch":** <br>https://docs.google.com/presentation/d/1zmt0hzcZGN_2xa4g52mCSlGNywuGCue9xSln1kV3Xp8/edit

Check out our finished project (includes a video tutorial) ! <br>https://chrome.google.com/webstore/detail/food-pulse/jnaadlondamcfedkbhlkpojimipbclbo?hl=en&authuser=0

**Version 1.1** <br>

## Navigating this madness

<ul>
    <li><b>DataScience</b></li><ul>
        <li><b>output_dir</b>: Trained Spacy model. </li>
        <li><b>scrapped_restaurant_reviews</b>: contains a scraped restaurant json file for local testing (intentionally misspelled). </li>
        <li><b>NER_CRF.ipynb</b>: Attempt at using Conditional Random Fields for NER. Shout out to <a href="https://towardsdatascience.com/named-entity-recognition-and-classification-with-scikit-learn-f05372f07ba2">Susan Li's article</a> on CRF implementation.</li>
        <li><b>NER_Spacy.ipynb</b>: Notebook that created the trained Spacy model. Shout out to <a href="https://spacy.io/usage/linguistic-features#named-entities">Spacy Docs</a>.</li>
        <li><b>review_train.txt</b>: Review training data. Big shout out to <a href="https://www.researchgate.net/publication/320282716_Ruchi_Rating_Individual_Food_Items_in_Restaurant_Reviews">this research paper</a> for the model training data. Unfortunately, this was not the most 'high quality' data due to many errors in the labeled data, but when you have a 0 dollar budget, this was gold.</li>
    </ul><li><b>extension</b></li><ul>
        <li><b>css</b>: Css for the <a href="https://materializecss.com/">Materialize library</a> and for the popup.</li>
        <li><b>content.js</b>: Script that sends the restaurant name from the webpage to the extension.</li>
        <li><b>manifest.json</b>: Template for setting up the Chrome extension. </li>
        <li><b>materialize.min.js</b>: Javascript add-on features from the materialize library.</li>
        <li><b>popup.html</b>: The face of Food Pulse (interface you interact with).</li>
        <li><b>popup.js</b>: The heart of Food Pulse (sends and receives messages from the Lambda function among other things).</li>
        </li>   
    </ul>
    <li><b>src</b> (brain 1):</li>
        <ul>
            <li><b>lambda_function.py</b>: What the lambda functions runs by default. Runs the review scraper, invokes lambda function 2, and returns the top foods.</li>
            <li><b>review_scraper.py</b>: Scraping Google reviews script.</li>
        </ul>
    <li><b>src1</b> (brain 2):</li>
        <ul>
            <li><b>entity</b>: Contains the final trained model to be uploaded to lambda (same one in DS folder).</li>
            <li><b>lambda_function.py</b>: Runs the ner, sentiment analysis, and returns the result to lambda function 1.</li>
            <li><b>ner.py</b>: Performs named entity recognition on the reviews.</li>
            <li><b>sentiment.py</b>: Performs sentiment analysis and returns the top food items.</li>
        </ul>
    <li><b>.gitignore</b>: Files we don't push to this repo.
    <li><b>docker-compose.yml</b>: Setting up the local Docker env to be used for local testing.
    <li><b>Dockerfile</b>: Instructions needed to setup the Docker image.
    <li><b>Makefile</b>: A set of instructions that can be run with a single specified command. This was used for local testing that simulated running Lambda functions on the cloud, and helped create deployment packages for Lambda. Big shoutout to <a href="https://github.com/jairovadillo/pychromeless">Jairo Vadillo</a>.</li>
    <li><b>requirements-scraper.txt</b>: Update needed.</ul>

<br>

## Special Thanks

- [Madhur Malhotra](https://www.linkedin.com/in/madhurxyz/) - For helping us create a bomb a$$ logo and powerpoint presentation.
- [Pranay Marella](https://www.linkedin.com/in/pranay-marella-0169018b/) - For helping with tricky front-end features.
- [Leyuan Yu](https://www.linkedin.com/in/leyuanyu/) - For helping with the Data Science components.
