# LaViDa-Pathgen 
World's First Diffusion Model based Visual Language Model for Pathology 
Only used LLaDA as the Large Language Diffusion Model (LaViDa has both with LLaDA and DREAM) 

# Dataset:
Download [GDC client](https://gdc.cancer.gov/access-data/gdc-data-transfer-tool). Download the required WSI using [download_wsi_using_gdc_client.sh](https://github.com/Himanshunitrr/LaViDa-PathGen/blob/main/download_wsi_using_gdc_client.sh). Download the [PathGen-1.6M.json](https://huggingface.co/datasets/jamessyx/PathGen/tree/main) which has wsi id, position and captions, once you have the WSIs, use [create_img_txt_pairs_for_pathgen.py](https://github.com/Himanshunitrr/LaViDa-PathGen/blob/main/create_img_txt_pairs_for_pathgen.py) to create image-text pairs.  
Download the VQA dataset from [jamessyx/PathGen-Instruct](https://huggingface.co/datasets/jamessyx/PathGen-Instruct).

Already curated dataset for [Stage 1 and Stage 2](https://huggingface.co/datasets/himanshunitrr/LaViDa-PathGen-Instruct-and-VQA/tree/main) training

# Transformers compatible weights (HF)

# Inference
Download checkpoint from https://huggingface.co/himanshunitrr/LaViDa-Pathgen
You can infer using predict.py


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
```
Pretrain(Stage 1) Scripts:
scripts/train/exps/cluster/pretrain_llada.sh
scripts/train/exps/cluster/pretrain_dream.sh

Finetune(Stage 2) Scripts

scripts/train/exps/cluster/llada-hd-llada-s2.sh
scripts/train/exps/cluster/llada-hd-dream-s2.sh

```
# Evaluation
PathMMU


![image](https://github.com/user-attachments/assets/1f16869f-d240-4f0c-876f-defe22d3ccd9)
![image](https://github.com/user-attachments/assets/af9ab674-4ac9-4c79-ab94-7db9312fd4f4)


# Thanks
A huge shoutout to @jacklishufan for LaViDa and answering all my stupid questions. 





