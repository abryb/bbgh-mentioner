from app import App

if __name__ == '__main__':
    app = App()
    try:
        print("Creating all mentions")
        app.create_all_mentions()
        app.save_state()
        print("Done")
    except KeyboardInterrupt:
        print("Canceled by user. Saving state...")
        app.save_state()
        print("Bye.")
