# My Application

## How to Run
To run the application, follow these steps:

1. Install Dependencies: First, ensure you have Poetry installed. If not, you can install it using the following command:

poetry install

2. Navigate to Main Folder: Enter the main folder of the project.

3. Run the Server: Open a terminal and navigate to the app folder using the following command:

bash
cd app

4. Start the Server: Run the following command to start the server:

css
uvicorn main:app --reload

This will start the server, and you'll see a message indicating that the server is running.

5. Access the API: Once the server is running, you can access the API through the following link:
http://127.0.0.1:8000/docs

This link will open the FastAPI interface in your browser, where you can interact with the API endpoints.


## How to Use
The application is designed to be used through the FastAPI interface. Here's how to use the available features:

1. GET REPORTS: To retrieve all reports, click on the "GET /reports" endpoint in the FastAPI interface, then click on "Try it out" followed by "Execute".

2. GET REPORT RECORD: To retrieve a specific report record, click on the "GET /reports/{id}" endpoint in the FastAPI interface. Enter the ID of the report you want to retrieve, then click on "Try it out" followed by "Execute".

3. DELETE REPORT: To delete a report, click on the "DELETE /reports/{id}" endpoint in the FastAPI interface. Enter the ID of the report you want to delete, then click on "Try it out" followed by "Execute".

4. ADD REPORT: To add a new report, click on the "POST /reports" endpoint in the FastAPI interface. Upload an EXRF file, and if it is valid, it will be added to the database.

