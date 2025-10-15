import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import io

# Page configuration
st.set_page_config(
    page_title="Urban Liability Index Dashboard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
.main-header {
    color: #1f4e79;
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1rem;
}

.sub-header {
    color: #2c5aa0;
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
}

.metric-container {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
}

.info-box {
    background-color: #e8f4ff;
    padding: 1rem;
    border-left: 4px solid #2c5aa0;
    margin: 1rem 0;
    border-radius: 5px;
}

.sidebar-content {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}

.data-table {
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# Load data directly from string (embedded data)
@st.cache_data
def load_data():
    """Load the urban livability data"""
    csv_data = """year,city,pm2.5,pm10,no2,so2,population,area,bpl_population,aqi,pdi,hi,bpl_index,livability_index
2019,Bangalore,33.31,66.0,31.88,4.12,11883000,800.0,57.58,0.7089,0.0000,0.7469,0.4242,46.999
2020,Bangalore,30.39,66.07,30.51,5.53,12033000,800.0,57.58,0.7115,0.0000,0.7626,0.4242,47.459
2021,Bangalore,27.99,88.73,45.14,2.96,12183000,800.0,57.58,0.6596,0.0000,0.7749,0.4242,46.465
2022,Bangalore,37.65,78.59,27.6,3.55,12333000,800.0,55.67,0.6992,0.0000,0.7266,0.4433,46.728
2023,Bangalore,32.23,104.11,34.9,5.79,12483000,800.0,55.67,0.6440,0.0000,0.7786,0.4433,46.648
2019,Chennai,41.09,56.83,24.12,9.34,10711000,1189.2,41.43,0.6925,0.0993,0.6714,0.5857,51.222
2020,Chennai,39.67,69.77,29.85,8.15,10831000,1189.2,41.43,0.6694,0.0892,0.7101,0.5857,51.360
2021,Chennai,30.62,84.28,21.57,10.73,10951000,1189.2,41.43,0.6836,0.0791,0.6959,0.5857,51.108
2022,Chennai,43.75,85.76,23.9,5.61,11071000,590.41,41.43,0.6737,0.0000,0.7479,0.5857,50.182
2023,Chennai,44.86,67.52,40.94,10.83,11191000,590.41,41.43,0.6078,0.0000,0.8285,0.5857,50.551
2019,Delhi,101.55,189.89,60.32,22.7,29399000,1483.3,33.43,0.3694,0.0000,0.7078,0.6657,43.068
2020,Delhi,95.14,188.41,51.75,17.17,29599000,1483.3,33.43,0.3994,0.0000,0.7342,0.6657,44.984
2021,Delhi,105.95,168.67,52.02,15.33,29799000,1483.3,33.43,0.3335,0.0000,0.7017,0.6657,42.527
2022,Delhi,101.98,209.93,49.52,18.94,29999000,1483.3,33.43,0.3439,0.0000,0.7754,0.6657,44.555
2023,Delhi,94.38,167.78,57.29,13.42,30199000,1483.3,33.43,0.4167,0.0000,0.7248,0.6657,44.546
2019,Kolkata,46.78,96.61,35.84,9.57,14850000,1886.67,56.78,0.6018,0.5812,0.7305,0.4322,58.589
2020,Kolkata,55.24,95.77,38.35,14.29,14950000,1886.67,56.78,0.5634,0.5797,0.7310,0.4322,57.617
2021,Kolkata,52.68,116.03,44.75,12.55,15050000,1886.67,56.78,0.5450,0.5782,0.7419,0.4322,57.361
2022,Kolkata,49.07,127.48,39.83,10.0,15150000,1886.67,56.78,0.5913,0.5766,0.7463,0.4322,58.640
2023,Kolkata,57.51,108.06,42.71,15.42,15250000,1886.67,56.78,0.5497,0.5751,0.7796,0.4322,58.434
2019,Mumbai,35.78,75.85,37.4,6.59,20411000,603.4,45.23,0.7026,0.0000,0.7239,0.5477,49.331
2020,Mumbai,47.31,75.76,45.19,13.83,20591000,603.4,45.23,0.6305,0.0000,0.7413,0.5477,48.782
2021,Mumbai,38.35,107.39,35.77,10.81,20771000,603.4,45.23,0.6455,0.0000,0.7459,0.5477,48.453
2022,Mumbai,45.36,99.96,49.24,8.12,20951000,603.4,45.23,0.6349,0.0000,0.7539,0.5477,48.440
2023,Mumbai,52.1,104.93,34.37,11.84,21131000,603.4,45.23,0.6052,0.0000,0.7847,0.5477,48.424"""
    
    return pd.read_csv(io.StringIO(csv_data))

# Initialize data
df = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
pages = ["🏠 Home", "📊 City Analysis", "🔄 City Comparison", "📈 Visualizations", "🏆 Leaderboard", "ℹ️ About"]
selected_page = st.sidebar.selectbox("Select Page", pages)

# Home Page
if selected_page == "🏠 Home":
    st.markdown("<h1 class='main-header'>🏙️ Urban Livability Index — Interactive Dashboard</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
    This dashboard presents an interactive analysis of urban livability (2019–2023) for selected Indian cities. 
    It computes a composite Livability Index from sub-indices: <strong>Air Quality (AQI)</strong>, 
    <strong>Population Density (PDI)</strong>, <strong>Health Index (HI)</strong> and <strong>Poverty Index (BPL)</strong>. 
    Use the pages in the sidebar to explore city-level trends, comparisons, visualizations, and the leaderboard.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Dataset:")
    
    # Display sample data table
    display_df = df.head(12).copy()
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Quick overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Cities Analyzed", len(df['city'].unique()))
    
    with col2:
        st.metric("Years Covered", f"{df['year'].min()}-{df['year'].max()}")
    
    with col3:
        st.metric("Total Records", len(df))
    
    with col4:
        avg_livability = df['livability_index'].mean()
        st.metric("Avg Livability Index", f"{avg_livability:.1f}")

# City Analysis Page
elif selected_page == "📊 City Analysis":
    st.markdown("<h1 class='main-header'>📊 City-wise Analysis</h1>", unsafe_allow_html=True)
    
    # City and year selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_city = st.selectbox("Select City", df['city'].unique(), key="city_analysis")
    
    with col2:
        years_range = st.select_slider(
            "Year Range", 
            options=list(range(2019, 2024)),
            value=(2019, 2023),
            key="year_range"
        )
    
    # Filter data
    city_data = df[
        (df['city'] == selected_city) & 
        (df['year'] >= years_range[0]) & 
        (df['year'] <= years_range[1])
    ].sort_values('year')
    
    if not city_data.empty:
        latest_data = city_data.iloc[-1]
        
        # Overview section
        st.markdown(f"### Overview — {selected_city} ({years_range[0]} to {years_range[1]})")
        
        # Current metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class='metric-container'>
                <h4>Livability Index (latest)</h4>
                <h2 style='color: #2c5aa0;'>{latest_data['livability_index']:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-container'>
                <h4>AQI</h4>
                <h2 style='color: #e74c3c;'>{latest_data['aqi']:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-container'>
                <h4>PDI</h4>
                <h2 style='color: #f39c12;'>{latest_data['pdi']:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='metric-container'>
                <h4>HI</h4>
                <h2 style='color: #27ae60;'>{latest_data['hi']:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
            <div class='metric-container'>
                <h4>BPL Index</h4>
                <h2 style='color: #8e44ad;'>{latest_data['bpl_index']:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Trends")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Livability trend
            fig1 = px.line(
                city_data, 
                x='year', 
                y='livability_index',
                title=f"{selected_city} — Livability Index Trend",
                markers=True
            )
            fig1.update_layout(height=400)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Sub-indices comparison
            sub_indices_data = []
            for _, row in city_data.iterrows():
                sub_indices_data.extend([
                    {'year': row['year'], 'subindex': 'aqi', 'value': row['aqi']},
                    {'year': row['year'], 'subindex': 'pdi', 'value': row['pdi']},
                    {'year': row['year'], 'subindex': 'hi', 'value': row['hi']},
                    {'year': row['year'], 'subindex': 'bpl_index', 'value': row['bpl_index']}
                ])
            
            sub_df = pd.DataFrame(sub_indices_data)
            
            fig2 = px.line(
                sub_df,
                x='year',
                y='value',
                color='subindex',
                title=f"{selected_city} — Sub-indices",
                markers=True
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Data table
        st.markdown("### Data table (filtered)")
        display_columns = ['year', 'city', 'pm2.5', 'pm10', 'no2', 'so2', 'population', 'area', 'bpl_population']
        st.dataframe(city_data[display_columns], use_container_width=True, hide_index=True)

# City Comparison Page
elif selected_page == "🔄 City Comparison":
    st.markdown("<h1 class='main-header'>🔄 City Comparison</h1>", unsafe_allow_html=True)
    
    # Controls
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_cities = st.multiselect(
            "Select Cities to Compare",
            df['city'].unique(),
            default=['Bangalore', 'Chennai'],
            key="comparison_cities"
        )
        
        if st.button("Clear all"):
            st.rerun()
    
    with col2:
        comparison_year = st.selectbox("Select Year", df['year'].unique(), index=0)
    
    if selected_cities:
        # Filter data
        comparison_data = df[
            (df['city'].isin(selected_cities)) & 
            (df['year'] == comparison_year)
        ]
        
        if not comparison_data.empty:
            st.markdown(f"### Livability Index Comparison — {comparison_year}")
            
            # Main comparison chart
            fig1 = px.bar(
                comparison_data,
                x='city',
                y='livability_index',
                title=f"Livability Index ({comparison_year}) - Comparison",
                color='livability_index',
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            st.markdown("### Sub-indices comparison (AQI, PDI, HI, BPL)")
            
            # Sub-indices comparison
            sub_indices_comp = []
            for _, row in comparison_data.iterrows():
                sub_indices_comp.extend([
                    {'city': row['city'], 'subindex': 'aqi', 'value': row['aqi']},
                    {'city': row['city'], 'subindex': 'pdi', 'value': row['pdi']},
                    {'city': row['city'], 'subindex': 'hi', 'value': row['hi']},
                    {'city': row['city'], 'subindex': 'bpl_index', 'value': row['bpl_index']}
                ])
            
            sub_comp_df = pd.DataFrame(sub_indices_comp)
            
            fig2 = px.bar(
                sub_comp_df,
                x='city',
                y='value',
                color='subindex',
                title=f"Sub-indices Comparison ({comparison_year})",
                barmode='group'
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # Comparison table
            st.markdown("### Table")
            display_columns = ['year', 'city', 'pm2.5', 'pm10', 'no2', 'so2', 'population', 'area', 'bpl_population']
            st.dataframe(comparison_data[display_columns], use_container_width=True, hide_index=True)

# Visualizations Page
elif selected_page == "📈 Visualizations":
    st.markdown("<h1 class='main-header'>📈 Visualization Dashboard (6 Figures)</h1>", unsafe_allow_html=True)
    
    # 1. Livability Index Trends
    st.markdown("## 1. Livability Index Trends (2019–2023)")
    
    fig1 = px.line(
        df,
        x='year',
        y='livability_index',
        color='city',
        title="Livability Index Trends (2019–2023)",
        markers=True
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("""
    **Result:** The line plot presents the temporal variation of the livability index for all five cities.
    
    **Discussion:** Chennai shows high and stable scores; Bangalore and Mumbai are mid-range; 
    Delhi and Kolkata show lower scores historically, with Kolkata improving recently.
    """)
    
    # 2. Livability Heatmap
    st.markdown("## 2. Livability Heatmap")
    
    heatmap_data = df.pivot(index='city', columns='year', values='livability_index')
    
    fig2 = px.imshow(
        heatmap_data,
        title="Livability Index Heatmap (2019–2023)",
        aspect="auto",
        color_continuous_scale="RdYlBu_r"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("""
    **Result:** The heatmap displays comparative livability values across cities and years.
    
    **Discussion:** Highlights inter-city disparities and temporal improvements (e.g., Kolkata).
    """)
    
    # 3. Radar Chart
    st.markdown("## 3. Radar Chart — Sub-indices (AQI, PDI, HI, BPL)")
    
    col1, col2 = st.columns(2)
    with col1:
        radar_city = st.selectbox("Select City", df['city'].unique(), key="radar_city")
    with col2:
        radar_year = st.selectbox("Select Year", df['year'].unique(), key="radar_year")
    
    radar_data = df[(df['city'] == radar_city) & (df['year'] == radar_year)]
    
    if not radar_data.empty:
        row = radar_data.iloc[0]
        categories = ['AQI', 'PDI', 'HI', 'BPL_index']
        values = [row['aqi'], row['pdi'], row['hi'], row['bpl_index']]
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # Close the polygon
            theta=categories + [categories[0]],
            fill='toself',
            name=f"{radar_city} {radar_year}"
        ))
        
        fig3.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title=f"Sub-indices Radar – {radar_city} ({radar_year})"
        )
        
        st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown("""
        **Result:** Radar shows relative strengths/weaknesses across sub-indices.
        
        **Discussion:** Use this to interpret the drivers of a city's overall score.
        """)
    
    # 4. Grouped Bar Chart
    st.markdown("## 4. City-wise Livability by Year (Grouped Bar)")
    
    fig4 = px.bar(
        df,
        x='year',
        y='livability_index',
        color='city',
        title="City-wise Livability Index by Year",
        barmode='group'
    )
    st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("""
    **Result:** Grouped bars show inter-city rank per year.
    
    **Discussion:** Useful to compare yearly ranking and see changes across time.
    """)
    
    # 5. Box Plot
    st.markdown("## 5. Distribution of Livability (Boxplot)")
    
    fig5 = px.box(
        df,
        x='city',
        y='livability_index',
        title="Distribution of Livability Index (2019–2023)"
    )
    st.plotly_chart(fig5, use_container_width=True)
    
    st.markdown("""
    **Result:** Boxplot summarizes distribution of scores for each city.
    
    **Discussion:** Highlights stability/variability across years for each city.
    """)
    
    # 6. Sub-indices Comparison
    st.markdown("## 6. Sub-Indices Comparison (Choose Year)")
    
    comparison_year = st.selectbox("Select Year", df['year'].unique(), key="sub_indices_year")
    
    year_data = df[df['year'] == comparison_year]
    
    sub_indices_data = []
    for _, row in year_data.iterrows():
        sub_indices_data.extend([
            {'city': row['city'], 'subindex': 'aqi', 'value': row['aqi']},
            {'city': row['city'], 'subindex': 'pdi', 'value': row['pdi']},
            {'city': row['city'], 'subindex': 'hi', 'value': row['hi']},
            {'city': row['city'], 'subindex': 'bpl_index', 'value': row['bpl_index']}
        ])
    
    sub_df = pd.DataFrame(sub_indices_data)
    
    fig6 = px.bar(
        sub_df,
        x='city',
        y='value',
        color='subindex',
        title=f"Sub-indices Comparison ({comparison_year})",
        barmode='group'
    )
    st.plotly_chart(fig6, use_container_width=True)
    
    st.markdown("""
    **Result:** Bar chart compares the four sub-indices across cities for the selected year.
    
    **Discussion:** Identifies which sub-index drives differences in overall livability.
    """)

# Leaderboard Page
elif selected_page == "🏆 Leaderboard":
    st.markdown("<h1 class='main-header'>🏆 Leaderboard — Average Livability (2019–2023)</h1>", unsafe_allow_html=True)
    
    # Calculate average livability by city
    leaderboard = df.groupby('city')['livability_index'].mean().sort_values(ascending=False).reset_index()
    leaderboard['rank'] = range(1, len(leaderboard) + 1)
    
    st.markdown("### City ranking (average Livability Index)")
    
    # Display leaderboard table
    st.dataframe(leaderboard, use_container_width=True, hide_index=True)
    
    # Leaderboard chart
    fig = px.bar(
        leaderboard,
        x='city',
        y='livability_index',
        title="Average Livability Index (2019–2023)",
        color='livability_index',
        color_continuous_scale='viridis'
    )
    
    # Add rank annotations
    for i, row in leaderboard.iterrows():
        fig.add_annotation(
            x=row['city'],
            y=row['livability_index'] + 1,
            text=f"#{row['rank']}",
            showarrow=False,
            font=dict(size=14, color="black")
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Result:** Ranked list of cities by average livability across the study period.
    
    **Discussion:** The leaderboard helps summarize which cities consistently perform well 
    and which require targeted policy interventions.
    """)

# About Page
elif selected_page == "ℹ️ About":
    st.markdown("<h1 class='main-header'>ℹ️ About this Project</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    **Project Title:** Data analysis of livable conditions in selected Indian cities based on Sustainable Development Goals
    
    **Team:** Urban Analytics Research Group
    
    **SDGs addressed:**
    
    • **SDG 1** — No poverty  
    • **SDG 3** — Good health and well-being  
    • **SDG 11** — Sustainable cities & communities
    
    **Methodology:**
    
    • Data were compiled for five cities Chennai, Bangalore, Mumbai, Delhi and Kolkata for the years 2019 to 2023.  
    • **Indicators:** PM2.5, PM10, NO2, SO2, Population, Area, Below Poverty Line %, Infant Mortality Rate, Life Expectancy.  
    • **Sub-indices computed:** Air Quality Index, Population Density Index, Health Index, Below Poverty Line Index.  
    • **Composite livability index** = mean(AQI, PDI, HI, BPL_index) scaled 0–100.
    
    **Usage:**
    
    Use the **City Analysis** page to inspect a single city, **Comparison** to compare multiple cities, 
    **Visualizations** for figures used in the journal paper, and **Leaderboard** for ranking of cities 
    based on urban livability index.
    
    ---
    
    ### Technical Details
    
    **Data Sources:**
    - Air quality data: Central Pollution Control Board (CPCB)
    - Population data: Census of India
    - Socio-economic indicators: Ministry of Statistics and Programme Implementation
    
    **Index Calculation:**
    
    1. **Air Quality Index (AQI)**: Normalized inverse pollution levels (0-1 scale)
    2. **Population Density Index (PDI)**: Inverse population density metric (0-1 scale)  
    3. **Health Index (HI)**: Healthcare infrastructure and outcomes (0-1 scale)
    4. **BPL Index**: Inverse below poverty line percentage (0-1 scale)
    
    Final Livability Index = (AQI + PDI + HI + BPL_index) ÷ 4 × 100
    
    **Framework:** Built with Streamlit, Pandas, and Plotly for interactive data visualization.
    """)
    
    # Additional metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Data Points", len(df))
    
    with col2:
        st.metric("Years Analyzed", f"{df['year'].max() - df['year'].min() + 1}")
    
    with col3:
        st.metric("Cities Covered", len(df['city'].unique()))

# Footer
st.markdown("---")
st.markdown("**Urban Livability Index Dashboard** | Built with ❤️ using Streamlit | Data period: 2019-2023")
