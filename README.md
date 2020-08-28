# Food-Pulse


**Goal:** Obtaining the top 5 best food items (that people like via reviews) for a particular restaurtant. 

**How**: We want a user to be able to open a desired restaurant via google reviews and click an extension icon to generate the top relevant food items.

V-1.0 <br>
**Process:** 
1) Send a request to aws lambda with an identifier for a particular restaurant
2) Use that input to open up a headless browser and scrape the restaurant reviews
3) After getting all the reviews, do NLP and get the top food items.
4) Return the top food items to be displayed on the extension. 

**Future Iterations:**
1) Store reviews in a db, so you can possibly write once and read many.
2) Set up 2 lambda functions, one for each process: scraping and NLP.
3) Possibly look up restaurants for the user to enter and we would take care of the rest. 
