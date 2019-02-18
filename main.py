import pyperclip
import cv2


def convert_to_5bit(data):
    max_hex = 255

    percent = data / max_hex

    five_bit = int(percent * 31)

    return five_bit


def convert_to_6bit(data):
    max_hex = 255

    percent = data / max_hex

    six_bit = int(percent * 63)

    return six_bit


def convert_to_565(b, g, r):
    result = convert_to_5bit(r)
    result = result << 6
    result = result | convert_to_6bit(g)
    result = result << 5
    result = result | convert_to_5bit(b)

    return '0x' + format(result, '04X')


def resize(img):
    user_input = input("Enter desired width\n")
    width = int(user_input)
    user_input = input("Enter desired height\n")
    height = int(user_input)

    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    return resized


def main():
    user_input = input("Enter image path\n")
    path = user_input

    print("Here we go!")
    image = cv2.imread(user_input)

    resized = resize(image)

    height, width, channels = image.shape

    print(height, width, channels)

    result = "{ " + hex(height) + ", " + hex(width) + ", " + "\n"
    for x in range(len(resized)):
        for y in range(len(resized[x])):
            result += convert_to_565(resized[x][y][0], resized[x][y][1], resized[x][y][2]) + ', '
        result += "\n"

    result = result[0:-3] + "};"

    print(result)

    pyperclip.copy(result)

    file = open("result.txt", "w")

    file.write(result)

    file.close()

    cv2.imshow('Image', resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
