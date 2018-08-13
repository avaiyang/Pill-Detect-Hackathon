# Pill-Detect-Hackathon
## Inspiration
At some point in our life, I think we've all faced the situation where we have a bunch of pills and no clue as to what each one is or does, or what it contains and it's always a chore to find a good and reliable resource to get that information. The situation is even worse for the visually impaired population and people in their Golden years, so we wanted a solution that gives the power of information to the people and at the same time helps make our elderly and visually impaired population more independent.

## What it does
1. You've got a pill or tablet  
2. You take its picture and click next, and it uses black magic to find the Information about the pill. 
3. You can also upload a picture of a pill and it'll give you the result in a similar manner.

## How we built it
Gathered data from a bunch of resources online ( https:https://rxnav.nlm.nih.gov/index.html ). Refined the data to build a proper usable database using pandas from python. Used AWS API to detect the imprint on the pill Used OpenCV to identify the shape and color of the pill Matched those attributes in our database to find the information about the pill.

## Challenges we ran into
Frontend and Backend Integration (nothing out of the ordinary)

## Accomplishments that we're proud of
Pill imprint(text) detection works with an accuracy of 99% (coutesy of AWS API), Image shape and color cam also be identified fairly reliably.

## What we learned
How to use OpenCV for shape and color detection AWS API for DIfficult to find text extraction

## What's next for PillDetect
Identify the pill and tell what it's used for.

## Built With
* python
* javascript
* html5
* css3
* jquery
* flask
* web2py
* amazon-web-services
* ajax
* pandas
