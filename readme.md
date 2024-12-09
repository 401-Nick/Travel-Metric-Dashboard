# Metrics Dashboard

## Overview
The **Metrics Dashboard** is a Flask-based application designed to provide users with insights into their uploaded CSV files. It allows users to upload files and view various metrics and visualizations from the data, such as revenue trends, refund distributions, and booking statistics.

---

## Features

### User Authentication
- Only logged-in users can access the dashboard.

### File Upload
- Users can upload CSV files for analysis and users can only access the data they upload.

### Metrics Calculations
- **Total Revenue**: Sum of the `Revenue` column.
- **Average Cost**: Mean of the `Cost` column.
- **Maximum Refund**: Highest value in the `Refund` column.
- **Total Bookings**: Count of all bookings.
- **Total Locations**: Number of unique destinations.
- **Canceled Bookings**: Sum of the `Canceled` column.
- **Refund Rate**: Average refund relative to bookings.

### Visualizations
- **Revenue vs Cost Scatter Plot**: Shows correlation between revenue and cost.
- **Refund Distribution**: Displays refunds using a pie chart.
- **Monthly Revenue Trends**: Line chart for revenue by month.
- **Destinations by Revenue**: Bar chart of revenue grouped by destination.
- **Canceled Bookings by Destination**: Bar chart of cancellations per destination.

---

## Installation
1. Clone the repository.
   ```bash
   git clone https://github.com/401-Nick/Travel-Metric-Dashboard.git
   ```

2. Navigate to the project directory.
   ```bash
   cd Travel-Metric-Dashboard
   ```

3. Install dependencies using:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the `app` directory with the following content:
   ```env
   DATABASE_URL="sqlite:///users.db"
   SECRET_KEY="your_secret_key"
   ```
   Replace `your_secret_key` with a secret key of your choice.

5. Navigate to the `app` directory:
   ```bash
   cd app
   ```

6. Run the flask application:
   ```bash
   flask run
   ```
