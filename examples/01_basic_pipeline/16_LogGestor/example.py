from wpipe.sqlite import Wsqlite


with Wsqlite(db_name="demo.db") as db:

    args_dict = {
        "inference": {
            "source": "<image>",
        },
        "conf": 0.5,
    }

    db.input = args_dict

    db.details = {"info": "Starting the process..."}

    db.output = {"queso": "delicioso"}

print("complete")
