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

## Back-End

The data_processor/ folder contains the HPV calculations by shift and the whole day. These calculations are written to an API to capture the "current" HPV values at the simulated (or real if connected to the live server) time. The API is used by the front-end via AJAX calls for the NVD3 graphs.

## Dashboard Display
Images of the dashboard can be found at http://imgur.com/a/mmhYX.

The dashboard's main page shows a table of the current HPV for the shift and the shifts over the last 24 hours (they reset 1 hour before the shift begins). Because the plant can have 1-3 shifts, the table adjusts based on the number set in the admin settings. The graph shows the HPV over the last 24 hours and the current statistics are displayed on the bottom.

The details page allows the user to select views by department or the plant. It displays data over the select time frame in the first graph. The second graph shows the current day compared to the same day last week. The heatmap on the bottom shows the relative hpv by day and hour. This helps visualize trends over the course of a week and find if productivity drops at predictable times.

The admin pages allows customization of a few things:
- The plant code (for expanding to other plants).
- The target number of trucks to make per day.
- The number of shifts.
- The maximum time to go without writing a "current hpv" entry in the API.
- How often to check for a new truck being completed.
- How long to keep data in the API
- The start time for each shift.
