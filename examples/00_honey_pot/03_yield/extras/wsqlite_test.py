from wpipe.sqlite import Wsqlite
import cv2




def test_Wsqlite():
    image = cv2.imread("images.jpeg")

    with Wsqlite(db_name="output/demo.db") as db:

        args_dict = {
            "inference": {
                "source": image,
            },
            "conf": 0.5,
        }

        db.input = args_dict

        db.details = {"info": "Starting the process..."}

        db.output = {"queso": "delicioso"}
        
        
