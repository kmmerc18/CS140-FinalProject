import pygame, util, color


def sketch():
    dog = pygame.image.load(input("What image would you like to edit? "))
    sizex = int(input("What width should the image be? "))
    sizey = int(input("What height should the image be? "))
    t = input("How much detail should be included, on a scale of 1 - 10? ")  # threshold of color difference
    z = input("How many times should the dot-filter be run? ")
    t = 45 - (float(t) + 1) * 4

    dog = pygame.transform.scale(dog, (sizex, sizey))
    win = pygame.display.set_mode((dog.get_width(), dog.get_height()))
    blacklistx = []
    blacklisty = []
    whitelistx = []
    whitelisty = []

    win.blit(dog, (0, 0))

    # look at each pixel to determine the color of it
    for y in range(0, win.get_height()):
        for x in range(0, win.get_width()):
            (r, g, b, a) = win.get_at((x, y))
            mainr = r
            maing = g
            mainb = b

            c = 0
            # Look at the neighbors of a pixel at (x, y) to see if there's a color change
            for column in range(y - 2, y + 3):
                for row in range(x - 2, x + 3):

                    # Define the border pixels as black
                    if x < 2 or y < 2 or x > win.get_width() - 3 or y > win.get_height() - 3:
                        blacklistx.append(x)
                        blacklisty.append(y)

                    # if not a border pixel
                    else:
                        (r1, g1, b1, a1) = win.get_at((row, column))

                        # find the difference of the pixel color values
                        rd = abs(mainr - r1)
                        gd = abs(maing - g1)
                        bd = abs(mainb - b1)

                        # if color change is present, count how many neighbors are different
                        if rd > t or gd > t or bd > t:
                            c = c + 1

            # if enough neighbors are different, add the pixel to the black list
            if c >= 12:  # out of 24 including the main pixel
                blacklistx.append(x)
                blacklisty.append(y)

            # if few neighbors are different, add the pixel to the white list
            else:
                whitelistx.append(x)
                whitelisty.append(y)

    # set the pixels in each list to their end colors
    for coordinate in range(0, len(blacklistx) - 1):
        win.set_at((blacklistx[coordinate], blacklisty[coordinate]), color.black)
    for coordinate in range(0, len(whitelistx) - 1):
        win.set_at((whitelistx[coordinate], whitelisty[coordinate]), color.white)

    # removing arbitrary black spots with a mean filter kind of: "dot filter"
    v = 0
    while v < int(z):
        nxs = []  # new x values
        nys = []  # new y values
        for y in range(1, win.get_height() - 1):
            for x in range(1, win.get_width() - 1):
                rs = 0
                (r1, g1, b1, a1) = win.get_at((x, y))
                if r1 < 255:
                    for ny in range(y - 1, y + 2):
                        for nx in range(x - 1, x + 2):
                            (r, g, b, a) = win.get_at((nx, ny))
                            rs = rs + r
                mean = rs / 9
                if mean > 170:
                    nxs.append(x)
                    nys.append(y)
        for c in range(len(nxs)):
            win.set_at((nxs[c], nys[c]), color.white)
        v = v + 1

    # anti-aliasing attempt
    for y in range(0, win.get_height()):
        for x in range(0, win.get_width()):
            (rm, gm, bm, am) = win.get_at((x, y))  # establishing the main pixel to compare to

            for row in range(y - 1, y + 2):
                for column in range(x - 1, x + 2):

                    if x < 1 or y < 1 or x > win.get_width() - 2 or y > win.get_height() - 2:
                        (x, y) = (x, y)

                    else:
                        (r, g, b, a) = win.get_at((column, row))
                        if (r, g, b) != (rm, gm, bm):
                            if (r, g, b) == color.black:
                                win.set_at((x, y), color.grey)

    # round two of anti-aliasing
    for y in range(0, win.get_height()):
        for x in range(0, win.get_width()):
            (rm, gm, bm, am) = win.get_at((x, y))  # establishing the main pixel to compare to

            for row in range(y - 1, y + 2):
                for column in range(x - 1, x + 2):

                    if x < 1 or y < 1 or x > win.get_width() - 2 or y > win.get_height() - 2:
                        (x, y) = (x, y)

                    else:
                        (r, g, b, a) = win.get_at((column, row))
                        if (r, g, b) == color.grey and (rm, gm, bm) == color.black:
                                win.set_at((column, row), color.lightgrey)

    pygame.display.update()
    pygame.event.poll()

    util.wait_for_quit()
    pygame.image.save(win, input("Name: ") + ".jpg")


sketch()

