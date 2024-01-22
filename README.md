# Movie Ticket Booking System

## Description

The Movie Ticket Booking System is a comprehensive application designed to facilitate the management of movie shows, venues, and ticket reservations. This system enables administrators to perform CRUD operations on the venue and show tables within the backend, while users can easily reserve tickets and search for various shows and venues. The main focus is on utilizing advanced technologies to enhance the overall functionality of the system.

## Technologies Used

- **DateTime:** Handling date and time, especially for timestamping ticket purchases.
- **Flask:** A Python micro web framework for routing, requests, and responses.
- **Flask Components:** Includes request, jsonify, and Response for request handling, JSON responses, and custom HTTP responses.
- **CORS:** A Flask extension for secure cross-origin data exchange.
- **SQLAlchemy:** An ORM simplifying database interactions through Python classes.
- **Flask-Login:** Managing user authentication, sessions, and roles.
- **pytz:** Handling time zones for timestamps.
- **Flask-APScheduler:** Integrating task scheduling with Flask.
- **smtplib:** Sending emails via SMTP.
- **email.mime.multipart, email.mime.text:** Building MIME messages for email.
- **CSV, io:** Python's built-in libraries for CSV and I/O operations.
- **Redis:** Caching.
- **Celery:** Batch jobs for daily reminders and monthly reports.


## Architecture

- **Project Root:**
  - Contains the database file and `main.py`, the primary file for running the backend.
  - Includes other Python files required for Celery.

- **Frontend Folder:**
  - Contains subfolders like src, views, components, router, assets, and various files that contribute to rendering the frontend using Vue.js.

## Features

- Admins can perform CRUD operations on shows and venues.
- Admins can download CSV files for shows and venues.
- Users can book tickets and search for shows and venues.
- Monthly reports and daily reminders are sent to user email IDs.
- Both admin and user authentication is managed.
- A navigation bar is provided for easy system navigation.
- Styling has been implemented to enhance the user interface.
- User information is cached in the browser's local storage for improved performance.
- Data related to shows, venues, and bookings are cached in Redis.

## Author
*Gautam Gala*

For inquiries, please [email me](mailto:gautamgala5544@gmail.com).
