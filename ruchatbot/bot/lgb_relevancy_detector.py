# -*- coding: utf-8 -*-
"""
28-07-2020 Преобразование входной матрицы в scipy.sparse.csr_matrix перед вызовом predict, чтобы не вылезало
           уродливое предупреждение UserWarning: Converting data to scipy sparse matrix.
"""

import json
import os
import logging
import lightgbm
import scipy

from ruchatbot.bot.gb_relevancy_detector import GB_RelevancyDetector


class LGB_RelevancyDetector(GB_RelevancyDetector):
    """
    Модель для определения релевантности предпосылки и вопроса на базе
    классификатора LightGBM.
    """
    def __init__(self):
        super(LGB_RelevancyDetector, self).__init__()
        self.logger = logging.getLogger('LGB_RelevancyDetector')
        self.x_matrix_type = 'float32'

    def load(self, models_folder):
        self.logger.info('Loading LGB_RelevancyDetector model files')

        with open(os.path.join(models_folder, 'lgb_relevancy.config'), 'r') as f:
            model_config = json.load(f)

        self.init_model_params(model_config)
        model_filepath = os.path.join(models_folder, os.path.basename(model_config['model_filename']))
        self.logger.info(u'Loading LightGBM model from {}'.format(model_filepath))
        self.lgb_relevancy = lightgbm.Booster(model_file=model_filepath)

    def predict_by_model(self, X_data):
        y_pred = self.lgb_relevancy.predict(scipy.sparse.csr_matrix(X_data))
        return y_pred
