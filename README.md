### Leveraging Capsule Routing to Associate Knowledge with Medical Literature Hierarchically

#### Description
This repository includes the source code for the paper "Leveraging Capsule Routing to Associate Knowledge with Medical Literature Hierarchically"(https://aclanthology.org/2021.emnlp-main.285/). 
Basically, the program takes the medical literature, the RCor text fragment, the KImp text fragment, and the knowledge as input, and predict a label to indicate the relevance degree between the medical literature and the knowledge. 
More details about the underneath model can be found in the submitted paper.

#### Requirements
Libraries: ubuntu = 16.04, cuda = 10.2, cudnn = 8, GPU card = NVIDIA Tesla V100 * 1<br>
Dependencies: python > 3.5, tensorflow > 1.10.0, pdb, numpy, tdqm, codecs<br>
#### Code Structure:
>HiCapsRKL<br>
├── SampleData<br>
│   ├── train.tsv<br>
│   ├── relevance_prediction_test_data<br>
│   │  ├── test.tsv<br>
│   ├── medical_literature_retrieval_test_data<br>
│   │  ├── test.tsv<br>
├── InitModel<br>
│   ├── modellink.txt<br>
├── __init__.py<br>
├── match_utils.py<br>
├── modeling.py<br>
├── optimization.py<br>
├── tokenization.py<br>
├── train_HiCapsRKL.py<br>
├── f1.py<br>
├── ranking_metrics.py<br>
└── README.md<br>

* "train_HiCapsRKL.py" is the main file for training or test.
* "modeling.py" is the file of the model structure.
* "match_utils.py" is the file containing the capsule network function
* "optimization.py" is the file for optimiztion.
* "tokenization.py" is the file to tokenize the sentences.
* "f1.py" is the file to calculate the macro-f1 and micro-f1 score on the prediction of matching test set.
* "ranking_metrics.py" is the file to calculate the P@K, NDCG@K, MRR, MAP scores on the prediction of ranking test set.

#### SampleData Description
The training data (train.tsv), the relevance prediction test data (relevance_prediction_test_data/test.tsv), and the medical literature retrieval test data (medical_literature_retrieval_test_data/test.tsv) are randomly sampled from each whole set 
and these data could be used to run the training and testing process for this code.
* data format: <label + [TAB] + MedL + [TAB] + K_str + [TAB] + K_idx + [TAB] + RCor_score + [TAB] + RCor_text_fragment + [TAB] + KImp_score + [TAB] + KImp_text_fragment + [TAB] + keywords + [TAB] + MedL_id + [TAB] + bk_location>

#### InitModel Description
The directory contains the `BERT-Base, Chinese` pre-trained model as the initial checkpoint for training HiCapsRKL. If needed, one can download these paramters from https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip .

#### Train Model : 
```shell
python train_HiCapsRKL.py --task_name=medrkg --do_train=true --data_dir=SampleData \
--vocab_file=InitModel/vocab.txt --bert_config_file=InitModel/bert_config.json \
--init_checkpoint=InitModel/bert_model.ckpt --max_seq_length=256 --train_batch_size=8 \
--learning_rate=2e-5 --num_train_epochs=10.0 --output_dir=output_dir/
```
#### Predict on relevance prediction test set & F1 measurement: 
```shell
* python train_HiCapsRKL.py --task_name=medrkg --do_predict=true \
--data_dir=SampleData/relevance_prediction_test_data --vocab_file=InitModel/vocab.txt \
--bert_config_file=InitModel/bert_config.json --init_checkpoint=output_dir/\*\*\*.ckpt \
--output_dir=output_dir/
* python f1.py output_dir
```

#### Predict on matching test set & P@K, NDCG@K, MRR, MAP measurements: 
```shell
* python train_HiCapsRKL.py --task_name=medrkg --do_predict=true \
--data_dir=SampleData/medical_literature_retrieval_test_data \
--vocab_file=InitModel/vocab.txt --bert_config_file=InitModel/bert_config.json \
--init_checkpoint=output_dir/\*\*\*.ckpt --output_dir=output_dir/
* python ranking_metrics.py output_dir
```

#### Reference
If you use any of the resources listed here, please cite:<br>
```
@inproceedings{liu-etal-2021-leveraging,
    title = "Leveraging Capsule Routing to Associate Knowledge with Medical Literature Hierarchically",
    author = "Liu, Xin  and
      Chen, Qingcai  and
      Chen, Junying  and
      Zhou, Wenxiu  and
      Liu, Tingyu  and
      Yang, Xinlan  and
      Peng, Weihua",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2021",
    address = "Online and Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.emnlp-main.285",
    pages = "3518--3532",
    abstract = "Integrating knowledge into text is a promising way to enrich text representation, especially in the medical field. However, undifferentiated knowledge not only confuses the text representation but also imports unexpected noises. In this paper, to alleviate this problem, we propose leveraging capsule routing to associate knowledge with medical literature hierarchically (called HiCapsRKL). Firstly, HiCapsRKL extracts two empirically designed text fragments from medical literature and encodes them into fragment representations respectively. Secondly, the capsule routing algorithm is applied to two fragment representations. Through the capsule computing and dynamic routing, each representation is processed into a new representation (denoted as caps-representation), and we integrate the caps-representations as information gain to associate knowledge with medical literature hierarchically. Finally, HiCapsRKL are validated on relevance prediction and medical literature retrieval test sets. The experimental results and analyses show that HiCapsRKLcan more accurately associate knowledge with medical literature than mainstream methods. In summary, HiCapsRKL can efficiently help selecting the most relevant knowledge to the medical literature, which may be an alternative attempt to improve knowledge-based text representation. Source code is released on GitHub.",
}
```

