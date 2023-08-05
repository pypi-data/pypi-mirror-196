from typing import Dict, List, Tuple

import tvm
from tvm import relax

from .models.unet_2d_condition import TVMUNet2DConditionModel


def detect_available_torch_device() -> str:
    if tvm.metal().exist:
        return "mps"
    elif tvm.cuda().exist:
        return "cuda"
    raise ValueError("At least one GPU backend is expected to be enabled")


def get_unet(pipe, device_str: str):
    model = TVMUNet2DConditionModel(
        sample_size=64, cross_attention_dim=768, device=device_str
    )
    pt_model_dict = pipe.unet.state_dict()
    model_dict = {}
    for name, tensor in pt_model_dict.items():
        if name.endswith("ff.net.0.proj.weight") or name.endswith("ff.net.0.proj.bias"):
            w1, w2 = tensor.chunk(2, dim=0)
            model_dict[name.replace("proj", "proj1")] = w1
            model_dict[name.replace("proj", "proj2")] = w2
            continue
        model_dict[name] = tensor
    model.load_state_dict(model_dict)
    return model


def merge_irmodules(*irmodules: tvm.IRModule) -> tvm.IRModule:
    merged_mod = tvm.IRModule()

    for mod in irmodules:
        for gv, func in mod.functions.items():
            merged_mod[gv] = func
    return merged_mod


def split_transform_deploy_mod(
    mod: tvm.IRModule, model_names: List[str], mod_deploy_entry_func: List[str]
) -> Tuple[tvm.IRModule, tvm.IRModule]:
    mod_transform = tvm.IRModule()
    mod_deploy = tvm.IRModule()

    transform_func_names = [name + "_transform_params" for name in model_names]
    for gv in mod.functions:
        func = mod[gv]
        if isinstance(func, tvm.tir.PrimFunc):
            mod_transform[gv] = func
            mod_deploy[gv] = func
        elif gv.name_hint in transform_func_names:
            mod_transform[gv] = func
        else:
            mod_deploy[gv] = func

    mod_transform = relax.transform.RemoveUnusedFunctions(transform_func_names)(
        mod_transform
    )
    mod_deploy = relax.transform.RemoveUnusedFunctions(mod_deploy_entry_func)(
        mod_deploy
    )

    return mod_transform, mod_deploy


def transform_params(
    mod_transform: tvm.IRModule, model_params: Dict[str, List[tvm.nd.NDArray]]
) -> Dict[str, List[tvm.nd.NDArray]]:
    ex = relax.build(mod_transform, target="llvm")
    vm = relax.vm.VirtualMachine(ex, tvm.cpu())
    new_params = dict()
    for name, params in model_params.items():
        new_params[name] = vm[name + "_transform_params"](params)
    return new_params


def save_params(params: Dict[str, List[tvm.nd.NDArray]], artifact_path: str) -> None:
    from tvm.contrib import tvmjs

    meta_data = {}
    param_dict = {}
    for model in ["unet", "vae", "clip"]:
        meta_data[f"{model}ParamSize"] = len(params[model])
        for i, nd in enumerate(params[model]):
            param_dict[f"{model}_{i}"] = nd
    tvmjs.dump_ndarray_cache(param_dict, f"{artifact_path}/params", meta_data=meta_data)


def load_params(artifact_path: str, device) -> Dict[str, List[tvm.nd.NDArray]]:
    from tvm.contrib import tvmjs

    pdict = {}
    params, meta = tvmjs.load_ndarray_cache(f"{artifact_path}/params", device)
    for model in ["vae", "unet", "clip"]:
        plist = []
        size = meta[f"{model}ParamSize"]
        for i in range(size):
            plist.append(params[f"{model}_{i}"])
        pdict[model] = plist
    return pdict
