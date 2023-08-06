import pandas
import feather


def predict_model(product, task, params, target_labels=['predictions']):
    if params['split_type'] == 'train_test':
        with open(task.upstream['split_data'].product['test_y_data'], 'rb') as f:
            target_data = feather.read_dataframe(f)
    elif params['split_type'] == 'k_fold':
        target_data = []
        for i in range(1, params['n_folds']+1):
            with open(task.upstream['split_data'].product[f'fold_{i}_y_data'], 'rb') as f:
                target_data.append(
                    feather.read_dataframe(f)
                )
        target_data = pandas.concat(target_data)

    target_shape = target_data.shape
    predictions = feather.read_dataframe(product['predictions'])

    if 'quantile_intervals' in params:
        quantiles = set()
        for interval in params['quantile_intervals']:
            quantiles.update(interval)
        for quantile in quantiles:
            str_quantile = 'Q' + f'{quantile * 100:g}'
            assert str_quantile in predictions.columns, f'{str_quantile} missing from predictions. Columns are {predictions.columns}.'

    try:
        assert target_shape == predictions[target_labels].shape, f'The predictions should have the same shape as the test data. Currently {predictions.shape} and {target_shape}.'
    except KeyError:
        raise Exception(f'{target_labels} are not in the columns. Columns are {predictions.columns}.')
