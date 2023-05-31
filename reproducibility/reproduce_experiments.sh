pip3 install -r requirements.txt

# Run Python script for populating data files for all datasets
python3 reproducibility/collect_data.py

# Run python scripts for descriptive analysis
python3 analysis/generate_split_analysis_plots.py
python3 analysis/generate_bias_plots.py
python3 analysis/generate_relation_pie_charts.py  
python3 analysis/generate_network_plots.py  

# Run python scripts for prediction analysis
python3 experiments/train_models.py
python3 experiments/prediction_analysis.py
python3 analysis/generate_prediction_plots.py