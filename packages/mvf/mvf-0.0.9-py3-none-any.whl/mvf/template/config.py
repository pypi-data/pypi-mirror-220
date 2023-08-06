import yaml
import os


class ConfigBuilder:
    config = {
        'data': {
            'source': 'path_to_your_source_code',
            'split': 'train_test',
            'test_size': 0.3,
        },
        'models': [
            {
                'name': 'your_model_name',
                'lang': 'Python',
                'validation_step': False,
            },
        ],
    }

    def __init__(self, pth):
        '''
        pth - path to MVF project.
        '''
        # make project dir if not already exists
        if not os.path.exists(pth):
            os.makedirs(pth)
        # construct path to config file
        self.config_path = os.path.join(
            pth,
            'mvf_conf.yaml',
        )
        if os.path.isfile(self.config_path):
            with open(self.config_path, 'r') as f:
                existing_config = yaml.safe_load(f)
            self.config.update(existing_config)

    def write(self):
        with open(self.config_path, 'w') as f:
            yaml.safe_dump(self.config, f, default_flow_style=False)
