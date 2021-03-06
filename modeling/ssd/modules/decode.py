"""Decode
Original author: YutaroOgawa
https://github.com/YutaroOgawa/pytorch_advanced/blob/master/2_objectdetection/utils/ssd_model.py
"""
import torch

def decode(loc, dbox_list, variances):
    """Decode predictions : DBox -> BBox

    Parameters
    ----------
    loc : torch.Tensor with size (8732, 4)
        location predictions for loc layer
    dbox_list : torch.Tensor with size (8732, 4)
        DBox location
    variances : list
        list of variance

    Returns
    -------
    boxes : [xmin, ymin, xmax, ymax]
        BBox info converted from [xcenter, ycenter, width, height]
    """

    #TODO: cx = cx_d + cx_d * 0.1 * Δcxなので、計算違うのでは？

    boxes = torch.cat((
        dbox_list[:, :2] + loc[:, :2] * variances[0] * dbox_list[:, 2:], 
        dbox_list[:, 2:] * torch.exp(loc[:, 2:] * variances[1])), dim=1)

    #TODO 以下が正しい?
    # boxes = torch.cat((
    #     dbox_list[:, :2] + loc[:, :2] * 0.1 * dbox_list[:, :2], 
    #     dbox_list[:, 2:] * torch.exp(loc[:, 2:] * 0.2)), dim=1)

    boxes[:, :2] -= boxes[:, 2:] / 2 # (xcenter, ycenter, width, height) -> (xmin, ymin, width, height)
    boxes[:, :2] = torch.clamp(boxes[:, :2], min=0.0) # minimum xmin and ymin should be 0.0
    boxes[:, 2:] += boxes[:, :2]     # (xmin, ymin, width, height) -> (xmin, ymin, xmax, ymax)

    return boxes