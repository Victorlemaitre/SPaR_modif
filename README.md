# SPaR
## Self-Play with Tree-Search Refinement to Improve Instruction-Following in Large Language Models

<p align="center">
   🤗 <a href="#data" target="_blank">Data</a> • 📃 <a href="https://arxiv.org/abs/2412.11605" target="_blank">Paper</a>
</p>

SPaR focuses on creating interference-free preference pairs for effective self- improvement. An example of the interfering factors (*story content*) in independently sampled multiple responses (Left). Refined response pairs exclude these factors, highlight the key difference (*ending sentence*), and lead to improved performance on iteratively trained LLaMA3-8B-Instruct (Right).

<div align="center">
<img src="assets/abs.png" alt="BPO" width="100%" />
</div>

<br>

## Table of Contents
- [Data](#data)
- [Quick Start](#quick-start)
    - [Data Construction](#data-construction)
    - [Model Training](#model-training)
- [Citation](#citation)

## Data

### SPaR dataset
SPaR Dataset can be found on [Hugging Face](https://huggingface.co/datasets/CCCCCC/SPaR).

We provide a high-quality SFT dataset for instruction-following tasks and the data for iterative self-training.


## Quick Start
For all codes, we have added `#TODO` comments to indicate places in the code that need modification before running. Please update the relevant parts as noted before executing each file.

### Data Construction
To construct the iterative training data yourself, run the following command
```bash
cd src

bash infer.sh

python process_data.py

bash judge.py

python process_data.py

vllm serve <your-model-path>

python tree_search.py

python process_data.py
```

### Model Training
If you want to train your own model, 
please run the following command:
```bash
cd src

# dpo
llamafactory-cli train configs/dpo.yaml

# sft
llamafactory-cli train configs/sft.yaml

```


## Acknowledgement
- Training code: [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)
- Tree-search implementation: [Rest-MCTS*](https://github.com/THUDM/ReST-MCTS)

## Citation
```
@misc{cheng2024sparselfplaytreesearchrefinement,
      title={SPaR: Self-Play with Tree-Search Refinement to Improve Instruction-Following in Large Language Models}, 
      author={Jiale Cheng and Xiao Liu and Cunxiang Wang and Xiaotao Gu and Yida Lu and Dan Zhang and Yuxiao Dong and Jie Tang and Hongning Wang and Minlie Huang},
      year={2024},
      eprint={2412.11605},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2412.11605}, 
}
```