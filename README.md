# Creality-K2-Custom-Macros
Creality K2 macros for better ORCA Sliser compatibility and other improvements\
Based on ideas: https://github.com/jamincollins great thanks!\
GPL-3.0 license\
Author: Mikhail Ivanov masluf@gmail.com  

> [!WARNING]
> Using custom macros could damage your printer and void your warranty, or cause unexpected behavior.

For use you need install Klipper Virtual Pins https://github.com/pedrolamas/klipper-virtual-pins \
Just copy virtual_pins.py to you printer /usr/share/klipper/klippy/extras/ via SSH\
Than copy main.cfg to you pinter config directory Fluidd web interface and include to printer.cfg after all includes.\
you can use tool.cfg or not. If you want, just copy tool.cfg and custom_vars.cfg to printer config directory via Fluidd web interface and include to printer.cfg after main.cfg\
\
Example:
![изображение](https://github.com/user-attachments/assets/d2adb77c-587f-4844-a844-545f4fd42174)
![изображение](https://github.com/user-attachments/assets/9f2b6c62-a756-42e8-a3e8-70fc86d4d4e8)
![изображение](https://github.com/user-attachments/assets/aa353b06-e271-4759-b018-69a6830509f7)

overrides.cfg need to be included in printer.cfg  after all blocs before SAVE_CONFIG section

![изображение](https://github.com/user-attachments/assets/331bd7bf-287d-4d6c-9f20-7ea7645a218d)




