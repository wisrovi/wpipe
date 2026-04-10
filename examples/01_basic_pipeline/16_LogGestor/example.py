from wpipe.sqlite import Wsqlite


with Wsqlite(db_name="demo.db") as db:

    args_dict = {
        "inference": {
            "source": "<image>",
        },
        "conf": 0.5,
    }

    db.input = args_dict

    try:
        results = {"queso": "delicioso"}

        db.output = results

        print(results)
    except Exception as error:

        db.details = {"error": f"Exception-Error: {str(error)}"}

        raise
