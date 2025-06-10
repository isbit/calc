# Instructions for using the application
## How to run
- Run setup_db.py to create the database with sample data.
- Start the application by running app.py

## Login information
| Username | Password |
|----------|----------|
| admin    | admin    |
| user     | user     |
| user1    | user     |
| user2    | user     |
| user3    | user     |
| user4    | user     |

# Functionalities
## Not logged in
- When not logged in, users can see a list with the names of the questionnaires. Answering requires login.

## Register user
- All fields are required.
- Username must be unique. Uses AJAX to check the database on keyup, and provides feedback using js.
- Password must be at least 6 characters long. Front- and backend checks to ensure this.
- Requires password to be retyped, and must match password. Front- and backend check to ensure this.

## Logged in user
- When logged in, the list of questionnaires includes buttons for answering or changing answers on a questionnaire. Another button lets the user filter out the already answered ones.
- On the users account page, the user can delete their own account. User datails, including information about answered questionnaires are deleted from the database.
- On the users account page, there is a toggle for dark mode. Clicking it updates the database with the choice, using a PUT method.
- Access to some sites, like /admin is restricted for normal users
- After sumbitting answers on a questionnaire, the information is validated backend.
- The user may change their answers, and this will update the database.

## Logged in admin
- When an admin is logged in, they are able to create new admin users. The ability is rendered frontend, and backend ensures they have admin rights to do so.
- When an admin navigates to /admin/users, all users appear in a list which is searchable by username or id. Admins can also delete users.
- Admins can create new questionnaires. The information is validated backend.

## Layout
- Flexbox is used on several divs and forms to control the appearance of the page when resized.
- On a window narrower than 500px, the right side of the navigation bar on the top gets hidden and becomes a hamburger menu. Clicking it brings back the options in a dropdown menu. The dropdown menu uses absolute position.

## Javascript game
- After answering a questionnaire, the user is directed to a wheel of fortune game made in javascript, where they can win tokens. The tokens are saved to the database using PUT methhod, and are shown on the users account.
- This game has security issues in relation to the winning and acumulation of tokens. As this is a frontend app the user might change the outcome of the result and send it in to server side. Optimally the calculation of win and loss would be done by a flask route.

## Image upload
- The user can upload a profile picture. Proper checks to ensure the file is an image is in place. The image gets saved to /static/uploads/username, and a link to this is saved to the database. The image is removed upon user deletion.

## Functions
- All selfmade Python functions are imported from functions.py

## Calculation and queries
- Admins can view a table that shows the percentage of users that have answered each questionnaire. 
The query uses LEFT JOIN to include unanswered questionnaires, and GROUP BY to only include each questionnaire once. The percentage is calculalted in a function.


### References
- The css part og the java game is based the game in this link. https://dev.to/madsstoumann/wheel-of-fortune-with-css-p-pi-1ne9