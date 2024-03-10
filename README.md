## Objectives 🎯
The objectives of this project are gaining descriptive information and finding the "why's" from the data. To obtain such objectives, 
there are two outputs of this project: 

<a href="https://colab.research.google.com/drive/15hujoJHjhT_T93XSk5qri5erxF6oAxpJ#scrollTo=kYarLAzOVOA0"><img align="left" src="https://github.com/raflidzaky/2024-March-stock_market_analysis/assets/104545005/3827e863-b0f8-437d-b29e-979c034f1350" alt="Google Colab Project" width="21px"/></a>  [**Google Colab Notebook**](https://colab.research.google.com/drive/15hujoJHjhT_T93XSk5qri5erxF6oAxpJ#scrollTo=kYarLAzOVOA0)

This colab notebook contains detailed thought process (raw code), descriptive statistics, and logical reasoning why certain occurences occur. 
You can see analyzing_stock_market_project.py for raw code only (without outputs)


<a href="https://2024-march-stockmarketanalysis.streamlit.app/"><img align="left" src="https://github.com/raflidzaky/2024-March-stock_market_analysis/assets/104545005/81af49e7-1a07-4e61-8404-3b864343b6e3" alt="Google Colab Project" width="21px"/></a>  [**Streamlit Dashboard**](https://2024-march-stockmarketanalysis.streamlit.app/)

While this Streamlit Dashboard will interactively show trends of specified timeframe and columns. You can use given .csv file in this branch as an input for dashboard.

## Tech stacks
![](https://img.shields.io/badge/Language-Python-informational?style=flat&logo=Python&color=FFD700)
</br>
![](https://img.shields.io/badge/Lib-Pandas-informational?style=flat&logo=Pandas&color=FFA500)
![](https://img.shields.io/badge/Lib-Plotly-informational?style=flat&logo=Plotly&color=FFC0CB)
![](https://img.shields.io/badge/Lib-Streamlit-informational?style=flat&logo=Streamlit&color=FF0000)
</br>

**Notes:** Pandas are used as it accounts for [Bessel Correction](https://www.statisticshowto.com/bessels-correction/) on its standar deviation calculation. Thus, it 
fits for this project context that uses sample data.

## Settings
Several things for consideration: **data set**, **cloning the projects**, and **running engine for dashboard**
### Data set
You can either download ```dataset_full.csv``` (already clean) or follow these steps for raw data (on your Jupyter Notebook or Google Colab):
```
  # Install the yfinance API
  !pip install yfinance

  # Import the library
  import yfinance as yf
  dataset = yf.download('BAC', start='2004-01-01', end='2016-01-01')
  dataset
```
### Cloning the projects
You can clone this project to run locally **using Git**. However, note you do not need to push it in this branch. Just do on your own local environment and push on your own Git branches! :D
```
$git config --local user.name "your-display-name"
$git clone https://github.com/raflidzaky/2024-March-stock_market_analysis
$dir 
$cd 2024-March-stock_market_analysis
```

### Running engine
You need an engine to showcase pre-deployed dashboard. Here's how (you could **write in Jupyter Notebook or Google Colab**)
```
  !pip install streamlit

  # Initialize file for writing streamlit dashboard
  %%writefile whatever_name.py

  # Run streamlit based on the file on whatever_name.py
  # And run it in localtunnel
  !streamlit run whatever_name.py & npx localtunnel --port your_port_number
```
