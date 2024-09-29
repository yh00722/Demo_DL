from transformers import BertJapaneseTokenizer, ElectraForPreTraining

tokenizer = BertJapaneseTokenizer.from_pretrained('Cinnamon/electra-small-japanese-discriminator', mecab_kwargs={"mecab_option": "-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd"})

model = ElectraForPreTraining.from_pretrained('Cinnamon/electra-small-japanese-discriminator')
