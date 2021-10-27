##Follow variable energy prices in the Netherlands

This is a simple Streamlit app where you can follow Dutch variable energy prices for gas and electricity, from 2018 until 2021.

Rates are published monthly by the Statistics Netherlands ([CBS](https://www.cbs.nl/en-gb)). The app uses the Statistics Netherlands opendata API client for Python ([cbsodata](https://pypi.org/project/cbsodata/)).

It also uses [streamlit-echarts](https://github.com/andfanilo/streamlit-echarts) for theming the chart. You can theme your own chart with the ECharts [theme-builder](https://echarts.apache.org/en/theme-builder.html), download/copy the theme and past it in the theme.json file.

The app is deployed on Streamlit with Streamlit Sharing.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/mvs12/cbs-energyrates-streamlit)
