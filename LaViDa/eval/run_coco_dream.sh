LLADA_VISION_ENCODER="google/siglip-so400m-patch14-384"
set -x
export TASKS=${TASKS:-"mme"}
export CUDA_VISIBLE_DEVICES=1,2,3,4,5,6,7,8
export DEBUG_PRINT_IMAGE_RES=1
# max_new_tokens
accelerate launch --num_processes=8 --main_process_port=25511\
    -m lmms_eval \
    --model llava_dream \
    --model_args pretrained=$1,conv_template=dream,model_name=llava_dream \
    --tasks $TASKS \
    --batch_size 1 \
    --gen_kwargs alg=topk_margin,prefix_lm=True,step_ratio=0.5,schedule=shift,schedule__shift=0.33 \
    --log_samples \
    --log_samples_suffix llava_llada \
    --output_path ./logs/ --verbosity=DEBUG \
    ${@:2} \
