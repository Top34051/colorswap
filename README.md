# ColorSwap: A Color and Word Order Dataset for Multimodal Evaluation

ColorSwap is a dataset designed to assess and improve the proficiency of multimodal models in matching objects with their colors. The dataset is comprised of 2,000 unique image-caption pairs, grouped into 1,000 examples. Each example includes a caption-image pair, along with a "color-swapped" pair. Crucially, the two captions in an example have the same words, but the color words have been rearranged to modify different objects. The dataset was created through a novel blend of automated caption and image generation with humans in the loop. 

Paper: Coming soon!

## Usage

First, please download the dataset from https://drive.google.com/file/d/1xdG94DQdz_eQVH1lrEeaHVz_BNkrVgb5/view?usp=sharing and extract the files to the `data` folder. We include the captions and images in `data/{train, test}.json` and `data/images.zip` respectively. An example of the dataset is as follows:

```python
[
    {
        "id": 0,
        "caption_1": "someone holding a yellow umbrella wearing a white dress",
        "caption_2": "someone holding a white umbrella wearing a yellow dress",
        "image_1": "images/img_0_1.png",
        "image_2": "images/img_0_2.png",
        "image_source": "midjourney",
        "caption_source": "human"
    },
    ...
]
```

Alternatively, you can download the dataset directly from the Hugging Face API with the following code:

```python
from datasets import load_dataset

dataset = load_dataset("Top34051/colorswap", use_auth_token=True)
```

Please make sure to install the `datasets` library and use the `use_auth_token` parameter to authenticate with the Hugging Face API.

## Evaluations

### Image-Text Matching Models

To replicate our ITM models evaluations, please refer to this [Colab demo](https://colab.research.google.com/drive/1EWPsSklfq49WiX2nUyOTmKZftU0AC4YL?usp=sharing).

### Visual Language Models

The responses generated from VLM models are included in the `vlm_results` folder. To extract the scores for VLM models, you can run the following command:

```bash
python vlm_eval.py
```

## Citation

If you find our work useful, please cite the following paper:

```
@article{burapacheep2024colorswap,
    author    = {Jirayu Burapacheep and Ishan Gaur and Agam Bhatia and Tristan Thrush},
    title     = {ColorSwap: A Color and Word Order Dataset for Multimodal Evaluation},
    journal   = {arXiv},
    year      = {2024},
}
```
