

LLADA_VISION_ENCODER="google/siglip-so400m-patch14-384"

set -x
# TASKS=
export TASKS=${TASKS:-"coco2017_cap_val_lite"}
export CUDA_VISIBLE_DEVICES=4
export DEBUG_PRINT_IMAGE_RES=1
export NOT_ALWASY_DO_2DPOOL=1 # llava do not have avg pooling
echo $TASKS

accelerate launch --num_processes=1 \
    -m lmms_eval \
    --model llava \
    --model_args pretrained=$1,model_name=llava,conv_template=llava_llama_3  \
    --tasks $TASKS \
    --batch_size 1 \
    --gen_kwargs prefix_lm=True \
    --log_samples \
    --log_samples_suffix llava_llada \
    --output_path ./logs/ --verbosity=DEBUG \
    ${@:2} \
