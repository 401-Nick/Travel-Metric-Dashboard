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
   ```
   git clone https://github.com/401-Nick/Travel-Metric-Dashboard.git
   ```

2. Navigate to the project directory.
   ```
   cd Travel-Metric-Dashboard
   ```

3. **Create a virtual environment**:
   - On macOS/Linux (Untested):
     ```
     python3 -m venv venv
     ```
   - On Windows:
     ```
     python -m venv venv
     ```

4. **Activate the virtual environment**:
   - On macOS/Linux (Untested):
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```

5. Create a `.env` file in the `app` directory with the following content:
   ```
   DATABASE_URI="sqlite:///users.db"
   SECRET_KEY="your_secret_key"
   ```
   Replace `your_secret_key` with a secret key of your choice.

6. Install dependencies using:
   ```
   pip install -r requirements.txt
   ```

7. Verify that Redis is installed and accessable by your system on port 6379. If not, you can download it from the [Redis website](https://redis.io/download). (Will improve this in the future, I use WSL to run Redis)

8. Navigate to the `app` directory:
   ```
   cd app
   ```

9. Run the flask application:
   ```
   flask run
   ```

