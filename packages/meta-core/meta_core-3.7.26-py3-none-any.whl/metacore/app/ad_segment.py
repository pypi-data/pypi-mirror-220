import os
import json
import cv2
import torch

import numpy as np
from PIL import Image
import torch.nn.functional as F

from .. import open_clip
from ..utils import LinearLayer
from ..utils import encode_text_with_prompt_ensemble


def apply_ad_scoremap(image, scoremap, alpha=0.5):
    np_image = np.asarray(image, dtype=float)
    scoremap = (scoremap * 255).astype(np.uint8)
    scoremap = cv2.applyColorMap(scoremap, cv2.COLORMAP_JET)
    scoremap = cv2.cvtColor(scoremap, cv2.COLOR_BGR2RGB)
    return (alpha * np_image + (1 - alpha) * scoremap).astype(np.uint8)


def normalize(pred, max_value=None, min_value=None):
    if max_value is None or min_value is None:
        return (pred - pred.min()) / (pred.max() - pred.min())
    else:
        return (pred - min_value) / (max_value - min_value)


class ADSegment(object):
    def __init__(self,
                 model_path="models/epoch_147.pth",
                 config_path="models/ViT-L-14-336.json",
                 obj_list=["PFL"],
                 image_size=518,
                 features_list=[6, 12, 18, 24],
                 model_name="ViT-L-14-336"):
        self.obj_list = obj_list
        self.image_size = image_size
        self.features_list = features_list
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        # clip
        self.clip, _, self.transform = open_clip.create_model_and_transforms(model_name, image_size,
                                                                             pretrained="openai")
        self.clip.to(self.device)
        tokenizer = open_clip.get_tokenizer(model_name)
        # seg
        with open(config_path, 'r') as f:
            model_configs = json.load(f)
        self.model = LinearLayer(model_configs['vision_cfg']['width'],
                                 model_configs['embed_dim'],
                                 len(features_list),
                                 model_name).to(self.device)
        checkpoint = torch.load(model_path, map_location=None if torch.cuda.is_available() else 'cpu')
        self.model.load_state_dict(checkpoint["trainable_linearlayer"])
        # text prompt
        with torch.cuda.amp.autocast(), torch.no_grad():
            self.text_prompts = encode_text_with_prompt_ensemble(self.clip, obj_list, tokenizer, self.device)

    def predict(self, image, thre=0.5):
        h, w = image.shape[:2]
        image_tensor = self.transform(Image.fromarray(image))
        image_tensor = image_tensor.unsqueeze(0)
        image_tensor = image_tensor.cuda()

        with torch.no_grad(), torch.cuda.amp.autocast():
            image_features, patch_tokens = self.clip.encode_image(image_tensor, self.features_list)
            image_features /= image_features.norm(dim=-1, keepdim=True)
            text_features = []
            for cls in self.obj_list:
                text_features.append(self.text_prompts[cls])
            text_features = torch.stack(text_features, dim=0)
            patch_tokens = self.model(patch_tokens)
            anomaly_maps = []
            for layer in range(len(patch_tokens)):
                patch_tokens[layer] /= patch_tokens[layer].norm(dim=-1, keepdim=True)
                anomaly_map = (100.0 * patch_tokens[layer] @ text_features)
                B, L, C = anomaly_map.shape
                H = int(np.sqrt(L))
                anomaly_map = F.interpolate(anomaly_map.permute(0, 2, 1).view(B, 2, H, H),
                                            size=self.image_size, mode='bilinear', align_corners=True)
                anomaly_map = torch.softmax(anomaly_map, dim=1)[:, 1, :, :]
                anomaly_maps.append(anomaly_map.cpu().numpy())
            anomaly_map = np.sum(anomaly_maps, axis=0)

        mask = cv2.resize(normalize(anomaly_map[0]), (w, h))
        mask = mask > thre
        torch.cuda.empty_cache()
        return mask

    @staticmethod
    def get_rect(mask):
        mask = (mask * 255).astype(np.uint8)
        _, pred = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(pred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) < 1:
            return []

        area = [cv2.contourArea(c) for c in contours]
        max_idx = np.argmax(area)
        min_rect = cv2.minAreaRect(contours[max_idx])
        min_rect = cv2.boxPoints(min_rect)

        return min_rect, contours[max_idx]

    @staticmethod
    def show(image, mask):
        return apply_ad_scoremap(image, mask, alpha=0.5)
