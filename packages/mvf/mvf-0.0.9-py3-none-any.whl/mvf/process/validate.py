# # Comparative Model Validation

# # Comparative Model Validation

# imports
import os
import feather
import pandas
from IPython.display import display
import pickle
import sklearn.metrics as error_metrics

# + tags=["parameters"]
upstream = None
product = None
models = []
split_type = ''
n_folds = 10
quantile_intervals = []
# -

# format variable
upstream = dict(upstream)

# ## Load predictions and ground truth

# load ground truth data from upstream
if split_type == 'train_test':
    ground_truth = feather.read_dataframe(upstream['split_data']['test_y_data']).reset_index(drop=True)
elif split_type == 'k_fold':
    ground_truth = []
    for i in range(1, n_folds+1):   
        ground_truth.append(
            feather.read_dataframe(upstream['split_data'][f'fold_{i}_y_data'])
        )
    ground_truth = pandas.concat(ground_truth).reset_index(drop=True)
del upstream['split_data']

# load predictions from upstream
predictions = {}
for model_name in models:
    predictions[model_name] = feather.read_dataframe(
        upstream[f'{model_name}_predict']['predictions']
    ).reset_index(drop=True)

# ## Error Metrics
# The error metrics reported are
# * MSE - Mean squared error
# * RMSE - Root mean squared error
# * MAE - Mean absolute error
# * MAPE - Mean absolute percentage error
# * R-squared - Coefficient of determination

# error
error_df = pandas.DataFrame()
# mse
for model, preds in predictions.items():
    mean_preds = preds['predictions']
    error_df.loc[model, 'MSE'] = error_metrics.mean_squared_error(ground_truth, mean_preds)
    error_df.loc[model, 'RMSE'] = error_metrics.mean_squared_error(ground_truth, mean_preds, squared=False)
    error_df.loc[model, 'MAE'] = error_metrics.mean_absolute_error(ground_truth, mean_preds)
    error_df.loc[model, 'MAPE'] = error_metrics.mean_absolute_percentage_error(ground_truth, mean_preds)
    error_df.loc[model, 'R-squared'] = error_metrics.r2_score(ground_truth, mean_preds)
error_df

# ## Quantile interval coverage
# For each of the intervals defined in `quantile_intervals`, what proportion of predicted values fall within the interval?

# quantile interval coverage
qi_coverage = pandas.DataFrame()
idx = 0
for model, preds in predictions.items():
    for qi in quantile_intervals:
        lb = 'Q' + f'{min(qi) * 100:g}'
        ub = 'Q' + f'{max(qi) * 100:g}'
        if lb in preds.columns and ub in preds.columns:
            qi_coverage.loc[idx, 'model'] = model
            qi_coverage.loc[idx, 'interval'] = str(sorted(qi))
            qi_coverage.loc[idx, 'level'] = max(qi) - min(qi)
            # boolean array for qi covering ground truth
            in_interval = (preds[ub] >= ground_truth.iloc[:, 0]) & (preds[lb] <= ground_truth.iloc[:, 0])
            qi_coverage.loc[idx, 'coverage'] = in_interval.sum() / in_interval.shape[0]
            idx += 1
try:
    display(qi_coverage.set_index(['model', 'interval']))
except KeyError:
    print('No quantile intervals specified. Nothing to calculate.')

# ## Model Sharpness
# How uncertain is the model? `sharpness` of a quantile interval is defined as the average width of the interval across all predictions.

# quantile interval sharpness
qi_sharpness = pandas.DataFrame()
for model, preds in predictions.items():
    for qi in quantile_intervals:
        lb = 'Q' + f'{min(qi) * 100:g}'
        ub = 'Q' + f'{max(qi) * 100:g}'
        if lb in preds.columns and ub in preds.columns:
            qi_sharpness.loc[model, str(sorted(qi))] = (preds[ub] - preds[lb]).mean()
qi_sharpness

# ## Computational performance
# Record
# * the total size in bytes of the fit model(s).
# * the total time taken to fit the model(s).
# * the total time taken for the model(s) to predict.

# computational performance
comp_perf = pandas.DataFrame()
for model in models:
    # fit time
    with open(upstream[f'{model}_fit']['process_metadata'], 'rb') as f:
        fit_metadata = pickle.load(f)
    comp_perf.loc[model, 'fit time'] = fit_metadata[f'{model}_fit']
    # predict time
    with open(upstream[f'{model}_predict']['process_metadata'], 'rb') as f:
        predict_metadata = pickle.load(f)
    comp_perf.loc[model, 'predict time'] = predict_metadata[f'{model}_predict']
    # model size
    if split_type == 'train_test':
        # only one model
        comp_perf.loc[model, 'size'] = os.path.getsize(
            os.path.join(
                'output',
                'models',
                f'{model}_fit'
            )
        )
    elif split_type == 'k_fold':
        # sum the model sizes
        total_size = 0
        for i in range(1, n_folds+1):
            total_size += os.path.getsize(
                os.path.join(
                    'output',
                    'models',
                    f'{model}_fit_{i}' 
                )
            )
        comp_perf.loc[model, 'size'] = total_size
comp_perf