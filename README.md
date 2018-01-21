# EbuildDevOpsDashboard
Simple Dashboard Service for Managing Gentoo Linux

# Overview
This project's purpose is to read in raw output from a Gentoo Linux emerge --pretend @world and generate a web dashboard detailing packages that the system would like to compile the next time administration approves a build. Currently this project provides 2 endpoints:
* / - The root endpoint produces a HTML output of a table with details about each component to be compiled
* /world/json - A JSON object output of the list of packages to be built for consumption by other automation.

# Future plans
Additional styling and features will be added to this component over time. Some planned additions are:
* Login capability - to safeguard additional root level functionalities.
* An Execute button on the dashboard - visible to users with devops permissions while a build is not in progress, will send a message to other automation components that will run the emerge @world as planned.
* self-refreshing log display showing realtime information about current execution in progress.
* updating header on dashboard during an execution showing progress
* CSS and JS based styling improvements to be more modern.
