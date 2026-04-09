import os

import numpy as np
from shapely import Polygon
from ultralytics import YOLO
from ultralytics.engine.results import Results


class ImageInference:
    NAME = __name__
    VERSION = "1.2.1"

    MODEL: YOLO = None
    TEMPLATE = {
        "name": None,
        "bbox": None,
        "conf": None,
        "mask": None,
        "status": None,
        "class_id": None,
    }

    def __init__(self, model_path: str):
        assert os.path.exists(model_path), (
            f"The model file in {model_path} does not exist"
        )

        self.model_path = model_path

        if self.MODEL is None:
            _, self.MODEL = self.predict(self.model_path)

    def predict(
        self, model_path: str = None, model: YOLO = None, inference_params: dict = None
    ) -> tuple[Results, YOLO]:
        """
        Performs prediction using a YOLO model, loading the model from a file path if a model object is not provided.

        Parameters:
        -----------
            * **model_path** (*str*): path to the pre-trained YOLO model file.

            * **model** (*YOLO*): pre-trained YOLO model object.

            * **inference_params** (*dict*): inference parameters passed to the model for making predictions.

        Returns:
        --------
            * **tuple**: containing:
                * **results** (*list | None*): the inference results, or 'None' if no inference parameters are provided.

                * **model** (*YOLO*): the YOLO model object used for inference.
        """

        results = None

        if model is None:
            model = YOLO(model_path)

        if inference_params:
            results = model(**inference_params)

        return results, model

    def __call__(self, args_dict: dict) -> dict:
        """
        Executes the inference on the image-based model.

        Parameters:
        -----------
            **args_dict** (*dict*): contains the following keys:
                * **data** (*dict*): contains the following keys:
                    - **model_path** (*str*): path where the model is stored.
                * **inference** (*dict*): contains the inference parameters.

        Returns:
        --------
        Depending on the problem that is being solved, the results are:

        Classification:

            **model_results** (*dict*): contains the following keys:
                * **model_results** (*list[dict]*): each element contains the following keys:
                    - **class_id** (*int*): identifier of the predicted class.
                    - **name** (*str*): name of the predicted class.
                    - **conf** (*float*): confidence associated with the predicted class.
                    - **conf_percentage** (*float*): confidence associated with the predicted
                        class expressed between 0 and 100.

                    - **status** (*bool*): indicates whether the prediction is considered appropriate.

        Segmentation:

            **model_results** (*dict*): contains the following keys:
                * **model_results** (*list[dict]*): each element contains the following keys:
                    - **class_id** (*int*): identifier of the predicted class.
                    - **name** (*str*): name of the predicted class.
                    - **conf** (*float*): confidence associated with the predicted class.
                    - **conf_percentage** (*float*): confidence associated with the predicted
                        class expressed between 0 and 100.

                    - **bbox** (*list[int]*): vertices of the bounding box of the area.
                    - **mask** (*list[float]*): vertices of the area.
                    - **area** (*float*): area
                    - **status** (*bool*): indicates whether the prediction is valid.

        Detection:

            **model_results** (*dict*): contains the following keys:
                * **model_results** (*list[dict]*): each element contains the following keys:
                    - **class_id** (*int*): identifier of the predicted class.
                    - **name** (*str*): name of the predicted class.
                    - **conf** (*float*): confidence associated with the predicted class.
                    - **conf_percentage** (*float*): confidence associated with the predicted
                        class expressed between 0 and 100.

                    - **bbox** (*list[int]*): vertices of the bounding box of the area.
                    - **status** (*bool*): indicates whether the prediction is valid.
        """

        model_results, _ = self.predict(
            model=self.MODEL, inference_params=args_dict["inference"]
        )
        assert model_results, "No results were returned during inference"

        collection_results = []
        for result in model_results:
            template = ImageInference.TEMPLATE.copy()

            if result.probs:
                class_id = result.probs.top1
                conf = result.probs.top1conf.item()
                name = self.MODEL.names[int(class_id)]
                template.update(
                    {
                        "class_id": class_id,
                        "name": name,
                        "conf": round(conf, 2),
                        "conf_percentage": round(conf * 100, 2),
                        "status": bool(args_dict["inference"]["conf"] <= conf),
                    }
                )
                collection_results.append(template)

            elif result.masks:
                classes = result.boxes.cls
                confs = result.boxes.conf
                boxes = result.boxes.xyxy
                masks = result.masks.xy
                for class_id, conf, bbox, mask in zip(classes, confs, boxes, masks):
                    class_id = int(class_id.item())
                    name = self.MODEL.names[class_id]
                    polygon_coords = np.int32([mask]).tolist()[0]
                    this_polygon = Polygon(polygon_coords)
                    template.update(
                        {
                            "class_id": class_id,
                            "name": name,
                            "conf": round(conf.item(), 2),
                            "conf_percentage": round(conf.item() * 100, 2),
                            "bbox": [int(x) for x in bbox],
                            "mask": list(this_polygon.exterior.coords),
                            "area": this_polygon.area,
                            "status": bool(args_dict["inference"]["conf"] <= conf),
                        }
                    )
                    collection_results.append(template)
                    template = ImageInference.TEMPLATE.copy()

            elif result.boxes:
                classes = result.boxes.cls
                boxes = result.boxes.xyxy
                confs = result.boxes.conf
                for class_id, conf, bbox in zip(classes, confs, boxes):
                    class_id = int(class_id.item())
                    name = self.MODEL.names[class_id]
                    template.update(
                        {
                            "class_id": class_id,
                            "name": name,
                            "conf": round(conf.item(), 2),
                            "conf_percentage": round(conf.item() * 100, 2),
                            "bbox": [int(x) for x in bbox],
                            "status": bool(
                                args_dict["inference"]["conf"] <= conf.item()
                            ),
                        }
                    )
                    collection_results.append(template)
                    template = ImageInference.TEMPLATE.copy()

                break

            template = ImageInference.TEMPLATE.copy()
            if len(collection_results) > 0:
                break

        model_results = {"model_results": collection_results}
        return model_results
