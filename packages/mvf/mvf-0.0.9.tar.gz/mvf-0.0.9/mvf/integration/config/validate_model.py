def validate_model_py(product, params):
    import models
    # get model class
    model_class = getattr(models, params['model_name'])
    # init model
    model = model_class()
    # run common checks
    validate_model(product, params, model)


def validate_model_r(product, params):
    import rpy2.robjects as robjects
    import rpy2_r6.r6b as r6b
    # get model class
    r = robjects.r
    r.source('models.R')
    model_class = r6b.R6DynamicClassGenerator(r[params['model_name']])
    # init model
    model = model_class.new()
    # run common checks
    validate_model(product, params, model)

def validate_model(product, params, model):
    assert 'nb' in product, 'The \'nb\' product must be defined.'
    # check the model has a validate method
    assert hasattr(model, 'validate'), f'The model class defined for {params["model_name"]} must have a validate() method.'
    assert callable(getattr(model, 'validate')), f'The model saved at {params["model_name"]} must have a validate() method. The class\' load attribute is not currently callable.'
