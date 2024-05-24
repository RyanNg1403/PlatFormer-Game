# Platformer-Game
## Sơ lược về đồ án:  
Đồ án cuối kì môn Lập trình hướng đối tượng (OOP) với đề tài "ỨNG DỤNG PYGAME LÀM GAME PLATFORMER" nhằm mục tiêu áp dụng những kiến thức đã học trong môn IT002.O21 tại trường Đại học Công nghệ Thông tin - Đại học Quốc gia Hồ Chí Minh vào việc xây dựng một trò chơi điện tử hoàn chỉnh. Trò chơi Mario được phát triển bằng thư viện Pygame, một thư viện phổ biến dành cho lập trình game trong Python. Đồ án này không chỉ nhằm giúp sinh viên củng cố và nâng cao kỹ năng lập trình hướng đối tượng mà còn phát triển khả năng tư duy logic và sáng tạo :smiley:.

## Nội dung
1. [Cài đặt](#1-.Cài-đặt)
2. [Cách sử dụng](#2.-Cách-sử-dụng)
3. [Cơ chế hoạt động](#3.-Cơ-chế-hoạt-động)
4. [Tham khảo](#4.-Tham-khảo)


## 1. Cài đặt 

Để có được một bản sao của dự án này và chạy nó trên máy tính của bạn, hãy làm theo các bước đơn giản sau.

### Yêu Cầu

Đảm bảo rằng bạn đã cài đặt Git trên hệ thống của mình. Bạn có thể tải xuống từ [git-scm.com](https://git-scm.com/).

### Các bước để cài đặt đồ án về máy

1. Mở terminal của bạn.
2. Điều hướng đến thư mục nơi bạn muốn nhân bản kho lưu trữ.
3. Sử dụng lệnh sau để nhân bản kho lưu trữ:

```bash
git clone git@github.com:Ryaniac/PlatFormer-Game.git
```
Để trải nghiệm trò chơi, thực hiện các bước sau:

```bash
cd PlatFormer-Game
```
Nếu bạn sử dụng Windows
```bash
py game.py
```
Nếu bạn sụng Linux
```bash
python3 game.py
```
##2. Cách sử dụng

### A. Cấu trúc của đồ án 
cấu trúc thư mục của dự án:

```plaintext
PlatFormer-Game/
├── README.md
├── game.py
├── editor.py
├── tutorial.json
│
│
├── data/
│   ├── images
│   ├── maps
│   ├── sfx
│   └── music.wav
│
│
├── scripts/
│   ├── clouds.py
│   ├── entities.py
│   ├── tilemap.py
│   ├── utils.py
│   └── particles.py
│
└── tests/
    ├── __init__.py
    └── test_main.py
