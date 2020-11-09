from app import app

if __name__ == '__main__':
    try:
        app.create_all_mentions()
    except KeyboardInterrupt:
        print("Canceled by user. Bye.")
    except BaseException as exc:
        print(exc)