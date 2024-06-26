## Summary
This repository summarizes all the data pipelines, data pre-processing codes, statistical models, descriptive statistics, and plot visualizations from Phase 1 of Mahdavi & Siegel (2020) (AS&ampT)  
Project Milestone: 2017 - 2020  
Full-length article: https://www.tandfonline.com/doi/full/10.1080/02786826.2020.1774492

## The Hidden Story in Our Air Filters

HVAC filters play a dual role in our homes. They not only purify the air we breathe by trapping harmful particles but also act as silent samplers, collecting a record of these airborne contaminants. This makes them a valuable resource for experts in Indoor Air Quality (IAQ), Indoor Environmental Engineering, and Health. By analyzing the dust accumulated on used filters, researchers gain insights into the particles and contaminants we may be inhaling.

This analysis technique is known as Filter Forensics. When combined with metadata from HVAC systems (airflow rate, runtime, filter efficiency), it allows for calculating long-term airborne particle concentrations. This concentration data is crucial for exposure assessments in chronic health studies. This more quantitative approach is termed Quantitative Filter Forensics (QFF).

Dust recovery from residential HVAC filters is a critical step in QFF. Efficient dust extraction significantly improves the accuracy of QFF estimations. Therefore, studying and optimizing this process is essential. Data analysis of extracted dust provides valuable insights for a better understanding of IAQ and the health effects of harmful contaminants.

## This Repository
This repository showcases the data pipelines, pre-processing code, statistical models, descriptive statistics, and visualizations used in Phase 1 of the Mahdavi & Siegel (2020) (AS&T) paper. 
In this phase, filters were artificially loaded with standardized test dust samples in the lab for further extraction experiment processes.
While the paper itself discusses the front-end results, this repository provides the underlying code that generates those results, allowing you to explore the analysis firsthand.

The pre-processing and logical Python codes are provided in .py (originally written in Spyder), and data visualization, statistical models, and front-end calculations are provided in .ipynb (written in Jupyter) for a guided walk-through of the data pipeline process.
