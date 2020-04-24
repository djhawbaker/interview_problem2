# Instructions

1. Create a program that can interactively play the game of Tic-Tac-Toe against a human 
   player. 
   * The program should win or draw, but never lose.
   * The human player should make the first move.
   * The program should announce the result of the game before clearing the board for 
     another round of play.
1. A git repo has been initialized in the project root - commit early and often, with good messages.

When you've completed your submission, zip or tar the project back up, and be sure to include
your `.git` folder so we can see your commit history.

We are more interested in getting a view into how you approach the problem than 
anything else, so a good commit history is vital.

This isn't a timed test, so don't think of the commit history as being a measure of 
pace - we're not looking at that.
We understand this is something you'll be working on in between other things.
If, for some reason, you feel unable to complete the entire exercise, that's fine.
Just try to give us enough code to look at to get a sense of your approach.

# Implementation Guidelines

Your implementation should meet the following requirements:

* The game logic should be executed server-side (you pick the language/framework but we 
  use a mix Django and Flask in Python).
* The interface for the game should be a JavaScript Single Page Application (SPA) running
  in a browser (again, you pick the frameworks/toolchains but we use a mix of React and Vue).
* You should rewrite this `README.md` to include build/run instructions for your apps 
  (both client and server).

For a little extra credit:

* The SPA should _not_ be hosted by the server-side app, but instead through a separate 
  server process (the client app should be completely standalone).

## Setup environment

The following packages need to be installed on the system before running
- [Node.js](https://nodejs.org/en/)
- [Yarn](https://yarnpkg.com/)
- [Python3](https://www.python.org/)

Create a virtual environment within the api directory to hold the required libraries 

Unix based

    cd api
    python3 -m venv venv
    source venv/bin/activate

Windows based

    cd api
    python -m venv venv
    venv\Scripts\activate

Then install the required libraries

    pip3 install flask python-dotenv
    yarn add react
    
## Run Instructions

Start the server app

    cd api
    yarn start-api

In a separate terminal start the client app from the root of the project

    yarn start

This should open a web browser running the game that is talking with the server AI



This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
