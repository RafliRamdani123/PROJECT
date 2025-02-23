# Import library yang dibutuhkan
import pygame
import random
from object import Coins, Fuel, Obstacle  
from object import Road, Player, Nitro, Tree, Button

# Inisialisasi pygame
pygame.init()

# Mengatur ukuran layar
SCREEN = WIDTH, HEIGHT = 288, 512
info = pygame.display.Info()
width = info.current_w
height = info.current_h

# Menentukan mode tampilan layar
if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

# Mengatur clock dan FPS
clock = pygame.time.Clock()
FPS = 30

# Posisi jalur mobil
lane_pos = [50, 95, 142, 190]

# Warna yang digunakan
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 20)

# Font untuk teks
font = pygame.font.SysFont('cursive', 32)
select_car = font.render('Select Car', True, WHITE)

# Memuat gambar yang dibutuhkan
bg = pygame.image.load('car2d/assets/bg.png')
home_img = pygame.image.load('car2d/assets/home.png')
play_img = pygame.image.load('car2d/assets/buttons/play.png')
end_img = pygame.image.load('car2d/assets/end.jpg')
end_img = pygame.transform.scale(end_img, (WIDTH, HEIGHT))
game_over_img = pygame.image.load('car2d/assets/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (220, 220))
coin_img = pygame.image.load('car2d/assets/coins/1.png')
dodge_img = pygame.image.load('car2d/assets/car_dodge.png')
left_arrow = pygame.image.load('car2d/assets/buttons/arrow.png')
right_arrow = pygame.transform.flip(left_arrow, True, False)
home_btn_img = pygame.image.load('car2d/assets/buttons/home.png')
replay_img = pygame.image.load('car2d/assets/buttons/replay.png')
sound_off_img = pygame.image.load("car2d/assets/buttons/soundOff.png")
sound_on_img = pygame.image.load("car2d/assets/buttons/soundOn.png")

# Memuat gambar mobil
cars = []
car_type = 0
for i in range(1, 9):
	img = pygame.image.load(f'car2d/assets/cars/{i}.png')
	img = pygame.transform.scale(img, (59, 101))
	cars.append(img)

# Memuat animasi nitro
nitro_frames = []
nitro_counter = 0
for i in range(6):
	img = pygame.image.load(f'car2d/assets/nitro/{i}.gif')
	img = pygame.transform.flip(img, False, True)
	img = pygame.transform.scale(img, (18, 36))
	nitro_frames.append(img)

# Fungsi untuk menghitung posisi tengah
def center(image):
	return (WIDTH // 2) - image.get_width() // 2

# Membuat tombol
play_btn = Button(play_img, (100, 34), center(play_img)+10, HEIGHT-80)
la_btn = Button(left_arrow, (32, 42), 40, 180)
ra_btn = Button(right_arrow, (32, 42), WIDTH-60, 180)
home_btn = Button(home_btn_img, (24, 24), WIDTH // 4 - 18, HEIGHT - 80)
replay_btn = Button(replay_img, (36,36), WIDTH // 2  - 18, HEIGHT - 86)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, HEIGHT - 80)

# Memuat suara yang dibutuhkan
click_fx = pygame.mixer.Sound('car2d/Sounds/click.mp3')
fuel_fx = pygame.mixer.Sound('car2d/Sounds/fuel.wav')
start_fx = pygame.mixer.Sound('car2d/Sounds/start.mp3')
restart_fx = pygame.mixer.Sound('car2d/Sounds/restart.mp3')
coin_fx = pygame.mixer.Sound('car2d/Sounds/coin.mp3')

# Memutar musik latar
pygame.mixer.music.load('car2d/Sounds/mixkit-tech-house-vibes-130.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.6)

# Membuat objek game
road = Road()
nitro = Nitro(WIDTH-80, HEIGHT-80)
p = Player(100, HEIGHT-120, car_type)
tree_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
fuel_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

# Variabel status game
home_page = True
car_page = False
game_page = False
over_page = False

# Variabel kontrol pemain
move_left = False
move_right = False
nitro_on = False
sound_on = True

# Variabel permainan
counter = 0
counter_inc = 1
speed = 3
dodged = 0
coins = 0
cfuel = 100

# Variabel animasi akhir
endx, enddx = 0, 0.5
gameovery = -50

# Loop utama permainan
running = True
while running:
	win.fill(BLACK)
	
	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

			if event.key == pygame.K_LEFT:
				move_left = True

			if event.key == pygame.K_RIGHT:
				move_right = True

			if event.key == pygame.K_n:
				nitro_on = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				move_left = False

			if event.key == pygame.K_RIGHT:
				move_right = False

			if event.key == pygame.K_n:
				nitro_on = False
				speed = 3
				counter_inc = 1

		if event.type == pygame.MOUSEBUTTONDOWN:
			x, y = event.pos

			if nitro.rect.collidepoint((x, y)):
				nitro_on = True
			else:
				if x <= WIDTH // 2:
					move_left = True
				else:
					move_right = True

		if event.type == pygame.MOUSEBUTTONUP:
			move_left = False
			move_right = False
			nitro_on = False
			speed = 3
			counter_inc = 1

	# Halaman utama
	if home_page:
		win.blit(home_img, (0,0))
		counter += 1
		if counter % 60 == 0:
			home_page = False
			car_page = True

	# Halaman pemilihan mobil
	if car_page:
		win.blit(select_car, (center(select_car), 80))

		win.blit(cars[car_type], (WIDTH//2-30, 150))
		if la_btn.draw(win):
			car_type -= 1
			click_fx.play()
			if car_type < 0:
				car_type = len(cars) - 1

		if ra_btn.draw(win):
			car_type += 1
			click_fx.play()
			if car_type >= len(cars):
				car_type = 0

		if play_btn.draw(win):
			car_page = False
			game_page = True

			start_fx.play()

			p = Player(100, HEIGHT-120, car_type)
			counter = 0
	# Halaman game over
	if over_page:
		# Menampilkan gambar dan teks akhir permainan
		win.blit(end_img, (endx, 0))
		endx += enddx
		if endx >= 10 or endx <= -10:
			enddx *= -1

		win.blit(game_over_img, (center(game_over_img), gameovery))
		if gameovery < 16:
			gameovery += 1

		# Menampilkan skor dan statistik akhir
		num_coin_img = font.render(f'{coins}', True, WHITE)
		num_dodge_img = font.render(f'{dodged}', True, WHITE)
		distance_img = font.render(f'Distance : {counter/1000:.2f} km', True, WHITE)

		win.blit(coin_img, (80, 240))
		win.blit(dodge_img, (50, 280))
		win.blit(num_coin_img, (180, 250))
		win.blit(num_dodge_img, (180, 300))
		win.blit(distance_img, (center(distance_img), 350))

		# Tombol untuk kembali ke menu utama atau mengulang permainan
		if home_btn.draw(win):
			# Reset status untuk kembali ke halaman utama
			over_page = False
			home_page = True

			coins = 0
			dodged = 0
			counter = 0
			nitro.gas = 0
			cfuel = 100

			endx, enddx = 0, 0.5
			gameovery = -50

		if replay_btn.draw(win):
			# Reset status untuk memulai ulang permainan
			over_page = False
			game_page = True

			coins = 0
			dodged = 0
			counter = 0
			nitro.gas = 0
			cfuel = 100

			endx, enddx = 0, 0.54
			gameovery = -50

			restart_fx.play()

		# Tombol untuk mengaktifkan/mematikan suara
		if sound_btn.draw(win):
			sound_on = not sound_on

			if sound_on:
				sound_btn.update_image(sound_on_img)
				pygame.mixer.music.play(loops=-1)
			else:
				sound_btn.update_image(sound_off_img)
				pygame.mixer.music.stop()

	# Halaman permainan
	if game_page:
		# Menampilkan latar belakang dan objek jalan
		win.blit(bg, (0,0))
		road.update(speed)
		road.draw(win)

		# Meningkatkan penghitung waktu
		counter += counter_inc

		# Menambahkan pohon secara berkala
		if counter % 60 == 0:
			tree = Tree(random.choice([-5, WIDTH-35]), -20)
			tree_group.add(tree)

		# Menambahkan koin atau bahan bakar secara berkala
		if counter % 270 == 0:
			type = random.choices([1, 2], weights=[6, 4], k=1)[0]
			x = random.choice(lane_pos) + 10
			if type == 1:
				# Menambahkan beberapa koin
				count = random.randint(1, 3)
				for i in range(count):
					coin = Coins(x, -100 - (25 * i))
					coin_group.add(coin)
			elif type == 2:
				# Menambahkan bahan bakar
				fuel = Fuel(x, -100)
				fuel_group.add(fuel)

		# Menambahkan rintangan secara berkala
		elif counter % 90 == 0:
			obs = random.choices([1, 2, 3], weights=[6, 2, 2], k=1)[0]
			obstacle = Obstacle(obs)
			obstacle_group.add(obstacle)

		# Efek nitro jika diaktifkan
		if nitro_on and nitro.gas > 0:
			x, y = p.rect.centerx - 8, p.rect.bottom - 10
			win.blit(nitro_frames[nitro_counter], (x, y))
			nitro_counter = (nitro_counter + 1) % len(nitro_frames)

			speed = 10
			if counter_inc == 1:
				counter = 0
				counter_inc = 5

		# Mematikan efek nitro jika habis
		if nitro.gas <= 0:
			speed = 3
			counter_inc = 1

		# Memperbarui dan menggambar objek
		nitro.update(nitro_on)
		nitro.draw(win)
		obstacle_group.update(speed)
		obstacle_group.draw(win)
		tree_group.update(speed)
		tree_group.draw(win)
		coin_group.update(speed)
		coin_group.draw(win)
		fuel_group.update(speed)
		fuel_group.draw(win)

		# Memperbarui dan menggambar pemain
		p.update(move_left, move_right)
		p.draw(win)

		# Menampilkan indikator bahan bakar
		if cfuel > 0:
			pygame.draw.rect(win, GREEN, (20, 20, cfuel, 15), border_radius=5)
		pygame.draw.rect(win, WHITE, (20, 20, 100, 15), 2, border_radius=5)
		cfuel -= 0.05

		# Deteksi tabrakan dan logika permainan
		for obstacle in obstacle_group:
			# Hapus rintangan yang keluar layar
			if obstacle.rect.y >= HEIGHT:
				if obstacle.type == 1:
					dodged += 1
				obstacle.kill() 

			# Tabrakan dengan rintangan
			if pygame.sprite.collide_mask(p, obstacle):
				pygame.draw.rect(win, RED, p.rect, 1)
				speed = 0

				# Beralih ke halaman game over
				game_page = False
				over_page = True

				# Kosongkan semua grup objek
				tree_group.empty()
				coin_group.empty()
				fuel_group.empty()
				obstacle_group.empty()

		# Deteksi tabrakan dengan koin
		if pygame.sprite.spritecollide(p, coin_group, True):
			coins += 1
			coin_fx.play()

		# Deteksi tabrakan dengan bahan bakar
		if pygame.sprite.spritecollide(p, fuel_group, True):
			cfuel += 25
			fuel_fx.play()
			if cfuel >= 100:
				cfuel = 100

	# Menggambar bingkai biru di sekitar layar
	pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT), 3)

	# Mengatur kecepatan frame
	clock.tick(FPS)
	pygame.display.update()

# Keluar dari pygame
pygame.quit()

