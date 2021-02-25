from PIL import Image, ImageDraw


# mode = int(input('mode:')) #Считываем номер преобразования.
# image = Image.open("temp.jpg") #Открываем изображение.
#from PIL.ImageDraw import ImageDraw

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    try:
        res=n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'
    except Exception: res=""
    return res
    # return ''.join(map(lambda x: chr(int(x, 2)), bits))

def encrypt(message):
    image = Image.open('kop.bmp')  # Can be many different formats.
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.

    pix = image.load()
    width = image.size[0]-2  # Определяем ширину.
    height = image.size[1]-2  # Определяем высоту.
    print(image.size)  # Get the width and hight of the image for iterating over
    print(pix[0, 0])  # Get the RGBA Value of the a pixel of an image


    size= len(message)
    print("количество символов в сообщении")
    print(size)
    # pix[x,y] = value  # Set the RGBA Value of the image (tuple)
    count=0
    for i in range(2, width, 2):
        for j in range(2, height, 2):
            r = pix[i, j][0]
            g = pix[i, j][1]
            b = pix[i, j][2]

            if (message [count] == '1'):
                b = (int) (b + (0.1 * (0.3 * r + 0.59 * g + 0.11 * b)))
                draw.point((i, j), (r, g, b))
            if (message [count] == '0'):
                b = (int) (b - (0.1 * (0.3 * r + 0.59 * g + 0.11 * b)))
                draw.point((i, j), (r, g, b))
            count+=1
            if(size <= count):
                image.show()
                image.save('kopEncrypt.bmp')  # Save the modified pixels as .png
                return


def decrypt():
    image = Image.open('kopEncrypt.bmp')  # Can be many different formats.

    pix = image.load()
    width = image.size[0]-2 # Определяем ширину.
    height = image.size[1]-2 # Определяем высоту.
    print(image.size)  # Get the width and hight of the image for iterating over
    print(pix[0, 0])  # Get the RGBA Value of the a pixel of an image
    print("Высота ")
    print(height)
    print("ширина ")
    print(width)
    message = ""
    count = 0
    for i in range(2, width,2):
        for j in range(2, height,2):

            #print (i,j)
            Bsum=0
            # Bsum += pix[i + 2, j][2]
            # Bsum += pix[i + 1, j][2]
            # Bsum += pix[i - 1, j][2]
            # Bsum += pix[i - 2, j][2]
            #
            # Bsum += pix[i , j+2][2]
            # Bsum += pix[i , j+1][2]
            # Bsum += pix[i , j-1][2]
            # Bsum += pix[i , j-2][2]
########
            Bsum += pix[i + 1, j][2]
            Bsum += pix[i - 1, j][2]

            Bsum += pix[i, j+1][2]
            Bsum += pix[i, j-1][2]

            Bsum += pix[i-1, j-1][2]
            Bsum += pix[i+1, j + 1][2]
            Bsum += pix[i-1, j + 1][2]
            Bsum += pix[i+1, j - 2][2]
######

            Bsum = Bsum/8

            b = pix[i, j][2]

            if (b>Bsum):
                message += '1'
            if (b<Bsum):
                message += '0'

    print(message)

    charcount=0
    message8bit=""
    messageResult=""
    for char in message:
        message8bit += char
        charcount += 1
        if(charcount==8):
            print(message8bit)
            messageResult += text_from_bits(message8bit)
            # print (messageResult)
            charcount=0
            message8bit=""


    print(messageResult)


print("Введите сообщение")
msg=input()
print(text_to_bits(msg))
encrypt(text_to_bits(msg))
decrypt()
# pix = image.load() #Выгружаем значения пикселей.




