import cv2
import numpy as np
import sys

BUTTONS_BAND_HEIGHT = 180
BUTTONS_HEIGHT = 30
BUTTONS_WIDTH = 50
OFFSET_BUTTONS = 10
MAX_BUTTONS = 7

def on_button_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global image, sticker_image
        height, width = image.shape[:2]
        # Lógica para tratar o clique do botão
        if is_button_clicked(bt_invert_position, x, y):
            image = 255 - image

        elif is_button_clicked(bt_gray_position, x, y):
            gray_image = np.mean(image, axis=2, keepdims=True).astype(np.uint8)
            gray_image = np.repeat(gray_image, 3, axis=2)
            image = gray_image

        elif is_button_clicked(bt_blur_position, x, y):
            image = cv2.blur(image, (height // 20, width // 20))

        elif is_button_clicked(bt_circle_position, x, y):
            mask = np.zeros((height, width), dtype=np.uint8)
            cv2.circle(mask, (width // 2, height // 2), int(min(height, width) * 0.5), (255), -1)
            image = cv2.bitwise_and(image, image, mask=mask)

        elif is_button_clicked(bt_heart_position, x, y):
            heartMask = cv2.imread('heart.jpg')
            heartMask = 255 - heartMask
            heartMask = cv2.resize(heartMask, (image.shape[1], image.shape[0]))
            image = cv2.bitwise_and(heartMask, image)    

        elif is_button_clicked(bt_fliph_position, x, y):
            image = cv2.flip(image, 0)

        elif is_button_clicked(bt_flipv_position, x, y):
            image = cv2.flip(image, 1)

        elif is_button_clicked(bt_red_position, x, y):
            channel_b, channel_g, channel_r = cv2.split(image)
            zeros = np.zeros(image.shape[:2], dtype=np.uint8)
            image = cv2.merge((zeros, zeros, channel_r))

        elif is_button_clicked(bt_green_position, x, y):
            channel_b, channel_g, channel_r = cv2.split(image)
            zeros = np.zeros(image.shape[:2], dtype=np.uint8)
            image = cv2.merge((zeros, channel_g, zeros))


        elif is_button_clicked(bt_blue_position, x, y):
            channel_b, channel_g, channel_r = cv2.split(image)
            zeros = np.zeros(image.shape[:2], dtype=np.uint8)
            image = cv2.merge((channel_b, zeros, zeros))

        elif is_button_clicked(bt_cool_position, x, y):
            sticker_image = cv2.imread('cool.png', cv2.IMREAD_UNCHANGED)

        elif is_button_clicked(bt_happy_position, x, y):
            sticker_image = cv2.imread('happy.png', cv2.IMREAD_UNCHANGED)

        elif is_button_clicked(bt_stop_position, x, y):
            sticker_image = cv2.imread('stop.png', cv2.IMREAD_UNCHANGED)

        elif is_button_clicked(bt_play_position, x, y):
            sticker_image = cv2.imread('play.png', cv2.IMREAD_UNCHANGED)

        elif is_button_clicked(bt_hat_position, x, y):
            sticker_image = cv2.imread('hat.png', cv2.IMREAD_UNCHANGED)            

        elif is_button_clicked(bt_reset_position, x, y):
            image = original_image.copy()

        elif is_button_clicked(bt_save_position, x, y):
            cv2.imwrite("saved.jpg", image)
        else:
            overlay_image = sticker_image.copy()
            overlay_height, overlay_width = overlay_image.shape[:2]
            overlay_image_alpha = overlay_image[:, :, 3]
            overlay_image_mask = cv2.bitwise_not(overlay_image_alpha)
            overlay_image_mask_not = cv2.bitwise_not(overlay_image_mask)
            overlay_image_rgb = overlay_image[:, :, :3]

            # Calcula as coordenadas para inserir a imagem com base no clique do mouse
            top_left_x = x - overlay_width // 2
            top_left_y = y - BUTTONS_BAND_HEIGHT - overlay_height // 2
            bottom_right_x = top_left_x + overlay_width
            bottom_right_y = top_left_y + overlay_height

            region_image = image[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
            region_bg = cv2.bitwise_and(region_image, region_image, mask=overlay_image_mask)
            region_fg = cv2.bitwise_and(overlay_image_rgb, overlay_image_rgb, mask=overlay_image_mask_not)
            final_region = cv2.add(region_bg, region_fg)

            image[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = final_region


def is_button_clicked(bt_position, x, y):
    return bt_position[0] < x < (bt_position[0] + BUTTONS_WIDTH) and bt_position[1] < y < (bt_position[1] + BUTTONS_HEIGHT)

def draw_button(text, position, buttons_band):
    vertical_offset = 0
    while (position + 1 > MAX_BUTTONS):
        position -= MAX_BUTTONS
        vertical_offset += BUTTONS_HEIGHT + 10
    band_width = buttons_band.shape[1]
    border = (band_width - ((BUTTONS_WIDTH + 10) * MAX_BUTTONS)) // 2
    # Cria botão
    button_text = text
    button_x = border + position * (BUTTONS_WIDTH + 10)
    button_y = (vertical_offset + BUTTONS_BAND_HEIGHT - BUTTONS_HEIGHT - ((BUTTONS_BAND_HEIGHT - BUTTONS_HEIGHT * 2)))
    cv2.rectangle(buttons_band, (button_x, button_y), (button_x + BUTTONS_WIDTH, button_y + BUTTONS_HEIGHT), (255, 128, 128), -1)
    cv2.putText(buttons_band, button_text, (button_x, button_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    return (button_x, button_y)

def main():
    # Define variáveis globais
    global original_image
    global image
    global sticker_image
    global bt_invert_position
    global bt_gray_position
    global bt_blur_position
    global bt_circle_position
    global bt_heart_position
    global bt_fliph_position
    global bt_flipv_position
    global bt_red_position
    global bt_green_position
    global bt_blue_position
    global bt_cool_position
    global bt_happy_position
    global bt_stop_position
    global bt_play_position
    global bt_hat_position
    global bt_reset_position
    global bt_save_position    


    # Verifica se pelo menos um argumento foi fornecido
    if len(sys.argv) < 2:
        print("Uso: python3 ./src/photoshop.py <imagem>")
        sys.exit(1)

    # Obtém o valor do path da imagem
    image_path = sys.argv[1]

    # Carrega imagem original
    original_image = cv2.imread(image_path)
    image = original_image.copy()

    # Carrega imagem default do sticker
    sticker_image = cv2.imread('cool.png', cv2.IMREAD_UNCHANGED)

    # Cria banda dos botões
    width = image.shape[1]
    buttons_band = np.zeros((BUTTONS_BAND_HEIGHT, width, 3), dtype=np.uint8)

    # Cria os botões
    bt_invert_position = draw_button("Invert", 0, buttons_band)
    bt_gray_position = draw_button("Gray", 1, buttons_band)
    bt_blur_position = draw_button("Blur", 2, buttons_band)
    bt_circle_position = draw_button("Circle", 3, buttons_band)
    bt_heart_position = draw_button("Heart", 4, buttons_band)
    bt_fliph_position = draw_button("Flip H", 5, buttons_band)
    bt_flipv_position = draw_button("Flip V", 6, buttons_band)
    bt_red_position = draw_button("Red", 7, buttons_band)
    bt_green_position = draw_button("Green", 8, buttons_band)
    bt_blue_position = draw_button("Blue", 9, buttons_band)
    bt_cool_position = draw_button("Cool", 10, buttons_band)
    bt_happy_position = draw_button("Happy", 11, buttons_band)
    bt_stop_position = draw_button("Stop", 12, buttons_band)
    bt_play_position = draw_button("Play", 13, buttons_band)
    bt_hat_position = draw_button("Hat", 14, buttons_band)
    bt_reset_position = draw_button("Reset", 15, buttons_band)
    bt_save_position = draw_button("Save", 16, buttons_band)

    # Exibe interface do photoshop
    cv2.namedWindow("Photoshop")
    cv2.setMouseCallback("Photoshop", on_button_click)
    while True:
        form = np.concatenate((buttons_band, image), axis=0)
        cv2.imshow("Photoshop", form)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

main()