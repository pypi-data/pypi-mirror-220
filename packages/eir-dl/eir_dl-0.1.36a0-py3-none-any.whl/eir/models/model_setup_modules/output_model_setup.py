from typing import TYPE_CHECKING, Dict, Type

import torch

from eir.models.output.linear import LinearOutputModule, LinearOutputModuleConfig
from eir.models.output.mlp_residual import (
    ResidualMLPOutputModule,
    ResidualMLPOutputModuleConfig,
)
from eir.models.output.output_module_setup import TabularOutputModuleConfig
from eir.models.output.sequence.sequence_output_modules import (
    SequenceOutputModule,
    SequenceOutputModuleConfig,
)
from eir.setup.output_setup_modules.sequence_output_setup import (
    ComputedSequenceOutputInfo,
)
from eir.setup.output_setup_modules.tabular_output_setup import (
    al_num_outputs_per_target,
)

if TYPE_CHECKING:
    from eir.models.model_setup_modules.meta_setup import FeatureExtractorInfo

al_output_module_init_configs = (
    ResidualMLPOutputModuleConfig
    | LinearOutputModuleConfig
    | SequenceOutputModuleConfig
)

al_sequence_module_classes = Type[SequenceOutputModule]
al_tabular_module_classes = Type[LinearOutputModule] | Type[ResidualMLPOutputModule]

al_output_module_classes = (
    Type[ResidualMLPOutputModule]
    | Type[LinearOutputModule]
    | Type[SequenceOutputModule]
)
al_output_modules = ResidualMLPOutputModule | LinearOutputModule | SequenceOutputModule


def get_sequence_output_module_from_model_config(
    output_object: ComputedSequenceOutputInfo,
    feature_dimensionalities_and_types: Dict[str, "FeatureExtractorInfo"],
    device: str,
) -> SequenceOutputModule:
    output_model_config = output_object.output_config.model_config
    output_module_type = output_model_config.model_type

    class_map = _get_sequence_output_module_type_class_map()
    cur_output_module_class = class_map[output_module_type]

    output_module = cur_output_module_class(
        output_object=output_object,
        output_name=output_object.output_config.output_info.output_name,
        feature_dimensionalities_and_types=feature_dimensionalities_and_types,
    )

    torch_device = torch.device(device=device)
    output_module = output_module.to(device=torch_device)

    return output_module


def _get_sequence_output_module_type_class_map() -> (
    dict[str, al_sequence_module_classes]
):
    mapping = {
        "sequence": SequenceOutputModule,
    }

    return mapping


def get_tabular_output_module_from_model_config(
    output_model_config: TabularOutputModuleConfig,
    input_dimension: int,
    num_outputs_per_target: "al_num_outputs_per_target",
    device: str,
) -> al_output_modules:
    output_module_type = output_model_config.model_type
    model_init_config = output_model_config.model_init_config

    output_module: al_output_modules
    match output_module_type:
        case "mlp_residual":
            assert isinstance(model_init_config, ResidualMLPOutputModuleConfig)
            output_module = ResidualMLPOutputModule(
                model_config=model_init_config,
                input_dimension=input_dimension,
                num_outputs_per_target=num_outputs_per_target,
            )
        case "linear":
            assert isinstance(model_init_config, LinearOutputModuleConfig)
            output_module = LinearOutputModule(
                model_config=model_init_config,
                input_dimension=input_dimension,
                num_outputs_per_target=num_outputs_per_target,
            )
        case _:
            raise ValueError(f"Invalid output module type: {output_module_type}")

    torch_device = torch.device(device=device)
    output_module = output_module.to(device=torch_device)

    return output_module


def _get_supervised_output_module_type_class_map() -> (
    dict[str, al_tabular_module_classes]
):
    mapping = {
        "mlp_residual": ResidualMLPOutputModule,
        "linear": LinearOutputModule,
    }

    return mapping
