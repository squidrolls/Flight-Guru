**Changes:**
- The UI is completely different, the final UI is much more professional looking, and easier for the user to use. 
- User Notifications for delayed or canceled flights are not present
- Added a map on the front page for a creative component
- Our create function is different from our original intent, we added an extra table to keep track of users and then a table to keep track of subscriptions, instead of one table to keep track of both.
- The subscription table design. We designed the username as the primary key. However, during the implementation, we realized that a single user could subscribe to multiple flights, resulting in duplicate primary keys. To resolve this issue, we changed the primary key to an auto-incrementing number.

**Usefulness:**

If the data was live data we believe this application would have been pretty useful to allow people to keep track of their or relative’s flights. Even without the live data we also believe that our visualization and the statistics of each airline would have been useful to make an informed decision about which airline to fly with or about what to expect/be prepared for during a flight

**Schema Changes:**

Our schema was relatively the same. We had every table we planned to have. However, for some tables the columns we selected were not enough to uniquely identify flights, so we had to select more columns. We also added in a table that was related to the Users table, this table kept track of the user’s subscriptions based on the username.

**ER Diagram Changes:**

The ER diagram had similar issues to the relational schema, as we sometimes needed more columns to uniquely identify parts of tables, but the overall functionality and dependencies are the same.

**Functionality Differences:**

We added many search bars depending on what part of the application you were looking at. This way the user knew what results they were getting when they searched, instead of having one search bar to search every table. The map we added was fully interactive and demonstrated the cancellation rate for an airport when that point was selected. We removed the notification functionality as it was too much to focus on with the other aspects of the project needing to get done.


**Challenges:**

- Learning new frameworks/full-stack development: When we looked at using Django or React, all the generated code and steps seemed much more overwhelming than Flask so I think choosing that framework helped us feel less confused. Having members that were more experienced with full-stack development helped as well since they were able to break down how different components of our application communicated with one another. Watching the workshop videos on prairielearn also was pretty essential as we used that code to help us get started with our application. Using libraries like bootstrap also helps cut down the time on working with HTML and CSS so that we could also create a beautiful site without much work. - **David**
- We overcame challenges setting up our computers to run the flask app through the docker environment. This included issues with the python version, terminal path, other various download/setup errors and challenges. To tackle these, a fair amount of googling and prior knowledge came into play. We realized some of the later python versions didn’t work and replaced them with earlier versions. Also some packages couldn’t be found after installing them while running so adjusting the PYTHONPATH while in the environment solved it. Other miscellaneous googling guided us through all other setup when and if issues were encountered. - **Chris**
- Setting up the tables in mySQL Workbench from CSV files. First, our CSV files were not separated into the tables we wanted them to be separated into. So we had to manually create more CSV files from the original files. The way we did this was in R, we used the Tidyverse to easily split our original tables into the many tables we needed. After that there was issues implementing the CSV files into GCP, so what I would recommend is using notepad++ to convert the CSV files into SQL files using this [reddit thread](https://www.reddit.com/r/SQLServer/comments/s0q10z/notepad_plugin_to_convert_csv_files_to_sql_insert/), and this [github repository](https://github.com/BdR76/CSVLint/). Once those tables were set up we had issues creating foreign keys, but our work around for that was to not implement them as foreign keys and every SQL command we wanted to implement ran exactly as we wanted it to, so I don’t think the fact that they weren’t implemented as foreign keys was an issue. - **Jake**
- The query execution time of calculating the cancelation rate is long because it  involves two subqueries, and the flights table is very large. At first, we tried to change the query by using an INNER JOIN with the flights table on the selected states only, and create indexes on columns used in the WHERE and JOIN clauses because the indexes can speed up searches and lookups. Through these process, we decreased the query time for all states from over 120 seconds to 30 seconds, but it was still very slow. Finally, we figured out that we could use a stored procedure and trigger to precompute and stored the cancellation rate of each airport, greatly reducing the calculation time when retrieving the cancellation rate later. - **Yijing**

**Future Work:**

In the future, ways this application can improve are in the data category. Using up to date information instead of older data, so that way the application is much more useful to users, as they can actually track their flights in real time. Another thing that could be improved upon is implementing the e-mail notifications after implementing the up to date data. E-mail notifications allow the user to be less vigilant when using the application, as they do not have to constantly check to see if their flight is on-time, delayed, or canceled. In addition, currently, our application focuses on the user side. In the future, we plan to add an admin side, allowing administrators to manage flight data directly through the front-end interface, rather than relying on MySQL Workbench.

**Division of Labor:**

Jake and David set up all of the SQL tables, and worked out any bug fixes in that category. Yijing and Chris worked on creating the actual front end side of the application, and we worked as a group to fix any bugs and make it look nicer. We used a discord groupchat to communicate. We primarily worked as a group meeting up a couple of times before each stage was due.


