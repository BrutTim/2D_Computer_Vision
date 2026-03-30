import matplotlib.pyplot as plt
import numpy as np
from skimage import io

def rgb_to_gray(image):

    if image.ndim == 2:
        return image.astype(np.uint8)

    hoehe, breite = image.shape[0], image.shape[1]
    gray = np.zeros((hoehe, breite), dtype=np.uint8)

    for y in range(hoehe):
        for x in range(breite):
            r = int(image[y, x, 0])
            g = int(image[y, x, 1])
            b = int(image[y, x, 2])
            graywert = int(0.299 * r + 0.587 * g + 0.114 * b)
            gray[y, x] = graywert

    return gray


def computeHisto(image):

    gray = rgb_to_gray(image)
    histo = np.zeros(256, dtype=np.int64)

    hoehe, breite = gray.shape
    for y in range(hoehe):
        for x in range(breite):
            intensitaet = int(gray[y, x])
            histo[intensitaet] += 1

    return histo


def plot_image(ax, image, title, cmap=None):
    ax.imshow(image, cmap=cmap)
    ax.set_title(title)
    ax.axis("off")


def plot_histogram(ax, histo, title):
    ax.bar(np.arange(256), histo, width=1.0, color="black")
    ax.set_title(title)
    ax.set_xlim(0, 255)
    ax.set_xlabel("Intensitaet")
    ax.set_ylabel("Anzahl Pixel")


def create_brightening_lut():

    lut = np.zeros(256, dtype=np.uint8)

    for i in range(256):
        if i < 80:
            neuer_wert = int(i * 1.8)
        elif i < 160:
            neuer_wert = int(i * 1.2 + 20)
        else:
            neuer_wert = int(i * 1.00 + 5)

        if neuer_wert > 255:
            neuer_wert = 255

        lut[i] = neuer_wert

    return lut


def apply_lut(image, lut):

    result = np.zeros_like(image)

    if image.ndim == 2:
        hoehe, breite = image.shape
        for y in range(hoehe):
            for x in range(breite):
                result[y, x] = lut[int(image[y, x])]
        return result

    hoehe, breite, kanaele = image.shape
    for y in range(hoehe):
        for x in range(breite):
            for c in range(kanaele):
                result[y, x, c] = lut[int(image[y, x, c])]

    return result

def show_histograms(images, histograms, names):
    fig, axes = plt.subplots(len(images), 2, figsize=(12, 4 * len(images)))

    for i, (image, histo, name) in enumerate(zip(images, histograms, names)):
        gray = rgb_to_gray(image)
        plot_image(axes[i, 0], gray, f"{name} (Graustufen)", cmap="gray")
        plot_histogram(axes[i, 1], histo, f"Histogramm {name}")

    plt.tight_layout()
    plt.show()


def show_lut_result(original_rgb):
    original_gray = rgb_to_gray(original_rgb)
    lut = create_brightening_lut()
    brightened_gray = apply_lut(original_gray, lut)

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    plot_image(axes[0, 0], original_gray, "Bild01 in Graustufen", cmap="gray")
    plot_histogram(axes[0, 1], computeHisto(original_gray), "Histogramm Bild01")
    plot_image(axes[1, 0], brightened_gray, "Bild01 mit Lookup-Tabelle aufgehellt", cmap="gray")
    plot_histogram(axes[1, 1], computeHisto(brightened_gray), "Histogramm nach Lookup-Tabelle")
    plt.tight_layout()
    plt.show()


def main():
    bildnamen = ["bild01.jpg", "bild02.jpg", "bild03.jpg", "bild04.jpg", "bild05.jpg", "monkey.jpg", "hidden.png", "sea_wall.jpg", "wood.jpg"]
    bilder = [io.imread(name) for name in bildnamen]
    histogramme = [computeHisto(bild) for bild in bilder]

    show_histograms(bilder, histogramme, bildnamen)
    show_lut_result(bilder[0])


if __name__ == "__main__":
    main()