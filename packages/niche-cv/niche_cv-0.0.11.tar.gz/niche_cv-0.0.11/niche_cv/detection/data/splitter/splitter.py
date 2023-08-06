from abc import ABC, abstractmethod


class Splitter(ABC):
    def __init__(
        self,
        root: str,
        ratio_train: float = 0.64,
        ratio_val: float = 0.16,
        ratio_test: float = 0.2,
    ):
        self.root = root
        self.config = None
        # ids
        self.ids = None
        self.id_train = None
        self.id_val = None
        self.id_test = None
        # split ratios
        self.ratio_train = ratio_train
        self.ratio_val = ratio_val
        self.ratio_test = ratio_test

    @abstractmethod
    def _set_dataset(self):
        """
        read or open the config file:
            COCO: JSON
            YOLO: YAML
        results:
            self.config
            self.ids
        """

    @abstractmethod
    def _get_ids(self) -> list:
        """
        get ids from the config file
        """

    def _set_ids(self) -> None:
        """
        set sample ids from the dataset to self.ids
        """
        self.ids = self._get_ids()

    @abstractmethod
    def shuffle_train_test(self) -> None:
        """
        shuffle ids into lists of train, val, test
        sets self.id_train, self.id_val, self.id_test
        """

    @abstractmethod
    def write_dataset(self) -> None:
        """
        write the images and configuration file based on the ids
        """
