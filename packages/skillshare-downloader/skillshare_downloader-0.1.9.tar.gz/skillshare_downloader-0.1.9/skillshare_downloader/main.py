import argparse
from skillshare_downloader.skillshare import Downloader
import os
import json

current_directory = os.getcwd()
configuration = os.path.join(current_directory, 'config.json')

def save_conf(registry):
        with open(configuration, 'w') as f:
            json.dump(registry, f, indent=4)

def load_conf():
    if os.path.exists(configuration):
        with open(configuration, 'r') as f:
            try:
                registry = json.load(f)
                return registry
            except json.JSONDecodeError:
                pass
    return {'cookie': None, 'api_id': None, 'api_hash': None, 'phone': None}

conf = load_conf()

def configure():
    global cookie, api_id, api_hash, phone

    print("\033[1;35mConfiguration ===================\033[0m")
    print("Put your cookies on a file .txt and drag and drop that fle into this window and press ENTER")
    print('for the Telegram configuration if you want to skip it for now just press ENTER after each input')
    print("You can run the script with the '-config' option to configure or update the variables.")
    # Read the cookie value from a .txt file specified by the user
    cookie_file_path = input("Enter the path to the .txt file containing the cookie value: ").strip("'\"")
    if cookie_file_path:
        with open(cookie_file_path, "r") as cookie_file:
            cookie = cookie_file.read().strip()

    # Check if the user provided new input for api_id, api_hash, and phone
    new_api_id = input("Enter your Telegram API ID (press Enter to keep the current value): ").strip()
    new_api_hash = input("Enter your Telegram API hash (press Enter to keep the current value): ").strip()
    new_phone = input("Enter your phone number with international prefix (e.g., +520000000000) (press Enter to keep the current value): ").strip()

    # Update the variables in config.py only if there is new input
    if new_api_id:
        api_id = new_api_id
    else:
        api_id = conf['api_id']

    if new_api_hash:
        api_hash = new_api_hash
    else:
        api_hash = conf['api_hash']

    if new_phone:
        phone = new_phone
    else:
        phone = conf['phone']

    # Save the updated configuration to config.py
    conf['cookie'] = cookie
    conf['api_id'] = api_id
    conf['api_hash'] = api_hash
    conf['phone'] = phone
    save_conf(conf)

def main():
    if conf['cookie'] is None:
        configure()

    # Default values script
    class CustomArgumentParser(argparse.ArgumentParser):
        def __init__(self, *args, **kwargs):
            kwargs['add_help'] = False  # Disable the default help option
            super().__init__(*args, **kwargs)

        def format_help(self):
            instructions = """
    \033[1;35m=========== Instructions ===========\033[0m

    \033[91m YOU REQUIRE A SUBSCRIPTION, THIS CODE DOESN'T DOWNLOAD VIDEOS FOR PEOPLE WITHOUT AN ACTIVE SUBSCRIPTION ON SKILLSHARE \033[0m

    \033[1mFollow these steps to make the code work:\033[0m

    \033[33m1 - Open skillshare.com on Chrome and using the inspection window.\033[0m
    \033[33m    1.1 - Go to network and select the \033[1mDoc filter\033[0m \033[0m
    \033[33m    1.2 - Press the first document and inside the headers copy all the Cookies from the Request Headers\033[0m
    \033[33m    1.3 - Paste the cookies into the file config.py\033[0m
    \033[33m2 - If you have plans of backup your tutorials on Telegram you need to create an app:\033[0m
    \033[33m    2.1 - Go to \033[1mhttps://my.telegram.org/auth\033[0m\033[0m
    \033[33m    2.2 - Enter your phone number wtih the international prefix code\033[0m
    \033[33m    2.3 - Click on \033[1mAPI development tools\033[0m\033[0m
    \033[33m    2.5 - Create you App\033[0m
    \033[33m    2.6 - use down -config to open the initial configuration\033[0m
    \033[33m    2.7 - Copy and paste your App api_id, api_hash and your phone number when it's asked\033[0m
    \033[33m3 - Run the script following the next template:\033[0m

    """
            help_text = super().format_help()
            help_text = help_text.replace("[-h] ", "").replace("[-config] ", "").strip()
            return instructions + help_text
        
    # parser = CustomArgumentParser()
    parser = CustomArgumentParser(prog='skillshare-download')  # Add "python" before the script name
    parser.add_argument('-h', '--help', action='help', help='show the current help')
    parser.add_argument('id', nargs='?', type=str, default=None, help='your class id, ex: 1749908541')
    parser.add_argument("-config", action="store_true", help="Configure the Skillshare Downloader")
    parser.add_argument('-s', type=str, default='en-US', choices=['es-MX', 'de', 'en-US', 'pt', 'fr'], help='Subtitles language')
    parser.add_argument('-r', type=str, default='854x480', choices=['1920x1080', '1728x1080', '1280x720', '1152x720', '854x480', '768x480', '640x360', '576x360', '426x240', '384x240'], help='Video resolution')
    parser.add_argument('-t', type=str, default=None, help='Your telegram group to save the files in format .mp4')
    parser.add_argument("-e", action="store_true", help="Erase the files after upload (only if there\'s a valid telegram group or id)")

    args = parser.parse_args()
    if args.config:
        configure()
        exit(0)

    if args.id is None:
        parser.error("the following arguments are required: id")

    if args.id is None and args.config is None:
        parser.print_help()
        exit()
    if args.t and conf['api_id'] is None:
        configure()
        exit(0)
    if args.t and conf['api_hash'] is None:
        configure()
        exit(0)
    if args.t and conf['phone'] is None:
        configure()
        exit(0)

    dl = Downloader(cookie=conf['cookie'], api_id=conf['api_id'], api_hash=conf['api_hash'], phone=conf['phone'])
    dl.download(class_id=args.id, language=args.s, resolution=args.r, telegram=args.t, erase=args.e)

if __name__ == "__main__":
    main()