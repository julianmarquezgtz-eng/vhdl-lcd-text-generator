"""
LCD Text Display FSM Generator
Author: Julian Marquez Gutierrez
Email: julianmarquezgtz@gmail.com
GitHub: https://github.com/julianmarquezgtz-eng
Date: 2025-07-08
"""

def generar_bloques_vhdl(texto, estado_inicial=21):
    bloques = []
    estado = estado_inicial

    simbolos_especiales = {
        '\n': 192,     # salto de línea (set DDRAM address)
        ' ': 32,       # espacio
        '.': 46,
        ',': 44,
        '!': 33,
        '?': 63,
        ':': 58,
        ';': 59
       
    }

    for caracter in texto:
        if caracter in simbolos_especiales:
            ascii_code = simbolos_especiales[caracter]
        else:
            ascii_code = ord(caracter)

        comentario = f"-- '{caracter}'"
        bloques.append(f"      when {estado} => RS<='1'; RW<='0'; EN<='0'; DATA<={ascii_code}; edo_sig<={estado+1}; {comentario}")
        bloques.append(f"      when {estado+1} => RS<='1'; RW<='0'; EN<='1'; DATA<={ascii_code}; edo_sig<={estado+2};")
        bloques.append(f"      when {estado+2} => RS<='1'; RW<='0'; EN<='0'; DATA<={ascii_code}; edo_sig<={estado+3};")
        estado += 3

    # Estado final para reiniciar
    bloques.append(f"      when {estado} => RS<='0'; RW<='0'; EN<='0'; DATA<=0; edo_sig <= 0; -- FIN")

    return "\n".join(bloques)


def generar_codigo_vhdl(texto):
    texto_procesado = texto.encode('utf-8').decode('unicode_escape')  # permite \n

    parte_inicial = """
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

entity LCD_A is
  port(CLK50, SW:in std_logic;
       RS, RW, EN, LCD_ON, LCD_BLON: out std_logic;
       DATA: out integer range 0 to 255);
end entity;

architecture arq of LCD_A is
  signal c: integer range 0 to 50000000;
  signal clk: std_logic;
  signal edo_act, edo_sig: integer range 0 to 255;
begin

  LCD_ON <= '1';
  LCD_BLON <= '0';

  process(CLK50, SW)
  begin
    if (SW = '1') then
      clk <= '0'; c <= 0;
    elsif rising_edge(CLK50) then
      c <= c + 1;
      if (c = 7000) then
        c <= 0; clk <= not clk;
      end if;
    end if;
  end process;

  process(edo_act)
  begin
    case edo_act is
      -- Inicialización del LCD
      when 0 => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 56; edo_sig <= 1;  -- Function set
      when 1 => RS <= '0'; RW <= '0'; EN <= '1'; DATA <= 56; edo_sig <= 2;
      when 2 => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 56; edo_sig <= 3;
      when 3 => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 56; edo_sig <= 4;
      when 4 => RS <= '0'; RW <= '0'; EN <= '1'; DATA <= 56; edo_sig <= 5;
      when 5 => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 56; edo_sig <= 6;
      when 6 => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 56; edo_sig <= 7;
      when 7 => RS <= '0'; RW <= '0'; EN <= '1'; DATA <= 56; edo_sig <= 8;
      when 8 => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 56; edo_sig <= 9;
      when 9 => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 56; edo_sig <= 10;
      when 10 => RS <= '0'; RW <= '0'; EN <= '1'; DATA <= 56; edo_sig <= 11;
      when 11 => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 56; edo_sig <= 12;

      -- Display ON
      when 12 => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 12; edo_sig <= 13;
      when 13 => RS <= '0'; RW <= '0'; EN <= '1'; DATA <= 12; edo_sig <= 14;
      when 14 => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 12; edo_sig <= 15;

      -- Clear Display
      when 15 => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 1; edo_sig <= 16;
      when 16 => RS <= '0'; RW <= '0'; EN <= '1'; DATA <= 1; edo_sig <= 17;
      when 17 => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 1; edo_sig <= 18;

      -- Entry Mode Set
      when 18 => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 6; edo_sig <= 19;
      when 19 => RS <= '0'; RW <= '0'; EN <= '1'; DATA <= 6; edo_sig <= 20;
      when 20 => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 6; edo_sig <= 21;

      -- Texto generado dinámicamente
"""

    texto_vhdl = generar_bloques_vhdl(texto_procesado, estado_inicial=21)

    parte_final = """
      when others => RS <= '0'; RW <= '0'; EN <= '0'; DATA <= 0; edo_sig <= 0;
    end case;
  end process;

  process(clk)
  begin
    if rising_edge(clk) then
      edo_act <= edo_sig;
    end if;
  end process;

end architecture;
"""

    return parte_inicial + texto_vhdl + parte_final


def main():
    print("=== Generador de código VHDL para LCD ===")
    texto = input("Introduce el texto a mostrar (usa \\n para saltos de línea):\n")

    vhdl_completo = generar_codigo_vhdl(texto)

    nombre_archivo = "lcd_autogenerado.vhd"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(vhdl_completo)

    print(f"\n✅ Archivo '{nombre_archivo}' generado con éxito.")


if __name__ == "__main__":
    main()
