![Python](https://img.shields.io/badge/Python-3.12.11-blue)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)
![Prophet](https://img.shields.io/badge/Forecasting-Prophet-green)
![License](https://img.shields.io/badge/License-MIT-black)

## **Pop Culture Buzz Predictor**
Forecasting tomorrow’s trends, today.

--- 
## **Project Overview**

*Problem statement:*

Marketers, creators, and brands often react late to cultural trends because existing platforms only show what is already popular. There is a lack of tools that can forecast upcoming spikes in popularity, making it difficult to anticipate audience engagement in advance.

*Solution Statement:*

Developed a **Pop Culture Buzz Predictor** that integrates Google Trends data to forecast trend spikes three weeks in advance. The interactive Streamlit dashboard lets users enter any keyword (artist, show, or song) and instantly see historical popularity and spikes along with predicted future buzz, enabling timely decisions for marketers and creators. Popularity trends and dynamic insights are also included.

*Scope:*
- Detect buzz spikes in artists, shows, and songs.
- Visualize long-term vs. short-term popularity.
- Forecast upcoming engagement with Prophet.
- Deliver insights via an interactive Streamlit dashboard.

This makes trend anticipation actionable, helping brands and marketers plan campaigns, product launches, and cross-promotions strategically.

--- 


## **Tech Stack & Tools**

- Python → data collection, cleaning, analysis
- Pandas / NumPy → wrangling & transformations
- Matplotlib / Seaborn / Plotly → visualization
- PyTrends (Google Trends API) → trend data collection
- Prophet → time-series forecasting
- Streamlit → interactive dashboard for end-users
---


## **Project Workflow**

- Data Collection → Pulled Google Trends, normalized with anchor keyword.
- Data Cleaning → Interpolated missing values, smoothed noise, weekly resample.
- Exploratory Data Analysis → Weekly trends, correlations, spike detection.
- Forecasting → Prophet predictions with confidence intervals.
- Dashboard → Interactive Streamlit app with spike markers + insights.
---


## **Key Insights**

- Taylor Swift → Highest baseline popularity, but large event-driven fluctuations.
- BTS & Blackpink → Strong correlation (r=0.81), reflecting shared K-pop fanbase cycles.
- Rihanna → Huge mid-2025 spike tied to album rumors + Met Gala appearance.
- Stranger Things & Jenna Ortega → Buzz moves in tandem, aligned with Netflix release dates.
--- 


 ## **Business Value**

This tool helps stakeholders:
- Strategically time releases → Align drops with high-buzz windows (e.g., November-December).
- Leverage cross-promotions → Use correlated entities for joint campaigns.
- Manage volatility → Smooth audience dips with sustained engagement strategies.
- Capitalize on spikes → Deploy moment marketing when cultural shocks hit.
- Plan global campaigns → Use data-driven forecasts for worldwide fanbases.
--- 


## **Dashboard Preview**

- Buzz Spikes View <img width="1913" height="1012" alt="Screenshot 2025-09-07 190113" src="https://github.com/user-attachments/assets/df57a1a5-550b-4ebd-9ec9-78a6c8cd2117" />

- Forecast View <img width="1918" height="1025" alt="9" src="https://github.com/user-attachments/assets/d6b744d9-9dfe-4d46-85be-bc4c0daaa763" />

- Relative Share View <img width="1918" height="1013" alt="10" src="https://github.com/user-attachments/assets/530489b1-17b0-4700-9b39-667bd0a5d84b" />
---


## **Project Structure** 

```
├── data/
│ ├── raw/ # Raw Google Trends pulls
│ ├── google_trends_clean.csv # Cleaned + smoothed data
│ ├── google_trends_spike_flags.csv
│ ├── forecasts_prophet/ # Forecast outputs
│
├── app.py # Streamlit dashboard
├── pop_culture_buzz_predictor.py # Main data pipeline
├── README.md # This file
```
--- 


## **Quick Start**

```
# Clone repo
git clone https://github.com/yourusername/pop-culture-buzz-predictor.git
cd pop-culture-buzz-predictor

# Install dependencies
pip install -r requirements.txt

# Run pipeline
python src/pop_culture_buzz_predictor.py

# Launch dashboard
streamlit run app/app.py

```
---



## **Use Cases:**
- The project is domain-agnostic. It doesn’t matter if the keyword is a singer, a product, a festival, or a meme.
- Marketers → Forecast campaign buzz (e.g., “Diwali Sale”).
- Content Creators → Spot trending formats (e.g., “AI memes”).
- Brands → Benchmark competitors (e.g., “Coke vs. Pepsi”).
- Event Planners → Anticipate audience hype (“Comic Con”).
---



## **Future Improvements**
- Add YouTube/Spotify API integration for richer signals.
- Use sentiment analysis from Twitter/Reddit alongside trends.
- Deploy as a full web app with user accounts + saved reports.
---


## **Conclusion:**

Pop Culture Buzz Predictor transforms raw search data into actionable insights. It’s not just a project— it’s a universal trend radar for marketers, creators, and brands.
