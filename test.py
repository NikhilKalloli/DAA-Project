import time
import asyncio
from typing import Tuple, Optional
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
# from RITScraping import exam_macro
import pygame

EXAM_RESULTS_URL = "https://exam.msrit.edu/"
UNSUCCESSFUL_LOOKUP_MESSAGE = "Oops!!! your USN could not be found in our result database, please verify the USN and click here to try again"
SITE_DOWN_MESSAGE = "This site is down for maintenance. Please check back soon."


def generate_payload(usn: str) -> dict:
    return {
        "usn": usn.upper(),
        "osolCatchaTxt": "",
        "osolCatchaTxtInst": "0",
        "option": "com_examresult",
        "task": "getResult"
    }


def prepare_exam_lookup(usn: str) -> Tuple[str, dict]:
    return EXAM_RESULTS_URL, generate_payload(usn)


async def fetch_exam_results(url: str, payload: dict) -> Optional[str]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=payload) as response:
                response.raise_for_status()  # Raises an error for bad responses
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"Request failed: {e}")
            return None


async def is_result_available(url: str) -> bool:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                html_content = await response.text()
                soup = BeautifulSoup(html_content, "html.parser")
                if soup.find("h2").text == SITE_DOWN_MESSAGE:
                    return False
        except aiohttp.ClientError as e:
            print(f"Request failed: {e}")
            return False


def parse_exam_results(soup: BeautifulSoup) -> bool:
    print("\n--- Exam Results ---")
    print(f"Name: {soup.find('h3').text}")
    print(f"SGPA: {soup.find_all('p')[3].text}")
    print(f"Sem: {soup.find('p').text.split(',')[-1].strip()}")
    return True


def play_alarm_sound():
    """Play an alarm sound using pygame."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('mission-impossible.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the music to finish playing
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing sound with pygame: {e}")


async def main():
    results_found = False
    YEAR = 2022
    DEPT = "CI"
    TEMP = False
    EVEN = False
    DRY = False
    usn = f"1MS{str(YEAR)[-2:]}{DEPT}001"  # Example USN

    while not results_found:
        now = datetime.now().strftime('%H:%M:%S')
        print(f"\nChecking results at {now}...")

        test_url, test_payload = prepare_exam_lookup(usn)
        test_html_content = await fetch_exam_results(test_url, test_payload)
        if test_html_content:
            test_soup = BeautifulSoup(test_html_content, "html.parser")
            if parse_exam_results(test_soup):
                print("Test Success")
            else:
                print("Results not found. Will check again in 1 minute.")
        else:
            print("Failed to fetch results. Will try again in 1 minute.")

        url, payload = prepare_exam_lookup(usn)
        html_content = await fetch_exam_results(url, payload)

        # if html_content:
        #     soup = BeautifulSoup(html_content, "html.parser")
        #     if parse_exam_results(soup):
        #         print("Results found! Process complete.")
        #         await exam_macro(YEAR, DEPT, TEMP, EVEN, start=1, stop=200, dry=DRY)
        #         # The above will download the csv file of all the students in the department
        #         play_alarm_sound()
        #         results_found = True
        #     else:
        #         print("Results not found. Will check again in 1 minute.")
        # else:
        #     print("Failed to fetch results. Will try again in 1 minute.")

        if not results_found:
            await asyncio.sleep(60)


asyncio.run(main())