from pytube import YouTube, Playlist
from colorama import init, Fore
from os import system, name

option_main_list = 1
option_main_video = 2
option_main_exit = 3

option_resolution_highest = 1
option_resolution_lowest = 2
option_resolution_audio = 3

def clear():
    # windows
    if name == "nt":
        _ = system("cls")
    # max / linux
        _ = system("clear")

def show_splash():
    print(Fore.GREEN +  f"Kimia Software Presents:\033[39m")
    print(Fore.LIGHTBLUE_EX + f"██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗██╗   ██╗████████╗██╗   ██╗██████╗ ███████╗\033[39m")
    print(Fore.LIGHTBLUE_EX + f"██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║╚██╗ ██╔╝╚══██╔══╝██║   ██║██╔══██╗██╔════╝\033[39m")
    print(Fore.WHITE +        f"██║ █╗ ██║███████║   ██║   ██║     ███████║ ╚████╔╝    ██║   ██║   ██║██████╔╝█████╗  \033[39m")
    print(Fore.WHITE +        f"██║███╗██║██╔══██║   ██║   ██║     ██╔══██║  ╚██╔╝     ██║   ██║   ██║██╔══██╗██╔══╝  \033[39m")
    print(Fore.LIGHTBLUE_EX + f"╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║   ██║      ██║   ╚██████╔╝██████╔╝███████╗\033[39m")
    print(Fore.LIGHTBLUE_EX + f" ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝   ╚═╝      ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝\033[39m")
    print(Fore.YELLOW + f"WatchyTube 1.0\033[39m")
    print(Fore.RED + f"YouTube Downloader App\033[39m")
    print()
    print()

def show_main_menu():
    print("MAIN MENU")
    print(Fore.GREEN + f"{str(option_main_list)}. Download List\033[39m")
    print(Fore.GREEN + f"{str(option_main_video)}. Download Video\033[39m")
    print(Fore.RED + f"{str(option_main_exit)}. Exit\033[39m")

    selected_option = input(Fore.YELLOW + f"Select your option: \033[39m")
    while not selected_option.isnumeric() and not selected_option in (option_main_list, option_main_video, option_main_exit):
        selected_option = input(Fore.YELLOW + f"Select a valid option: \033[39m")

    print()
    
    return int(selected_option)
        
def ask_resolution():
    print("DOWNLOAD OPTIONS:")
    print(Fore.GREEN + f"{str(option_resolution_highest)}. Highest Resolution\033[39m")
    print(Fore.GREEN + f"{str(option_resolution_lowest)}. Lowest Resolution\033[39m")
    print(Fore.GREEN + f"{str(option_resolution_audio)}. Only Audio\033[39m")

    selected_option = input(Fore.YELLOW + f"Select your option: \033[39m")
    while not selected_option.isnumeric() and not selected_option in (option_resolution_highest, option_resolution_lowest, option_resolution_audio):
        selected_option = input(Fore.YELLOW + f"Select a valid option: \033[39m")

    print()
    
    return int(selected_option)


def ask_output_directory():
    directory = input(Fore.YELLOW + f"Paste your output directory: \033[39m")
    return directory


def on_complete(stream, file_path):
    print(Fore.GREEN + f"DOWNLOAD COMPLETE: {file_path}\033[39m")
    print()
    print()


def on_progress(stream, chunk, bytes_remaining):
    remaining = bytes_remaining / stream.filesize * 100
    percentage_complete = 100 - remaining

    color = ""
    if percentage_complete < 35:
        color = Fore.WHITE
    elif percentage_complete < 70:
        color = Fore.LIGHTBLUE_EX
    else:
        color = Fore.BLUE

    print(color + f"Progress: {round(percentage_complete, 2)}%\033[39m")

def show_list_information(playlist):
    print(Fore.GREEN + f"Title:            \033[39m {playlist.title}")
    print(Fore.GREEN + f"Number of videos: \033[39m {playlist.length}")


def download_list(link, resolution, output_directory):
    playlist = Playlist(link)

    show_list_information(playlist)

    counter = 0
    
    if ask_confirmation():
        for video in playlist.videos:
            video_object = YouTube(
                video.watch_url,
                on_complete_callback = on_complete,
                on_progress_callback = on_progress)

            counter += 1
            print(Fore.GREEN + f"VIDEO {str(counter)} OF {str(playlist.length)}\033[39m")

            download_final_video(video_object, resolution, output_directory)
    
    print(Fore.GREEN + f"LIST COMPLETELY DOWNLOADED AT: {output_directory}\033[39m")
    print()
    print()


def download_final_video(video_object, resolution, output_directory):
    print(Fore.GREEN + f"DOWNLOAD STARTED:  \033[39m")
    show_video_information(video_object)

    if resolution == option_resolution_highest:
        video_object.streams.get_highest_resolution().download(output_directory)
    elif resolution == option_resolution_lowest:
        video_object.streams.get_lowest_resolution().download(output_directory)
    elif resolution == option_resolution_audio:
        video_object.streams.get_audio_only().download(output_directory)

def download_video(link, resolution, output_directory):
    video_object = YouTube(
        link,
        on_complete_callback = on_complete,
        on_progress_callback = on_progress)

    show_video_information(video_object)

    if ask_confirmation():
        download_final_video(video_object, resolution, output_directory)

def show_video_information(video_object):
    print(Fore.GREEN + f"Title:  \033[39m {video_object.title}")
    print(Fore.GREEN + f"Length: \033[39m {round(video_object.length / 60,2)} minutes")
    print(Fore.GREEN + f"Views:  \033[39m {video_object.views / 1000000} million")
    print(Fore.GREEN + f"Author: \033[39m {video_object.author}")
    print()

def ask_confirmation():
    selected_option = input(Fore.YELLOW + f"Do you want to proceed? Y/N: \033[39m")

    while not selected_option.upper() in ("Y", "N"):
        selected_option = input(Fore.YELLOW + f"Select a valid option: \033[39m")

    return selected_option.upper() == "Y"

def main():
    clear()
    show_splash()
    main_option = 0    

    while main_option != option_main_exit:
        main_option = show_main_menu()
        resolution = ask_resolution()

        if main_option == option_main_list:
            link = input(Fore.YELLOW + f"Insert the link of the list: \033[39m")
            output_directory = ask_output_directory()
            download_list(link, resolution, output_directory)
        elif main_option == option_main_video:
            link = input(Fore.YELLOW + f"Insert the link of the video: \033[39m")
            output_directory = ask_output_directory()
            download_video(link, resolution, output_directory)

        main_option = show_main_menu()

main()