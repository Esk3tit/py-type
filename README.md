# py-type
This is a touch typing app I made to practice touch typing since I decided to relearn how to type properly. All of the websites for touch typing online are good for learning and general practice, but I wanted to practice specific keys over and over instead of all keys or some predefined subset of keys, so I made this app to address the problem.

This app was made using the `curses` module, which is a built-in library on Mac and Linux.

**Windows users will need to install `windows-curses` since there is no `curses` support out of the box (as far as I know).**

## Usage

Docker is the preferred way to run the app, since the Docker image ensures a consistent experience for all users regardless of their environment.

Otherwise users will need to install `windows-curses` if they are on Windows. Users should also make sure their Python 3 version is compatible just in case.

### Docker Instructions
1. **OPTIONAL** Clone this repo somewhere
2. **OPTIONAL** build the image with `docker build .` (if building/running command in same directory as the Dockerfile)
3. Run `docker compose run app` to pull the latest image and run it with Docker.
4. In the docker bash shell session, run `python py-type.py` (I haven't found a way to start the bash shell and then run this command in one go yet, so this is the workaround for now).

### Windows/Mac/Linux
1. Clone this repo somewhere
2. **OPTIONAL** Install `windows-curses` if on Windows.
3. Open a terminal and then execute the script with `python py-type.py` (or whatever `python` command you have, but the script requires a terminal session to work)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.