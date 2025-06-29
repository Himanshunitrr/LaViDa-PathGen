

LLADA_VISION_ENCODER="google/siglip-so400m-patch14-384"

set -x
# TASKS=
export TASKS="coco2017_cap_val_lite"
export CUDA_VISIBLE_DEVICES=2,3,4,5,6,7,8,9
export DEBUG_PRINT_IMAGE_RES=1
export NOT_ALWASY_DO_2DPOOL=1 # lowres
echo $TASKS

accelerate launch --num_processes=8 \
    -m lmms_eval \
    --model llava_llada \
    --model_args pretrained=$1,conv_template=llada,model_name=llava_llada \
    --tasks $TASKS \
    --batch_size 1 \
    --gen_kwargs prefix_lm=True,step_ratio=0.5,schedule=shift,schedule__shift=0.33 \
    --log_samples \
    --log_samples_suffix llava_llada \
    --output_path ./logs/ --verbosity=DEBUG \
    ${@:2} \
