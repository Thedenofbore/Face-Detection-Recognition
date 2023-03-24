import os
import json
import requests
import time
from requests.exceptions import ConnectionError, RequestException

# Replace with your Bing Image Search API key
BING_API_KEY = '911b552272824a09a8bf31553a6136d3'

# List of science celebrities
science_celebrities = [
    "Ada Yonath",
    "Alan Guth",
    "Alice Roberts",
    "Andrew Wiles",
    "Angela Belcher",
    "Astro Teller",
    "Atul Butte",
    "Barbara Liskov",
    "Bernard Bigot",
    "Brian Greene",
    "Carlo Rovelli",
    "Catherine Mohr",
    "Chimamanda Ngozi Adichie",
    "Christiane Nüsslein-Volhard",
    "Claire Voisin",
    "Craig Venter",
    "Cynthia Kenyon",
    "Daniel Kahneman",
    "David Deutsch",
    "David Gross",
    "David J. Thouless",
    "David Spergel",
    "Dennis Lo",
    "Doris Tsao",
    "Edward Witten",
    "Elaine Fuchs",
    "Elon Musk",
    "Emmanuelle Charpentier",
    "Eric Lander",
    "Eric Topol",
    "Eve Marder",
    "Feng Zhang",
    "Frances Arnold",
    "Frank Wilczek",
    "Gero Miesenböck",
    "Gina Rippon",
    "Gustav Born",
    "Hannah Fry",
    "Hans Clevers",
    "Harald zur Hausen",
    "Helen Fisher",
    "Huda Zoghbi",
    "Ian Goodfellow",
    "Jack Szostak",
    "J. Craig Venter",
    "James Allison",
    "James P. Allison",
    "Jane Lubchenco",
    "Jane Richardson",
    "Jared Diamond",
    "Jay Keasling",
    "Jennifer Doudna",
    "Jocelyn Bell Burnell",
    "John Gurdon",
    "John Pendry",
    "Jonathan Eisen",
    "Jorge Cham",
    "Joseph Stiglitz",
    "Joshua Greene",
    "Juan Enriquez",
    "Jürgen Knoblich",
    "Kai-Fu Lee",
    "Karin Mölling",
    "Kathryn D. Sullivan",
    "Kathryn Hall",
    "Kathy Niakan",
    "Kip Thorne",
    "Lawrence Krauss",
    "Lene Vestergaard Hau",
    "Leslie Vosshall",
    "Linda Buck",
    "Lionel Messi",
    "Lisa Randall",
    "Luc Montagnier",
    "Luigi Naldini",
    "Luis von Ahn",
    "Manuel Blum",
    "Manuel Castells",
    "Marcela Gómez",
    "Marek Kukula",
    "Margaret Hamburg",
    "Mark Post",
    "Mark Zuckerberg",
    "Mary-Claire King",
    "Matthew Meselson",
    "Max Levchin",
    "Max Tegmark",
    "May-Britt Moser",
    "Melissa Franklin",
    "Michael Faraday",
    "Michael Levitt",
    "Michael Rosbash",
    "Michel Mayor",
    "Michelle Simmons",
    "Mihir M. Patel",
    "Mikhail Gromov",
    "Nalini Nadkarni",
    "Natalie Batalha",
    "Nergis Mavalvala",
    "Nick Bostrom",
    "Nita Ahuja",
    "Norman Foster",
    "Oliver Smithies",
    "Oren Etzioni",
    "Paola Arlotta",
    "Patricia Churchland",
	"Patrick Soon-Shiong",
	"Paul Nurse",
	"Peter Agre",
	"Peter Higgs",
	"Peter Thiel",
	"Pierre Omidyar",
	"Raj Reddy",
	"Randy W. Jirtle",
	"Ray Kurzweil",
	"Rebecca Goldstein",
	"Richard Dawkins",
	"Richard Ernst",
	"Richard Roberts",
	"Richard Thaler",
	"Richard Wrangham",
	"Robert Langer",
	"Robert Sapolsky",
	"Roger Penrose",
	"Rosetta Elkin",
	"Sallie Chisholm",
	"Salvador Moncada",
	"Sam Harris",
	"Sara Seager",
	"Saul Perlmutter",
	"Seth Lloyd",
	"Shafi Goldwasser",
	"Shirley Ann Jackson",
	"Shuji Nakamura",
	"Siddhartha Mukherjee",
	"Simon Levin",
	"Sir Martin Evans",
	"Sonia Suter",
	"Srinivasa Varadhan",
	"Stephen Hawking",
	"Steven Chu",
	"Steven Pinker",
	"Stuart Firestein",
	"Suzanne Cory",
	"Svante Pääbo",
	"Sydney Brenner",
	"Tamas D. Gonda",
	"Terry Sejnowski",
	"Thierry Vrain",
	"Thomas Jessell",
	"Thomas Piketty",
	"Tim Berners-Lee",
	"Tim Hunt",
	"Ting Xu",
	"Tom Cheeseman",
	"Tom Frieden",
	"Tom Siebel",
	"Tracy Caldwell Dyson",
	"Uri Alon",
	"Vandana Shiva",
	"Viktor Frankl",
	"Vint Cerf",
	"Wafaa El-Sadr",
	"Wendy Suzuki",
	"Wolfgang Ketterle",
	"Yann LeCun",
	"Yoshua Bengio",
	"Yves Chauvin",
	"Zeresenay Alemseged"
	]

# Function to download image
def download_image(url, save_path, celeb_name):
    retries = 3
    while retries > 0:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                ext = 'jpg' if url.endswith('.jpg') else 'png'
                with open(os.path.join(save_path, f'{celeb_name}.{ext}'), 'wb') as f:
                    f.write(response.content)
            break
        except (ConnectionError, RequestException) as e:
            print(f"Error downloading {celeb_name}'s image: {str(e)}")
            retries -= 1
            if retries > 0:
                print(f"Retrying {celeb_name} in 5 seconds...")
                time.sleep(5)
            else:
                print(f"Failed to download {celeb_name}'s image after 3 retries.")

# Function to search for images
def search_image(celeb_name):
    search_url = f"https://api.bing.microsoft.com/v7.0/images/search?q={celeb_name.replace(' ', '+')}"
    headers = {
        "Ocp-Apim-Subscription-Key": BING_API_KEY
    }
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        for image in json_data['value']:
            img_url = image['contentUrl']
            if img_url and (img_url.endswith('.jpg') or img_url.endswith('.png')):
                return img_url
    return None

# Function to download images of science celebrities
def download_science_celebrities_images(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for celeb in science_celebrities:
        print(f"Searching for {celeb}'s image...")
        image_url = search_image(celeb)
        if image_url:
            print(f"Downloading {celeb}'s image...")
            download_image(image_url, folder_path, celeb)
        else:
            print(f"Couldn't find an image for {celeb}")

# Main function
def main():
    folder_path = r"/workspaces/Face-Detection-Recognition/images"  # Replace with the desired folder path
    download_science_celebrities_images(folder_path)

if __name__ == "__main__":
    main()
