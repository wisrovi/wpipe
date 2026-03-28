from wpipe import start_dashboard

db_path = "full_example.db"



def main():
    

    start_dashboard(
        db_path=db_path,
        host="127.0.0.1",
        port=8034,
        open_browser=True,
    )

if __name__ == "__main__":
    main()