import pygame
import random
import sys

pygame.init()

# Ayarlar
HUCRE = 20
GENISLIK, YUKSEKLIK = 400, 400
FPS = 10

BEYAZ = (255, 255, 255)
YESIL = (40, 160, 90)
KOYU_YESIL = (20, 100, 60)
KIRMIZI = (200, 60, 60)
SIYAH = (20, 20, 20)

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Yılan Oyunu")
saat = pygame.time.Clock()
yazi_tipi = pygame.font.SysFont("arial", 24)


def rastgele_yem(yilan):
    while True:
        x = random.randrange(0, GENISLIK // HUCRE) * HUCRE
        y = random.randrange(0, YUKSEKLIK // HUCRE) * HUCRE
        if (x, y) not in yilan:
            return (x, y)


def metin_ciz(metin, x, y, renk=BEYAZ):
    yuzey = yazi_tipi.render(metin, True, renk)
    ekran.blit(yuzey, (x, y))


def oyunu_calistir():
    yilan = [(200, 200), (180, 200), (160, 200)]
    yon = (HUCRE, 0)
    yem = rastgele_yem(yilan)
    skor = 0
    canli = True

    while True:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if olay.type == pygame.KEYDOWN and canli:
                if olay.key == pygame.K_UP and yon != (0, HUCRE):
                    yon = (0, -HUCRE)
                elif olay.key == pygame.K_DOWN and yon != (0, -HUCRE):
                    yon = (0, HUCRE)
                elif olay.key == pygame.K_LEFT and yon != (HUCRE, 0):
                    yon = (-HUCRE, 0)
                elif olay.key == pygame.K_RIGHT and yon != (-HUCRE, 0):
                    yon = (HUCRE, 0)
            if olay.type == pygame.KEYDOWN and not canli:
                if olay.key == pygame.K_r:
                    oyunu_calistir()
                    return

        if canli:
            bas = (yilan[0][0] + yon[0], yilan[0][1] + yon[1])

            # Duvar veya kendine çarpma kontrolü
            if (
                bas[0] < 0 or bas[0] >= GENISLIK or
                bas[1] < 0 or bas[1] >= YUKSEKLIK or
                bas in yilan
            ):
                canli = False
            else:
                yilan.insert(0, bas)
                if bas == yem:
                    skor += 10
                    yem = rastgele_yem(yilan)
                else:
                    yilan.pop()

        # Çizim
        ekran.fill(SIYAH)
        for i, parca in enumerate(yilan):
            renk = YESIL if i == 0 else KOYU_YESIL
            pygame.draw.rect(ekran, renk, (*parca, HUCRE, HUCRE))
        pygame.draw.rect(ekran, KIRMIZI, (*yem, HUCRE, HUCRE))

        metin_ciz(f"Skor: {skor}", 8, 8)

        if not canli:
            metin_ciz("Oyun bitti! Tekrar için R'ye bas", 40, YUKSEKLIK // 2 - 12, KIRMIZI)

        pygame.display.flip()
        saat.tick(FPS)


if __name__ == "__main__":
    oyunu_calistir()
