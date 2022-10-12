import json
import os
import sys
import time
from collections import Counter
from datetime import date
from subprocess import Popen


NUM_RUNS=12
GPU_IDS=list(range(4))
NUM_GPUS=len(GPU_IDS)
counter=0


DATASETS = [
    'domainnet',
    'camelyon',
    # # 'iwildcam',
    'fmow',
    'cifar10',
    'cifar100',
    'entity13', 
    'entity30',
    'living17',
    'nonliving26',
    # 'office31',
    'officehome',
    'visda'
]
TARGET_SETS = {
    'cifar10': ['0','1', '10', '23','57', '71', '95'],
    'cifar100': ['0', '4', '12', '43', '59', '82'], 
    'fmow': ['0','1','2'], 
    'iwildcams': ['0','1','2'], 
    'camelyon': ['0','1','2'], 
    'domainnet': ['0','1','2','3'], 
    'entity13': ['0','1','2', '3'],
    'entity30': ['0','1','2', '3'],
    'living17': ['0','1','2', '3'],
    'nonliving26': ['0','1','2', '3'],
    'officehome': ['0','1','2', '3'], 
    'office31': ['0','1','2'], 
    'visda': ['0','1','2'], 
}

SEEDS = ['42']
ALPHA = ['0.5', '1.0',  '3.0', '10.0', '100.0']
ALGORITHMS= ["ERM", "ERM-aug"]

SOURCE_FILE = {
    "cifar10": "logs/cifar10_seed\:42/%s-imagenet_pretrained\:imagenet/", 
    "cifar100": "logs/cifar100_seed\:42/%s-imagenet_pretrained\:imagenet/", 
    "camelyon": "logs/camelyon_seed\:42/%s-rand_pretrained\:rand/", 
    "entity13": "logs/entity13_seed\:42/%s-rand_pretrained\:rand/", 
    "entity30": "logs/entity30_seed\:42/%s-rand_pretrained\:rand/", 
    "living17": "logs/living17_seed\:42/%s-rand_pretrained\:rand/", 
    "nonliving26": "logs/nonliving26_seed\:42/%s-rand_pretrained\:rand/", 
    "fmow": "logs/fmow_seed\:42/%s-imagenet_pretrained\:imagenet/", 
    "domainnet": "logs/domainnet_seed\:42/%s-imagenet_pretrained\:imagenet/", 
    "officehome": "logs/officehome_seed\:42/%s-imagenet_pretrained\:imagenet/", 
    "visda": "logs/visda_seed\:42/%s-imagenet_pretrained\:imagenet/"
}

procs = []

for dataset in DATASETS:
    for seed in SEEDS: 
        for alpha in ALPHA: 
            for target_set in TARGET_SETS[dataset]: 
                for algorithm in ALGORITHMS: 
                    
                    gpu_id = GPU_IDS[counter % NUM_GPUS]

                    source_models = SOURCE_FILE[dataset] % algorithm

                    cmd=f"CUDA_VISIBLE_DEVICES={gpu_id} python run_expt.py --remote False \
                    --dataset {dataset} --root_dir /home/ubuntu/data --seed {seed} \
                    --transform image_none --algorithm  {algorithm} --eval_only --use_source_model \
                    --source_model_path={source_models} --dirichlet_alpha {alpha} \
                    --target_split {target_set} --use_target True  --simulate_label_shift True"
                    
                    print(cmd)                    
                    procs.append(Popen(cmd, shell=True))
                    
                    time.sleep(3)

                    counter += 1

                    if counter % NUM_RUNS == 0:
                        for p in procs:
                            p.wait()
                        procs = []
                        time.sleep(3)

                        print("\n \n \n \n --------------------------- \n \n \n \n")
                        print(f"{date.today()} - {counter} runs completed")
                        sys.stdout.flush()
                        print("\n \n \n \n --------------------------- \n \n \n \n")


# ALGORITHMS= ["ERM"]

# SOURCE_FILE = {
#     "camelyon": "logs/camelyon_seed\:42/ERM-clip_pretrained\:clip/lr\:1e-05_wd\:0.1_bs\:96_opt\:AdamW/", 
#     "fmow": "logs/fmow_seed\:42/ERM-clip_pretrained\:clip/lr\:1e-05_wd\:0.1_bs\:64_opt\:AdamW/", 
#     "domainnet": "logs/domainnet_seed\:42/ERM-clip_pretrained\:clip/lr\:1e-05_wd\:0.1_bs\:96_opt\:AdamW/", 
#     "officehome": "logs/officehome_seed\:42/ERM-clip_pretrained\:clip/lr\:1e-05_wd\:0.1_bs\:96_opt\:AdamW/", 
#     "visda": "logs/visda_seed\:42/ERM-clip_pretrained\:clip/lr\:1e-05_wd\:0.1_bs\:96_opt\:AdamW/"
# }

# for dataset in DATASETS:
#     for seed in SEEDS: 
#         for alpha in ALPHA:
#             for target_set in TARGET_SETS[dataset]: 
#                 for algorithm in ALGORITHMS: 
                    
#                     gpu_id = GPU_IDS[counter % NUM_GPUS]

#                     cmd=f"CUDA_VISIBLE_DEVICES={gpu_id} python run_expt.py --remote False \
#                     --dataset {dataset} --root_dir ../data --seed {seed} \
#                     --transform image_none --algorithm  {algorithm} --eval_only --use_source_model \
#                     --source_model_path={SOURCE_FILE[dataset]} --dirichlet_alpha {alpha} \
#                     --target_split {target_set} --use_target True  --simulate_label_shift True \
#                     --model clipvitb16 --n_epochs 10 --lr 0.00001 --weight_decay 0.1"
                    
#                     print(cmd)                    
#                     procs.append(Popen(cmd, shell=True))
                    
#                     time.sleep(10)

#                     counter += 1

#                     if counter % NUM_RUNS == 0:
#                         for p in procs:
#                             p.wait()
#                         procs = []
#                         time.sleep(10)

#                         print("\n \n \n \n --------------------------- \n \n \n \n")
#                         print(f"{date.today()} - {counter} runs completed")
#                         sys.stdout.flush()
#                         print("\n \n \n \n --------------------------- \n \n \n \n")

for p in procs:
    p.wait()
procs = []