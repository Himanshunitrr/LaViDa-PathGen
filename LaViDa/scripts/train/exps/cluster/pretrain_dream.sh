LLM_VERSION=/path/to/Dream-v0-Instruct-7B
VISION_MODEL_VERSION="/path/to/google/siglip-so400m-patch14-384"



LLM_VERSION_CLEAN="${LLM_VERSION//\//_}"
VISION_MODEL_VERSION_CLEAN="${VISION_MODEL_VERSION//\//_}"


PROMPT_VERSION=plain

BASE_RUN_NAME="pretrain-dream"
echo "BASE_RUN_NAME: ${BASE_RUN_NAME}"
NUM_GPUS=8
export NOT_ALWASY_DO_2DPOOL=1
IMG_PATH=data/pretrain/images
DATA_PATH=data/pretrain/blip_laion_cc_sbu_558k.json 
torchrun --nproc_per_node="${NUM_GPUS}" --master_port=22233 \
    llava/train/train_mem.py \
    --deepspeed scripts/zero3.json \
    --model_name_or_path ${LLM_VERSION} \
    --version ${PROMPT_VERSION} \
    --data_path $DATA_PATH \
    --image_folder $IMG_PATH\
    --vision_tower ${VISION_MODEL_VERSION} \
    --mm_tunable_parts="mm_mlp_adapter" \
    --mm_vision_select_layer -2 \
    --mm_projector_type mlp2x_gelu \
    --mm_use_im_start_end False \
    --mm_use_im_patch_token False \
    --bf16 True \
    --output_dir output/lavida/v1/projectors/${BASE_RUN_NAME} \
    --num_train_epochs 1 \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --evaluation_strategy "no" \
    --save_strategy "no" \
    --save_steps 50000 \
    --learning_rate 1e-3 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --tf32 True \
    --model_max_length 8192 \
    --gradient_checkpointing True \
    --dataloader_num_workers 4 \
    --lazy_preprocess True \
    --report_to wandb \
    --run_name $BASE_RUN_NAME \
    --resume_from_checkpoint latest \
    --attn_implementation sdpa ${@}

