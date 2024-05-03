# Text Classification demo on Japanese News by Using Bert


## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python run.py \              
    --model_name_or_path=cl-tohoku/bert-base-japanese-whole-word-masking \
    --do_train \
    --do_eval \
    --max_seq_length=128 \
    --per_device_train_batch_size=32 \
    --use_fast_tokenizer=False \
    --learning_rate=2e-5 \
    --num_train_epochs=10 \
    --output_dir=output/ \
    --overwrite_output_dir \
    --train_file=train.csv \
    --validation_file=dev.csv \
    --report_to="wandb" \
    --logging_steps=100 \
    --evaluation_strategy="epoch"
```
