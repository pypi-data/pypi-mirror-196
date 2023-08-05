from functools import partial
import jax
import optax
from ..train.loss import Loss
from ..ops import sorbel_edges
from .detection import _binary_focal_crossentropy

jnp = jax.numpy

def _compute_edge(instance_output, instance_yc, instance_xc, height, width):
    _, ps, _ = instance_yc.shape
    padding = ps // 2 + 1

    patch_edges = jnp.square(sorbel_edges(instance_output))
    patch_edges = (patch_edges[0] + patch_edges[1]) / 8.0
    patch_edges = jnp.sqrt(jnp.clip(patch_edges, 1e-8, 1.0)) # avoid GPU error
    # patch_edges = jnp.where(patch_edges > 0, jnp.sqrt(patch_edges), 0)
    combined_edges = jnp.zeros([height + padding*2, width + padding*2])
    combined_edges = combined_edges.at[instance_yc + padding, instance_xc + padding].add(patch_edges)
    combined_edges = combined_edges[padding:padding+height, padding:padding+width]
    combined_edges = jnp.tanh(combined_edges)

    return combined_edges

def self_supervised_edge_losses(pred, input):
    '''
    Args:
        auxnet_out: [H,W, n_groups]
        instance_edge: [H,W]
        category: category number [0, n_groups)
    return:
        loss: float
    '''
    instance_output = pred['instance_output']
    instance_yc = pred['instance_yc']
    instance_xc = pred['instance_xc']
    height, width, _ = input['image'].shape
    instance_edge = _compute_edge(
        instance_output, instance_yc, instance_xc, height, width
    )
    instance_edge_pred = jax.nn.sigmoid(pred['edge_pred'])

    return optax.l2_loss(instance_edge_pred, instance_edge).mean()

# def auxnet_losses(auxnet_out, instance_edge, category=None):
#     '''
#     Args:
#         auxnet_out: [H,W, n_groups]
#         instance_edge: [H,W]
#         category: category number [0, n_groups)
#     return:
#         loss: float
#     '''
#     edge_pred, instance_edge = _get_auxnet_prediction(auxnet_out, instance_edge, category)

#     return _binary_focal_crossentropy(edge_pred, instance_edge >= 0.5).mean()

# class AuxnetLoss(Loss):
#     def call(
#         self,
#         preds: dict,
#         group_num: jnp.ndarray = None,
#     ):
#         if not 'training_locations' in preds:
#             return 0.0

#         return jax.vmap(auxnet_losses)(
#             auxnet_out = preds['auxnet_out'],
#             instance_edge = preds['instance_edge'],
#             category = group_num.astype(int),
#         )

class InstanceEdgeLoss(Loss):
    def call(
        self,
        inputs: dict,
        preds: dict,
        **kwargs,
    ):
        if not 'training_locations' in preds:
            return 0.0

        return jax.vmap(self_supervised_edge_losses)(
            preds, inputs
        )
