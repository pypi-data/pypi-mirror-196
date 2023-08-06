
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

   ```bash
   from psvis.models import resnet
   resnet50 = resnet.__dict__['resnet50'](pretrained=True)
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

