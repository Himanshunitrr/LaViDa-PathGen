# LaViDa-Pathgen 
World's First Diffusion Model based Visual Language Model for Pathology based on LaViDa, trained on PathGen-1.6M dataset and finetuned on PathGen-Instruct datasets.

![LaViDa-PathGen Animation](image_text_animation.gif)

# Dataset:
Download [GDC client](https://gdc.cancer.gov/access-data/gdc-data-transfer-tool). Download the required WSI using [download_wsi_using_gdc_client.sh](https://github.com/Himanshunitrr/LaViDa-PathGen/blob/main/curate_dataset_from_scratch/download_wsi_using_gdc_client.sh).
 Download the [PathGen-1.6M.json](https://huggingface.co/datasets/jamessyx/PathGen/tree/main) which has wsi id, position and captions, once you have the WSIs, use [create_img_txt_pairs_for_pathgen.py](https://github.com/Himanshunitrr/LaViDa-PathGen/blob/main/curate_dataset_from_scratch/create_img_txt_pairs_for_pathgen.py) to create image-text pairs.  
Download the VQA dataset from [jamessyx/PathGen-Instruct](https://huggingface.co/datasets/jamessyx/PathGen-Instruct).

You can directly download the dataset for Stage 1 and Stage 2 from [here](https://huggingface.co/datasets/himanshunitrr/LaViDa-PathGen-Instruct-and-VQA/tree/main) in the format required for training.

# Transformers compatible weights (HF)

# Inference
Download checkpoint from https://huggingface.co/himanshunitrr/LaViDa-Pathgen
You can infer using [predict.py](https://github.com/Himanshunitrr/LaViDa-PathGen/blob/main/LaViDa/predict.py)


# LaViDa Setup:
```
git clone https://github.com/Himanshunitrr/LaViDa-PathGen.git
cd LaViDa
conda create --name lavida python=3.13
conda activate lavida
pip install -e .[train]
cd eval
pip install -e .
cd ../
pip install trl==0.17.0 
```

# Training
### Stage 1 Pretraining
IMG_PATH is the path to the images
DATA_PATH is the path to the stage-1 dataset (json file)

You can view the wandb.ai log for this stage at [this link](https://wandb.ai/himanshu_nitrr/huggingface/reports/Stage-1-training--VmlldzoxMzM4OTg4Nw?accessToken=jztmj7d8pxo5k00yr081pmon77iflc55cu9o4kscb7h32t7uubx9yenh7o8kjhg4)

```

LaViDa-PathGen/LaViDa/scripts/train/exps/cluster/pretrain_llada.sh
```

### Stage 2 Finetuning
For Stage 2 finetuning, you will need mm_projector.bin which you will get from Stage 1 training. If you just want to do Stage 2 finetuning, you can download the mm_projector.bin from [here](https://huggingface.co/jacklishufan/lavida-llada-1.0-stage1/blob/main/mm_projector.bin). 

IMG_PATH is the path to the images
DATA_PATH is the path to the stage-2 dataset (json file)

You can view the wandb.ai log for this stage at [this link](https://api.wandb.ai/links/himanshu_nitrr/28w44nmw)

```
LaViDa-PathGen/LaViDa/scripts/train/exps/cluster/llada-hd-llada-s2.sh

```
# Evaluation
PathMMU

To evaluate the model on PathMMU use [main.py](https://github.com/Himanshunitrr/LaViDa-PathGen/blob/main/PathMMU-main/eval/main.py)

Use the conda environment you created earlier for LLaVA for evaluating LLaVA based models and use the conda environment you created for LaViDa for evaluating LaViDa based models.

Also, for some reason for LLaVA based models, you need to use an old version of LLaVA, for more information, check [this issue](https://github.com/PathMMU-Benchmark/PathMMU/issues/7)

![image](https://github.com/user-attachments/assets/ea7c4e08-4738-4590-96a1-d752714d9993)

![image](https://github.com/user-attachments/assets/a5ea8760-66cf-4c37-81d4-a5a79f338684)

* in the PathGen-LLaVA paper the reported accuracy is quite low (~60.1) but I got different results. 

# Thanks
A huge shoutout to @jacklishufan et al for [LaViDa](https://github.com/jacklishufan/LaViDa/tree/main) and answering all my stupid questions, @superjamessyx et al for [PathGen](https://github.com/PathFoundation/PathGen-1.6M) and [PathMMU](https://github.com/PathMMU-Benchmark/PathMMU) and my Boss Anant for all the support and guidance.





