import os
import pandas as pd
import plotly.express as px
from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from app import db
from app.models import UploadedFile
from app.utils.verify_extension_type import is_csv_file

dashboard = Blueprint("dashboard", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@dashboard.route("/")
@login_required
def home():
    # Fetch uploaded files for the current user
    uploaded_files = UploadedFile.query.filter_by(user_id=current_user.id).all()
    if not uploaded_files:
        flash("No files uploaded yet", "danger")
        return render_template("dashboard.html", uploaded_files=[])

    # Initialize DataFrame
    data = pd.DataFrame()

    # Load and concatenate CSVs
    for f in uploaded_files:
        filepath = os.path.join(UPLOAD_FOLDER, f.filename)
        if os.path.exists(filepath) and is_csv_file(filepath):
            # Read CSV, treating specified NA values
            df = pd.read_csv(
                filepath, na_values=["", "NA", "NAN"], keep_default_na=False
            ).fillna(0)

            if not df.empty:
                df = df.dropna(how="all", axis=1)

                if "Booking Date" in df.columns:
                    df["Booking Date"] = pd.to_datetime(
                        df["Booking Date"], errors="coerce"
                    )

                if not df.empty:
                    data = pd.concat([data, df])

    # Metrics Calculation
    total_bookings = len(data)
    total_locations = len(data["Destination"].unique())
    total_revenue = round(data.get("Revenue", pd.Series()).fillna(0).sum(), 2)
    avg_cost = round(data.get("Cost", pd.Series()).mean(), 2)
    max_refund = round(data.get("Refund", pd.Series()).max(), 2)
    refund_rate = round(data.get("Refund", pd.Series()).mean(), 2)
    cancel_count = round(data.get("Canceled", pd.Series()).sum(), 2)

    # Generate Charts
    def generate_monthly_revenue_chart():
        if "Booking Date" in data and not data["Booking Date"].empty:
            data["Month"] = data["Booking Date"].dt.to_period("M").astype(str)
            monthly_revenue = data.groupby("Month")["Revenue"].sum().reset_index()
            return px.line(monthly_revenue, x="Month", y="Revenue").to_html(
                full_html=False
            )
        return "Upload a file to see monthly revenue trends"

    def generate_destinations_chart():
        if "Destination" in data and "Revenue" in data:
            dest_revenue = data.groupby("Destination")["Revenue"].sum().reset_index()
            return px.bar(dest_revenue, x="Destination", y="Revenue").to_html(
                full_html=False
            )
        return "Upload a file to see destinations by revenue"

    def generate_revenue_cost_chart():
        if "Revenue" in data and "Cost" in data:
            return px.scatter(
                data,
                x="Revenue",
                y="Cost",
                labels={"Revenue": "Revenue ($)", "Cost": "Cost ($)"},
                hover_data=["Destination", "Customer Name"],
                color="Destination",
            ).to_html(full_html=False)
        return "Upload a file to see revenue vs cost scatter plot"

    def generate_refund_chart():
        if "Refund" in data:
            # Ensure the Refund column is properly handled
            data["Refund"] = pd.to_numeric(data["Refund"], errors="raise").fillna(0)

            # Exclude rows where Refund is zero or less (if required)
            refund_data = data[data["Refund"] > 0].fillna(0)

            if not refund_data.empty:
                max_refund = refund_data["Refund"].max()

                # Create bins for the refund range
                bins = pd.interval_range(
                    start=0, end=max_refund, periods=5, closed="right"
                )
                refund_data["Refund Range"] = pd.cut(
                    refund_data["Refund"], bins=bins, include_lowest=True
                ).astype(str)

                return px.pie(
                    refund_data,
                    names="Refund Range",
                ).to_html(full_html=False)
            else:
                return "Refund data exists but no positive values to generate the distribution"
        return "Upload a file to see refund distribution"

    def generate_canceled_chart():
        if "Destination" in data and "Canceled" in data:
            return px.bar(
                data,
                x="Destination",
                y="Canceled",
            ).to_html(full_html=False)
        return "Upload a file to see canceled bookings by destination"

    # Render Template
    return render_template(
        "dashboard.html",
        total_revenue_metric=f"${total_revenue:,.2f}",
        average_cost_metric=f"${avg_cost:,.2f}",
        max_refund_metric=f"${max_refund:,.2f}",
        total_locations_metric=total_locations,
        total_bookings_metric=total_bookings,
        canceled_count_metric=cancel_count,
        refund_rate_metric=(
            f"{(refund_rate / total_bookings):.2%}" if total_bookings > 0 else "0.00%"
        ),
        revenue_cost_chart_html=generate_revenue_cost_chart(),
        refund_chart_html=generate_refund_chart(),
        canceled_location_chart_html=generate_canceled_chart(),
        monthly_revenue_chart_html=generate_monthly_revenue_chart(),
        destinations_chart_html=generate_destinations_chart(),
        uploaded_files=uploaded_files,
    )
