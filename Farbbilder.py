import matplotlib.pyplot as plt
from skimage import io


def spiegle_bild(bild, richtung="horizontal"):

    hoehe, breite = bild.shape[0], bild.shape[1]

    gespiegeltes_bild = [[[0 for _ in range(len(bild[0][0]))]
                   for _ in range(breite)]
                  for _ in range(hoehe)]

    for y in range(hoehe):
        for x in range(breite):
            if richtung == "horizontal":
                gespiegeltes_bild[y][x] = bild[y][breite - 1 - x]
            else:
                gespiegeltes_bild[y][x] = bild[hoehe - 1 - y][x]

    return gespiegeltes_bild


def zeige_farbkanaele(bild):
    fig, achsen = plt.subplots(1, 3, figsize=(15, 5))
    farben = ["Rot", "Gruen", "Blau"]
    colormaps = ["Reds", "Greens", "Blues"]

    for i in range(3):
        achsen[i].imshow(bild[:, :, i], cmap=colormaps[i])
        achsen[i].set_title(f"{farben[i]}-Kanal")
        achsen[i].axis("off")

    plt.tight_layout()
    plt.show()


def main():
    bildpfad = "bild01.jpg"

    bild = io.imread(bildpfad)

    plt.figure(figsize=(6, 6))
    plt.imshow(bild)
    plt.title("Originalbild")
    plt.axis("off")
    plt.show()

    zeige_farbkanaele(bild)

    vertikal = spiegle_bild(bild, "horizontal")
    horizontal = spiegle_bild(bild, "vertikal")

    fig, achsen = plt.subplots(1, 3, figsize=(16, 5))
    achsen[0].imshow(bild)
    achsen[0].set_title("Original")
    achsen[1].imshow(horizontal)
    achsen[1].set_title("Horizontal gespiegelt")
    achsen[2].imshow(vertikal)
    achsen[2].set_title("Vertikal gespiegelt")

    for achse in achsen:
        achse.axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
