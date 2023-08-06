import cv2
import os.path as osp
from typing import Optional, List

from weathon.dl.base.dataset import TorchCustomDataset
from weathon.dl.registry import CUSTOM_DATASETS
from weathon.dl.utils.config.config import ConfigDict
from weathon.dl.utils.constants import Tasks, Datasets


@CUSTOM_DATASETS.register_module(group_key=Tasks.ocr_detection, module_name=Datasets.icdar2015_ocr_detection)
class IcdarOcrDetectionDataset(TorchCustomDataset):

    def __init__(self, dataset_cfg: Optional[ConfigDict] = None, *args, **kwargs):
        dataset_cfg = dataset_cfg if dataset_cfg else dict()
        self.img_mode = kwargs.get("img_mode", dataset_cfg.get("img_mode", 'RGB'))

        self.data_dir = kwargs.get("data_dir", dataset_cfg.get("data_dir", None))
        self.label_file = kwargs.get("label_file", dataset_cfg.get("label_file", None))
        self.ignore_tags = kwargs.get("ignore_tags", dataset_cfg.get("ignore_tags", ['*', '###']))
        self.load_char_annotation = kwargs.get("load_char_annotation", dataset_cfg.get("load_char_annotation", False))

        self.preprocessor = kwargs.get("preprocessor", dataset_cfg.get("preprocessor", None))
        self.examples = self._get_examples()

    def _get_examples(self):
        examples = []
        with open(osp.join(self.data_dir, self.label_file), "r", encoding="utf8") as reader:
            for line in reader:
                image_file, line_labels = line.split("\t", maxsplit=1)

                img_path = osp.join(self.data_dir, image_file)
                img_name = image_file.split("/")[-1]
                im = cv2.imread(img_path, 1 if self.img_mode != 'GRAY' else 0)
                if self.img_mode == "RGB":
                    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                labels = self._parse_line_label(line_labels)
                polygons = []
                texts = []
                illegibility_list = []
                language_list = []
                for label in labels:
                    if len(label["polygon"]) == 0 or len(label["text"]) == 0:
                        continue
                    polygons.append(label["polygon"])
                    texts.append(label["text"])
                    illegibility_list.append(label["illegibility"])
                    language_list.append(label["language"])
                    if self.load_char_annotation:
                        for char_label in label["chars"]:
                            if len(char_label["polygon"]) == 0 or len(char_label["char"]) == 0:
                                continue
                            polygons.append(char_label["polygon"])
                            texts.append(char_label["char"])
                            illegibility_list.append(char_label["illegibility"])
                            language_list.append(char_label["language"])
                examples.append({
                    "img_path": img_path,
                    "img_name": img_name,
                    "text_polys": polygons,
                    "texts": texts,
                    "ignore_tags": illegibility_list,
                    "img": im,
                    "shape": [im.shape[0], im.shape[1]]
                })
        return examples

    def _parse_line_label(self, line_labels: str) -> List:
        labels = []
        annotations = eval(line_labels)
        for annotation in annotations:
            labels.append({
                "polygon": annotation["points"],
                "text": annotation["transcription"],
                "illegibility": annotation["transcription"] in self.ignore_tags,
                "language": "Latin",
                "chars": [
                    {
                        "polygon": [],
                        "char": "",
                        "illegibility": False,
                        "language": "Latin"
                    }
                ]
            })

        return labels

    def __getitem__(self, index):
        return self.preprocessor(self.examples[index]) if self.preprocessor else self.examples[index]

    def __len__(self):
        return len(self.examples)
