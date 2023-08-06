from keras.metrics import CategoricalAccuracy
from ml.loss.cross_entropy import categorical_focal_loss
from ml.model.categorical_model import CategoricalModel


class ImbalancedCategoricalModel(CategoricalModel):
    def __init__(self, class_names, name, input_size, class_ids, dropout_rate=0.1) -> None:
        super().__init__(class_names, name, input_size, class_ids, dropout_rate)

    def instance_loss_accuracy(self):
        return categorical_focal_loss, CategoricalAccuracy()
