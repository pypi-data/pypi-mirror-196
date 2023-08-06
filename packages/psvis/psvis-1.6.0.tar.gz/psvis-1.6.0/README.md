
## Introduction

This is pretrained models for person search. (resnet50,resnet18,shufflenetv1)

## License

This project is released under the [Apache 2.0 license](LICENSE).


## Installation

This project is developed upon [MMdetection](https://github.com/open-mmlab/mmdetection), please refer to [install.md](docs/install.md) to install MMdetection.

We utilized mmcv=1.3.9, pytorch=1.7.0

   ```bash
   pip install psvis
   ```

## Usage

   1. resnet50
   ```bash
   from psvis.models.backbones import resnet
   resnet50 = resnet.__dict__['resnet50'](pretrained=True)
   ```
   2. resnet18
   ```bash
   from psvis.models.backbones import resnet
   resnet18 = resnet.__dict__['resnet18'](pretrained=True)
   ```   
   3. shufflenetv1
   ```bash
   from psvis.models.backbones import shufflenet_v1
   shufflenetv1 = shufflenet_v1.__dict__['shufflenetv1'](pretrained=True)

   ```

[comment]: <> (## Citation)

[comment]: <> (If you use this toolbox or benchmark in your research, please cite this project.)

[comment]: <> (```)

[comment]: <> (@inproceedings{yan2021alignps,)

[comment]: <> (  title={Anchor-Free Person Search},)

[comment]: <> (  author={Yichao Yan, Jinpeng Li, Jie Qin, Song Bai, Shengcai Liao, Li Liu, Fan Zhu, Ling Shao},)

[comment]: <> (  booktitle={CVPR},)

[comment]: <> (  year={2021})

[comment]: <> (})

[comment]: <> (```)

