# DTNA Productivity Dashboard

Real-time analysis of efficiency based on man hours per vehicle made for Daimler Trucks North America's Mt Holly, NC plant. Data has been obfuscated to keep sensitive information from public view. As such, the app will not run properly without formatted data to run through.

## Features

- Analysis of Hours-Per-Vehicle(HPV) by department and shift as well as the plant as a whole.
- Table of current HPV per department and shift.
- Graphs showing the trend of the HPV over the course of the day and shift.
- Graphs showing HPV by department over the day, week, or month.
- Compare today's trend with the same day last week.
- Heatmap showing trends over the course of the day to identify hour-by-hour trends.

## How to Use

The app cannot work without either being connected to the Daimler live server or with csv data to use to simulate live data coming in via the "dripper". Since the information in those files is private and cannot be put on github, the app will not be able to run. The names of variables and columns have been changed as well.

Because there are no properly formatted CSVs, this project is only available to view, not run.

# Walk-through

The app is composed of two main parts: Development tools and the application display.

## Development tools - Data dripper

Because we could not connect to the database during development (the team was located 2 hours away from the plant) we had to devise a way to simulate the database being connected and populated. We found that we would actually have needed this solution even if we could connect to the database because we needed to have new data come in more often than every 10-15 minutes.

### Data Dripper

The "generic_dripper" files contain the data dripper. The dripper allows us to simulate the tables in the live database and add data at will or on a timer. This is done through a web app interface in X steps:

1) Data is read from CSVs into a local database.
2) It is copied from those tables into dripper versions of themselves.
3) Data is flushed from the original tables.
4) Dripper is started.

The interval between drips is set to the refresh rate of the page in the generic_dripper/templates folder.

The dripper checks and modify incoming data from the attendance table. Because the data is historic and clock-in/out columns are filled even when the employee is considered "clocked-in" based on what time we are simulating.

When developing we can watch the app run over the course of days or weeks in a matter of minutes. Combined with testing, this creates an ideal development scenario.

## Dashboard display
