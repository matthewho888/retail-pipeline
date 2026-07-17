import pandas as pd
import psycopg2
import streamlit as st


st.set_page_config(
    page_title="Retail Pipeline Dashboard",
    layout="wide",
)

st.title("Retail Pipeline Dashboard")
st.caption("PostgreSQL → dbt marts → Streamlit")


@st.cache_data(ttl=60)
def run_query(query: str) -> pd.DataFrame:
    """Run a PostgreSQL query and return the results as a DataFrame."""

    with psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        port=st.secrets["postgres"]["port"],
        dbname=st.secrets["postgres"]["dbname"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        connect_timeout=5,
    ) as connection:

        with connection.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()
            columns = [
                column[0]
                for column in cursor.description
            ]

    return pd.DataFrame(rows, columns=columns)

# --- navigation ---

page = st.sidebar.radio(
    "Navigate",
    ["Customers", "Sellers", "Fulfillment"],
)

# --- dashboard pages ---

try:
    if page == "Customers":
        st.header("Customer Analysis")

        customer_summary = run_query(
            """
            SELECT
                COUNT(*) AS total_customers,
                SUM(
                    CASE
                        WHEN num_of_orders > 1 THEN 1
                        ELSE 0
                    END
                ) AS repeat_customers,
                SUM(total_sum) AS total_customer_spend
            FROM retail_transforms.mart_customer_orders;
            """
        )

        total_customers = int(
            customer_summary.loc[0, "total_customers"]
        )

        repeat_customers = int(
            customer_summary.loc[0, "repeat_customers"]
        )

        total_customer_spend = float(
            customer_summary.loc[0, "total_customer_spend"]
        )

        column_one, column_two, column_three = st.columns(3)

        column_one.metric(
            "Total Customers",
            f"{total_customers:,}",
        )

        column_two.metric(
            "Repeat Customers",
            f"{repeat_customers:,}",
        )

        column_three.metric(
            "Total Customer Spend",
            f"${total_customer_spend:,.0f}",
        )

        top_customers = run_query(
            """
            SELECT
                customer_unique_id,
                most_recent_purchase,
                num_of_orders,
                total_sum
            FROM retail_transforms.mart_customer_orders
            ORDER BY total_sum DESC
            LIMIT 10;
            """
        )

        st.subheader("Top 10 Customers by Spend")

        st.dataframe(
            top_customers,
            use_container_width=True,
            hide_index=True,
        )

    elif page == "Sellers":
        st.header("Seller Performance")

        seller_summary = run_query(
            """
            SELECT
                COUNT(*) AS total_sellers,
                SUM(total_revenue) AS total_revenue,
                SUM(avg_review_score * num_of_reviews)
                    / NULLIF(SUM(num_of_reviews), 0) AS overall_review_score
            FROM retail_transforms.mart_seller_performance;
            """
        )

        total_sellers = int(
            seller_summary.loc[0, "total_sellers"]
        )

        total_revenue = float(
            seller_summary.loc[0, "total_revenue"]
        )

        overall_review_score = float(
            seller_summary.loc[0, "overall_review_score"]
        )

        column_one, column_two, column_three = st.columns(3)

        column_one.metric(
            "Total Sellers",
            f"{total_sellers:,}",
        )

        column_two.metric(
            "Total Seller Revenue",
            f"${total_revenue:,.0f}",
        )

        column_three.metric(
            "Overall Review Score",
            f"{overall_review_score:.2f}",
        )

        top_sellers = run_query(
            """
            SELECT
                seller_id,
                seller_state,
                seller_city,
                total_revenue,
                avg_review_score,
                num_of_reviews
            FROM retail_transforms.mart_seller_performance
            ORDER BY total_revenue DESC
            LIMIT 10;
            """
        )

        st.subheader("Top 10 Sellers by Revenue")

        st.dataframe(
            top_sellers,
            use_container_width=True,
            hide_index=True,
        )

        revenue_by_state = run_query(
            """
            SELECT
                seller_state,
                SUM(total_revenue) AS state_revenue
            FROM retail_transforms.mart_seller_performance
            WHERE seller_state IS NOT NULL
            GROUP BY seller_state
            ORDER BY state_revenue DESC;
            """
        )

        st.subheader("Revenue by Seller State")

        st.bar_chart(
            revenue_by_state,
            x="seller_state",
            y="state_revenue",
        )

    elif page == "Fulfillment":
        st.header("Order Fulfillment")
        fulfillment_summary = run_query(
            """
            SELECT
                COUNT(*) FILTER (
                    WHERE order_status = 'delivered'
                ) AS delivered_orders,

                COUNT(*) FILTER (
                    WHERE delivery_status = 'on_time'
                ) AS on_time_orders,

                COUNT(*) FILTER (
                    WHERE delivery_status = 'late'
                ) AS late_orders,

                AVG(
                    EXTRACT(EPOCH FROM days_difference) / 86400
                ) FILTER (
                    WHERE order_status = 'delivered'
                ) AS average_days_difference

            FROM retail_transforms.mart_order_fulfillment;
            """
        )

        delivered_orders = int(
            fulfillment_summary.loc[0, "delivered_orders"]
        )

        on_time_orders = int(
            fulfillment_summary.loc[0, "on_time_orders"]
        )

        late_orders = int(
            fulfillment_summary.loc[0, "late_orders"]
        )

        average_days_difference = float(
            fulfillment_summary.loc[0, "average_days_difference"]
        )

        on_time_rate = (
            on_time_orders / delivered_orders * 100
            if delivered_orders > 0
            else 0
        )

        column_one, column_two, column_three = st.columns(3)

        column_one.metric(
            "Delivered Orders",
            f"{delivered_orders:,}",
        )

        column_two.metric(
            "On-Time Delivery Rate",
            f"{on_time_rate:.1f}%",
        )

        column_three.metric(
            "Average Days Early/Late",
            f"{average_days_difference:.1f}",
        )

        delivery_counts = run_query(
            """
            SELECT
                delivery_status,
                COUNT(*) AS order_count
            FROM retail_transforms.mart_order_fulfillment
            WHERE delivery_status IS NOT NULL
            GROUP BY delivery_status
            ORDER BY delivery_status;
            """
        )

        st.subheader("Delivery Performance")

        st.bar_chart(
            delivery_counts,
            x="delivery_status",
            y="order_count",
        )

        recent_orders = run_query(
            """
            SELECT
                order_id,
                order_status,
                ordered_at,
                delivered_at,
                estimated_delivery_at,
                delivery_status,
                days_difference
            FROM retail_transforms.mart_order_fulfillment
            ORDER BY ordered_at DESC
            LIMIT 20;
            """
        )

        st.subheader("Recent Fulfillment Records")

        st.dataframe(
            recent_orders,
            use_container_width=True,
            hide_index=True,
        )

except Exception as error:
    st.error("Dashboard query failed.")
    st.exception(error)