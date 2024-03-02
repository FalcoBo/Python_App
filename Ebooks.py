import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from docx import Document
import os

class Ebooks:
    def __init__(self):
        self.book_title = None
        self.author_name = None
        self.first_chapter = None
        self.paragraph_lengths = None

    # Télécharger une version texte d'un livre à partir du site web du Project Gutenberg
    def download_book(self, url):
        response = requests.get(url)
        return response.text

    # Extraire le titre du livre, le nom de l'auteur et le premier chapitre du livre
    def extract_book_info(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        self.book_title = soup.find('h1').text
        self.author_name = soup.find('h2').text
        self.first_chapter = soup.find('p').text

    # Compter le nombre de mots dans chacun des paragraphes du premier chapitre
    def count_paragraph_words(self):
        paragraphs = self.first_chapter.split('\n\n')
        self.paragraph_lengths = [self.round_word_count(len(p.split())) for p in paragraphs]

    # Arrondir le nombre de mots à la dizaine
    def round_word_count(self, count):
        return round(count, -1)

    # Créer un graphique montrant la distribution des longueurs des paragraphes
    def plot_paragraph_lengths(self):
        plt.hist(self.paragraph_lengths, bins=len(set(self.paragraph_lengths)))
        plt.xlabel('Nombre de mots par paragraphe')
        plt.ylabel('Nombre de paragraphes')
        plt.title('Distribution des longueurs des paragraphes')
        plt.show()

    # Télécharger une image depuis Internet et la sauvegarder localement
    def download_image(self, url, filename):
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)

    # Recadrer et redimensionner l'image téléchargée
    def resize_image(self, image_path, output_path, width, height):
        pass

    # Lire une deuxième image depuis le disque, la faire pivoter selon un angle choisi, puis la coller dans la première image
    def rotate_and_paste_image(self, image_path1, image_path2, output_path, angle):
        # Code pour lire, faire pivoter et coller les images
        pass

    # Créer un document Word comprenant la page de titre et la page avec le graphique
    def create_word_document(self, filename):
        doc = Document()
        # Page de titre
        doc.add_heading('Titre du livre : ' + self.book_title, level=1)
        doc.add_paragraph('Auteur du livre : ' + self.author_name)
        doc.add_picture('image1.jpg', width=Document().page_width)
        doc.add_heading('Auteur du rapport : Votre nom', level=2)
        doc.add_page_break()
        # Page avec le graphique
        doc.add_heading('Distribution des longueurs des paragraphes', level=1)
        doc.add_paragraph('Description de l\'image : explication de l\'intrigue...')
        self.plot_paragraph_lengths()
        doc.add_picture('distribution_paragraphes.png', width=Document().page_width)
        doc.save(filename)