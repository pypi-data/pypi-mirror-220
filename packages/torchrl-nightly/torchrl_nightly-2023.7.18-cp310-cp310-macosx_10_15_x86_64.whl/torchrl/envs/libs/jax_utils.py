# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import dataclasses
from typing import Union

import jax
import numpy as np
import torch
from jax import dlpack as jax_dlpack, numpy as jnp
from tensordict.tensordict import make_tensordict, TensorDictBase
from torch.utils import dlpack as torch_dlpack
from torchrl.data.tensor_specs import (
    CompositeSpec,
    TensorSpec,
    UnboundedContinuousTensorSpec,
    UnboundedDiscreteTensorSpec,
)
from torchrl.data.utils import numpy_to_torch_dtype_dict


def _tree_reshape(x, batch_size: torch.Size):
    shape, n = batch_size, 1
    return jax.tree_util.tree_map(lambda x: x.reshape(shape + x.shape[n:]), x)


def _tree_flatten(x, batch_size: torch.Size):
    shape, n = (batch_size.numel(),), len(batch_size)
    return jax.tree_util.tree_map(lambda x: x.reshape(shape + x.shape[n:]), x)


_dtype_conversion = {
    np.dtype("uint16"): np.int16,
    np.dtype("uint32"): np.int32,
    np.dtype("uint64"): np.int64,
}


def _ndarray_to_tensor(value: Union[jnp.ndarray, np.ndarray]) -> torch.Tensor:
    # JAX arrays generated by jax.vmap would have Numpy dtypes.
    if value.dtype in _dtype_conversion:
        value = value.view(_dtype_conversion[value.dtype])
    if isinstance(value, jnp.ndarray):
        dlpack_tensor = jax_dlpack.to_dlpack(value)
    elif isinstance(value, np.ndarray):
        dlpack_tensor = value.__dlpack__()
    else:
        raise NotImplementedError(f"unsupported data type {type(value)}")
    out = torch_dlpack.from_dlpack(dlpack_tensor)
    # dtype can be messed up by dlpack
    return out.to(numpy_to_torch_dtype_dict[value.dtype])


def _tensor_to_ndarray(value: torch.Tensor) -> jnp.ndarray:
    return jax_dlpack.from_dlpack(torch_dlpack.to_dlpack(value))


def _get_object_fields(obj) -> dict:
    """Converts an object (named tuple or dataclass or dict) to a dict."""
    if isinstance(obj, tuple) and hasattr(obj, "_fields"):  # named tuple
        return dict(zip(obj._fields, obj))
    elif dataclasses.is_dataclass(obj):
        return {
            field.name: getattr(obj, field.name) for field in dataclasses.fields(obj)
        }
    elif isinstance(obj, dict):
        return obj
    elif obj is None:
        return {}
    else:
        raise NotImplementedError(f"unsupported data type {type(obj)}")


def _object_to_tensordict(obj, device, batch_size) -> TensorDictBase:
    """Converts a namedtuple or a dataclass to a TensorDict."""
    t = {}
    _fields = _get_object_fields(obj)
    for name, value in _fields.items():
        if isinstance(value, (np.number, int, float)):
            t[name] = _ndarray_to_tensor(np.asarray([value])).to(device)
        elif isinstance(value, (jnp.ndarray, np.ndarray)):
            t[name] = _ndarray_to_tensor(value).to(device)
        else:
            nested = _object_to_tensordict(value, device, batch_size)
            if nested is not None:
                t[name] = nested
    if len(t):
        return make_tensordict(t, device=device, batch_size=batch_size)
    # discard empty tensordicts
    return None


def _tensordict_to_object(tensordict: TensorDictBase, object_example):
    """Converts a TensorDict to a namedtuple or a dataclass."""
    t = {}
    _fields = _get_object_fields(object_example)
    for name, example in _fields.items():
        value = tensordict.get(name, None)
        if isinstance(value, TensorDictBase):
            t[name] = _tensordict_to_object(value, example)
        elif value is None:
            if isinstance(example, dict):
                t[name] = _tensordict_to_object({}, example)
            else:
                t[name] = None
        else:
            if value.dtype is torch.bool:
                value = value.to(torch.uint8)
            value = jax_dlpack.from_dlpack(torch_dlpack.to_dlpack(value))
            t[name] = value.reshape(example.shape).view(example.dtype)
    return type(object_example)(**t)


def _extract_spec(data: Union[torch.Tensor, TensorDictBase], key=None) -> TensorSpec:
    if isinstance(data, torch.Tensor):
        shape = data.shape
        if key in ("reward", "done"):
            shape = (*shape, 1)
        if data.dtype in (torch.float, torch.double, torch.half):
            return UnboundedContinuousTensorSpec(
                shape=shape, dtype=data.dtype, device=data.device
            )
        else:
            return UnboundedDiscreteTensorSpec(
                shape=shape, dtype=data.dtype, device=data.device
            )
    elif isinstance(data, TensorDictBase):
        return CompositeSpec(
            {key: _extract_spec(value, key=key) for key, value in data.items()}
        )
    else:
        raise TypeError(f"Unsupported data type {type(data)}")
