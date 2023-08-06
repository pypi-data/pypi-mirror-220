#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The auto tuning strategy."""
from copy import deepcopy
from .strategy import strategy_registry, TuneStrategy, STRATEGIES
from ..utils import logger

@strategy_registry
class AutoTuneStrategy(TuneStrategy):
    """The auto tuning strategy.

    There are three stages executed by auto strategy sequentially,
    and the tuning process ends once the condition meets the exit policy.
    """

    def __init__(self,
                 model,
                 conf,
                 q_dataloader=None,
                 q_func=None,
                 eval_func=None,
                 eval_dataloader=None,
                 eval_metric=None,
                 resume=None,
                 q_hooks=None):
        """Init an auto tuning strategy.

        Args:
            model: The FP32 model specified for low precision tuning.
            conf: The Conf class instance includes all user configurations.
            q_dataloader: Data loader for calibration, mandatory for post-training quantization.  Defaults to None.
            q_func: Training function for quantization aware training. Defaults to None. Defaults to None.
            eval_func: The evaluation function provided by user. This function takes model as parameter, and
                evaluation dataset and metrics should be encapsulated in this function implementation and
                outputs a higher-is-better accuracy scalar value.
            eval_dataloader: Data loader for evaluation. Defaults to None.
            eval_metric: Metric for evaluation. Defaults to None.
            resume: The dict containing resume information. Defaults to None.
            q_hooks: The dict of training hooks, supported keys are: on_epoch_begin, on_epoch_end, on_step_begin,
                on_step_end. Their values are functions to be executed in adaptor layer.. Defaults to None.
        """
        super().__init__(model=model,
                         conf=conf,
                         q_dataloader=q_dataloader,
                         q_func=q_func,
                         eval_func=eval_func,
                         eval_dataloader=eval_dataloader,
                         eval_metric=eval_metric,
                         resume=resume,
                         q_hooks=q_hooks)
        logger.info(f"*** Initialize auto tuning")
        self.strategies_sequence = ['conservative', 'basic']

    def sequential_traverse(self):
        """Try different strategies sequentially."""
        pre_strategy = self
        for strategy_name in self.strategies_sequence:
            logger.info(f"*** Start {strategy_name} tuning.")
            strategy = STRATEGIES[strategy_name](
                model = self.model,
                conf = self.conf,
                q_dataloader=self.calib_dataloader,
                q_func=self.q_func,
                eval_func=self.eval_func,
                eval_dataloader=self.eval_dataloader,
                eval_metric=self.eval_metric,
                resume=self._resume,
                q_hooks=self.q_hooks,
                pre_strategy = pre_strategy
                )

            pre_strategy = strategy
            strategy.traverse()
            self.best_qmodel = strategy.best_qmodel
            if self.best_qmodel:
                return

    def next_tune_cfg(self):
        """Generate and yield the default tuning config.

        Returns:
            tune_config (dict): A dict containing the tuning configuration for quantization.
        """
        tuning_space = self.tuning_space
        calib_sampling_size_lst = tuning_space.root_item.get_option_by_name('calib_sampling_size').options
        _, _, op_tuning_cfg = self.initial_tuning_cfg()
        op_tuning_cfg['calib_sampling_size'] = calib_sampling_size_lst[0]
        logger.info(f"Quantize the model with default config.")
        yield op_tuning_cfg

    def traverse(self):
        """Traverse the tuning space."""
        # Quantize model with default config
        super().traverse()
        if self.best_qmodel:
            return
        else:
            # Start to try different strategies sequentially
            self.sequential_traverse()