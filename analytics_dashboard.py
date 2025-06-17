import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_manager import AnalyticsDataManager
import pandas as pd
from datetime import datetime, timedelta
import json

class AnalyticsDashboard:
    def __init__(self):
        self.data_manager = AnalyticsDataManager()
        self.setup_page()

    def setup_page(self):
        st.set_page_config(
            page_title="Real-Time Analytics Dashboard",
            page_icon="📊",
            layout="wide"
        )
        st.title("📊 Real-Time Analytics Dashboard")

    def display_overview_metrics(self):
        analytics = self.data_manager.get_analytics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Active Users",
                analytics['active_users'],
                delta=f"{analytics['active_users'] - analytics.get('previous_active_users', 0)}"
            )
        
        with col2:
            st.metric(
                "Total Visits",
                analytics['total_visits'],
                delta=f"{analytics['total_visits'] - analytics.get('previous_total_visits', 0)}"
            )
        
        with col3:
            st.metric(
                "Avg. Time Spent",
                f"{analytics['average_time']:.1f}s",
                delta=f"{analytics['average_time'] - analytics.get('previous_average_time', 0):.1f}s"
            )
        
        with col4:
            st.metric(
                "Bounce Rate",
                f"{analytics['bounce_rate']:.1f}%",
                delta=f"{analytics['bounce_rate'] - analytics.get('previous_bounce_rate', 0):.1f}%"
            )

    def display_traffic_sources(self):
        st.subheader("Traffic Sources")
        traffic_data = self.data_manager.real_time_data['traffic_sources']
        
        # Create pie chart
        fig = px.pie(
            values=list(traffic_data.values()),
            names=list(traffic_data.keys()),
            title="Traffic Sources Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    def display_geographic_data(self):
        st.subheader("Geographic Distribution")
        geo_data = self.data_manager.real_time_data['geographic_data']
        
        # Create choropleth map
        fig = px.choropleth(
            locations=list(geo_data.keys()),
            locationmode="country names",
            color=list(geo_data.values()),
            title="Visitor Distribution by Country"
        )
        st.plotly_chart(fig, use_container_width=True)

    def display_active_times(self):
        st.subheader("Active Times")
        active_times = self.data_manager.real_time_data['active_times']
        
        # Create line chart
        fig = px.line(
            x=active_times['labels'],
            y=active_times['values'],
            title="Visitor Activity by Hour"
        )
        fig.update_layout(
            xaxis_title="Hour",
            yaxis_title="Active Users"
        )
        st.plotly_chart(fig, use_container_width=True)

    def display_page_engagement(self):
        st.subheader("Page Engagement")
        page_data = self.data_manager.page_engagement
        
        # Create bar chart
        pages = list(page_data.keys())
        views = [data['views'] for data in page_data.values()]
        avg_times = [data['avg_time'] for data in page_data.values()]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=pages,
            y=views,
            name="Page Views"
        ))
        fig.add_trace(go.Bar(
            x=pages,
            y=avg_times,
            name="Avg. Time (s)"
        ))
        
        fig.update_layout(
            title="Page Views and Average Time Spent",
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True)

    def display_device_types(self):
        st.subheader("Device Types")
        device_data = self.data_manager.real_time_data['device_types']
        
        # Create pie chart
        fig = px.pie(
            values=list(device_data.values()),
            names=list(device_data.keys()),
            title="Visitor Device Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    def display_search_visibility(self):
        st.subheader("Search Visibility")
        search_data = self.data_manager.real_time_data['search_visibility']
        
        # Create bar chart for rankings
        rankings = search_data['google_rankings']
        fig = px.bar(
            x=list(rankings.keys()),
            y=list(rankings.values()),
            title="Google Search Rankings"
        )
        fig.update_layout(
            xaxis_title="Search Term",
            yaxis_title="Ranking Position"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display search metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Impressions", search_data['total_impressions'])
        with col2:
            st.metric("Total Clicks", search_data['total_clicks'])
        with col3:
            st.metric("Average Position", f"{search_data['average_position']:.1f}")

    def display_bounce_rates(self):
        st.subheader("Bounce Rates")
        bounce_data = self.data_manager.real_time_data['bounce_rates']
        
        # Create bar chart
        fig = px.bar(
            x=list(bounce_data.keys()),
            y=list(bounce_data.values()),
            title="Bounce Rate by Page"
        )
        fig.update_layout(
            xaxis_title="Page",
            yaxis_title="Bounce Rate (%)"
        )
        st.plotly_chart(fig, use_container_width=True)

    def display_time_spent(self):
        st.subheader("Time Spent")
        time_data = self.data_manager.real_time_data['time_spent']
        
        # Create bar chart
        fig = px.bar(
            x=list(time_data.keys()),
            y=list(time_data.values()),
            title="Average Time Spent by Page"
        )
        fig.update_layout(
            xaxis_title="Page",
            yaxis_title="Time Spent (s)"
        )
        st.plotly_chart(fig, use_container_width=True)

    def display_recent_events(self):
        st.subheader("Recent Events")
        events = self.data_manager.real_time_data['events'][-10:]  # Show last 10 events
        
        if events:
            for event in reversed(events):
                timestamp = datetime.fromtimestamp(event['timestamp'])
                st.write(f"**{timestamp.strftime('%H:%M:%S')}** - {event['type']}: {event.get('data', '')}")
        else:
            st.write("No recent events")

    def run(self):
        self.display_overview_metrics()
        
        # Create two columns for the main layout
        col1, col2 = st.columns(2)
        
        with col1:
            self.display_traffic_sources()
            self.display_geographic_data()
            self.display_active_times()
            self.display_page_engagement()
        
        with col2:
            self.display_device_types()
            self.display_search_visibility()
            self.display_bounce_rates()
            self.display_time_spent()
        
        # Display recent events at the bottom
        self.display_recent_events()
        
        # Auto-refresh every 30 seconds
        st.empty()
        st.button("Refresh Data")

if __name__ == "__main__":
    dashboard = AnalyticsDashboard()
    dashboard.run() 