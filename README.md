# Diana

This project is developed as a part of **Flipkart Grid 2.0 Hackathon** by me(Susanka Majumder) and my classmate Souvik Dutta (Team **NeoSaints**).

## Problem Statement

A fashion retailer wants to source ongoing and upcoming fashion trends from major online fashion portals and online magazines in a consumable and actionable format, so that they are able to effectively and efficiently design an upcoming fashion product portfolio.

Deliverables:

  1. Identify products that are better performers (in a rank ordered fashion)
  2. Help the user view the products that are both trending and lagging
  3. Identify a logic for classifying products as per their trendiness

We were asked to complete the challenge for just the t-shirt product vertical, but to ensure that our solution would be scalable to other products as well.

## Project Explanation

here a [youtube video](https://youtu.be/1sd2M33Di4M) explaining how the project works.

## Project Structure

This project consists of two major components 

1. **Backend** - consists of jupypet notebooks that were used to collect data and train our models on that data. 
2. **Frontend** - consists of a ReactJs project in order to serve the result to the end user.

## Installion and Running
1. Clone this repository 
```
git clone https://github.com/susanka068/Diana.git
```
2. Run the bash script for initial setup
```
./setup.sh
```
3. From the root directory run the stage_0.py file to download, extract and refine the data. (Note : As the dataset is quite large , it might take some time to download all the data)
``` 
python ./Backend/stage_0.py
```
( Hit `Ctrl + C` if you want to terminate data extraction at any point .Although it's crucial to download the complete dataset to train the model properly )

4. Run the final script to train the model and start the frontend.
```
./run.sh
```

## Contributing 

I believe in the power of open source hence feel free to contribute in any way possible(Bug Fixes or Enhancements). Also if you liked the project you can give it a star 🌟 😁.


