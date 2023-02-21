# Flight Guru

## Description
For our project we plan to use the [2015 Flight Delays and Cancellations](https://www.kaggle.com/datasets/usdot/flight-delays) dataset. The data stores all of the flight information from flights in 2015, the information is from the department of transportation, and we want to provide users searching up flights with up to date flight statuses. We are aiming to solve the problem of travel stress by giving users up to date information on their flights. We plan to reduce user’s stress by allowing them to subscribe for email notifications for flights that they select, these notifications update users on if their flight is delayed or canceled. 
Our application will also inform our users so they can make smart decisions on airline choices based on data like the percentage of flights on time for an airline or an airport. 

## Realness

The U.S. Department of Transportation's (DOT) Bureau of Transportation Statistics tracks the on-time performance of domestic flights operated by large air carriers. Summary information on the number of on-time, delayed, canceled, and diverted flights is published in DOT's monthly Air Travel Consumer Report and in this dataset of 2015 flight delays and cancellations. 

The columns we plan on using are: month, day, day of the week, airline, flight number, tail number, origin airport, destination airport, scheduled departure time, actual departure time, departure delay, elapsed time of the flight, scheduled arrival, actual arrival, arrival delay, canceled flights, reason for the cancellation, reason for delay. For visualizations we plan to use the airports positional data to display where the airports are geographically. 


## Usefulness

Our application is useful because it gives users up-to-date information on their flights. Going to the airport can be an extremely stressful situation, our application aims to ease that travel stress. By giving users notifications on the status of their flights and even helping them find alternative flights if theirs gets canceled. There are similar websites out there, but ours is more aimed at the passenger of a flight, while most flight tracking websites are aimed at people who like to watch flights. The main difference is that ours sends notifications of the estimated time of departure, and provides help upon cancellations. A similar website is [Flight Aware](https://flightaware.com/), which does not provide as many search options as we do, and their main focus is the flight path so people can see where the flight is from take-off, to arrival. 

## Functionality

On our application, users can search up flights by flight number or by: departure airport, destination airport, and airline. After searching the user will get one of four new screens. If the flight is on time, the user will be displayed a screen stating that their flight is on time and a list of flight attributes; these attributes include the departure airport, arrival airport, departure time, airline, and flight number. If the flight is delayed, the user will get a message similar to: "The flight (flight number), from X-airport to Y-airport, has been DELAYED, the flight will now be at (new time),which was originally at (original time). We plan to calculate if the flight is delayed by using the departure_delay column. If the flight is canceled, the user will get a message stating that the flight was canceled, and they will see a table of flights with similar airports, and times that they can rebook onto. The last result would be if we can't find their flight, which shouldn't happen because our search bars should only let them search for flights that exist.

## Work Distribution

We plan to split the work between front-end and back-end, with David and Yijing working on the back end, and Chris and Jake working on the front end. We plan to use both Python and MySQL for the back-end, and JavaScript and HTML for the front-end; if we need to incorporate any other language or resource, we will make that decision when the time comes. The backend team is working on setting up and populating our databases, and creating a functional user authentication system. Our front end team is going to work on building the website, making it usable and making it look good, and they will also work on data analysis.

## UI Mockup
[Mock UI.pdf](https://github.com/cs411-alawini/sp23-cs411-team065-team065/files/10797181/Mock.UI.pdf)
