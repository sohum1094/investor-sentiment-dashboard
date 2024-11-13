# streamlit-frontend.py

#terminal command to launch - "streamlit streamlit-frontend.py"





import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Define industries and sub-industries
industries = {
    "Tech": ["Software", "Hardware", "AI & ML"],
    "Healthcare": ["Pharmaceuticals", "Medical Devices", "Health Insurance"],
    "Finance": ["Banking", "Investment", "Fintech"],
    "Energy": ["Oil & Gas", "Renewable Energy", "Utilities"],
    "Consumer Goods": ["Food & Beverage", "Retail", "Luxury Goods"],

    # Creating one to show all Graphs so it doesnt seem buggy
    "Test Graphs": ["All Charts","Line Chart", "Bar Chart", "Pie Chart", "Scatter Plot", "Table", "Gauge Chart"]
}

# Initialize session state for page routing
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Sidebar logic to route pages
def main():
    st.title("Investor Sentiment Analysis Dashboard")

    # Dropdown to select industry and sub-industry
    selected_industry = st.selectbox("Select an Industry", list(industries.keys()))
    selected_sub_industry = st.selectbox(
        "Select a Sub-Industry", industries[selected_industry]
    )

    if st.button("Submit"):
        # Route to the new page
        st.session_state.page = f"industry/{selected_sub_industry}"

    # Default homepage visualization
    render_homepage()

def render_homepage():
    st.header("Sentiment Analysis by Industry (2000 - 2030)")

    # Generate smoother random data for the homepage visualization
    years = np.arange(2000, 2031)

    def generate_scores(base, variation):
        trend = np.linspace(base - variation, base + variation, len(years))
        noise = np.random.normal(0, 2, len(years))
        return np.clip(trend + noise, 50, 100)

    # Create a DataFrame for the homepage line chart
    df = pd.DataFrame({
        "Year": np.tile(years, len(industries)),
        "Industry": np.repeat(list(industries.keys()), len(years)),
        "Interest Score": np.hstack([
            generate_scores(base=70, variation=10) for _ in industries
        ])
    })

    # Interactive line chart for the homepage
    fig = px.line(
        df, 
        x="Year", 
        y="Interest Score", 
        color="Industry", 
        markers=True, 
        title="Interest Scores by Industry (2000 - 2030)"
    )
    fig.update_layout(xaxis=dict(tickmode='linear', tick0=2000, dtick=5), hovermode="x unified")

    # Display the line chart
    st.plotly_chart(fig, use_container_width=True)

def render_sub_industry_page(sub_industry):
    st.title(f"Analysis Dashboard: {sub_industry}")

    #Just making it example specific
    if sub_industry == "All Charts":
        # Bar Chart Example
        st.subheader("Bar Chart Example")
        bar_values = [3, 7, 5]
        bar_categories = ["Category A", "Category B", "Category C"]
        fig_bar = px.bar(x=bar_categories, y=bar_values, labels={"x": "Category", "y": "Values"}, title="Bar Chart Example")
        st.plotly_chart(fig_bar, use_container_width=True)

        # Line Chart Example
        st.subheader("Line Chart Example")
        line_data = pd.DataFrame({"x": [1, 2, 3], "y": [10, 20, 15]})
        fig_line = px.line(line_data, x="x", y="y", labels={"x": "X-Axis", "y": "Y-Axis"}, title="Line Chart Example")
        st.plotly_chart(fig_line, use_container_width=True)

        # Pie Chart Example
        st.subheader("Pie Chart Example")
        fig_pie = px.pie(values=[30, 20, 50], names=["Category A", "Category B", "Category C"], title="Pie Chart Example")
        st.plotly_chart(fig_pie, use_container_width=True)

        # Scatter Plot Example
        st.subheader("Scatter Plot Example")
        fig_scatter = px.scatter(x=[1, 2, 3], y=[5, 9, 2], labels={'x': "X-Axis", 'y': "Y-Axis"}, title="Scatter Plot Example")
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Table Example
        st.subheader("Table Example")
        table_data = pd.DataFrame({
            "Metric": ["Metric A", "Metric B", "Metric C"],
            "Value": [100, 200, 300]
        })
        st.table(table_data)
        # Gauge Chart Example
        st.subheader("Gauge Chart Example")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=75,
            title={"text": "Performance"},
            gauge={"axis": {"range": [0, 100]}}
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    #Wanted to show the example of a single page
    elif sub_industry == "Line Chart":
        # Line Chart Example
        st.subheader("Line Chart Example")
        line_data = pd.DataFrame({"x": [1, 2, 3], "y": [10, 20, 15]})
        fig_line = px.line(line_data, x="x", y="y", labels={"x": "X-Axis", "y": "Y-Axis"}, title="Line Chart Example")
        st.plotly_chart(fig_line, use_container_width=True)

    #Information about page when content not loaded according to this specific example
    else:
        st.subheader(f"Currently viewing {sub_industry} data")
        st.write("This is where industry-specific content would be.")

    # Button to go back to the home page
    if st.button("Back to Home"):
        st.session_state.page = "home"

# Router to handle page rendering based on session state
def router():
    page = st.session_state.page

    if page.startswith("industry/"):
        sub_industry = page.split("/")[-1]
        render_sub_industry_page(sub_industry)
    else:
        main()

# Run the app
if __name__ == "__main__":
    router()