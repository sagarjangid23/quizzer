# Project Description:
You will be building an application that allows users to create and participate in timed quizzes. The application should have a RESTful API that provides functionalities for creating and retrieving quizzes.


# Functionalities:
- Create a Quiz: Users should be able to create a quiz by sending a POST request to the API with the following fields:
    - question: the text of the question
    - options: an array of the answer options for the question
    - rightAnswer: the index of the correct answer in the options array
    - startDate: the date and time when the quiz should start
    - endDate: the date and time when the quiz should end

- Get Active Quiz: Users should be able to retrieve the active quiz (the quiz that is currently within its start and end time).

- Get Quiz Result: After the 5 minute of end time of a quiz, users should be able to retrieve the result of the quiz. The result is basically the right answer .


# The API should have the following endpoints:
    - POST /quizzes - to create a new quiz
    - GET /quizzes/active - to retrieve the active quiz (the quiz that is currently within its start and end time)
    - GET /quizzes/:id/result - to retrieve the result of a quiz by its ID
    - GET /quizzes/all - to retrieve the all quizes

The API should be well-documented, and the code should be well-organized and easy to read.
The API should implement error handling for all endpoints and return appropriate error responses.


# The API should have a status field for each quiz:
    - inactive: before the start time of the quiz
    - active: during the time when the quiz is available
    - finished: after the end time of the quiz
    
The status field should be updated automatically by the application based on the start and end time of each quiz.
  
IMPORTANT NOTE: Use Cron Job for changing the status of the quiz based on it’s start time


# Bonus Points:
    Implement rate-limiting to prevent abuse of the API.
    Implement caching to reduce the response time of frequently accessed data.
    
Tech Stack you used: python, django rest framework, mysql, apscheduler etc..
