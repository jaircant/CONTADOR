import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_contador_3bits(dut):
    dut.ena.value = 1       # Habilita el proyecto
    dut.clk.value = 0
    dut.rst_n.value = 1
    dut.ui_in.value = 0     # ui_in[7] = 0: permite contar
    dut.uio_in.value = 0

    async def pulso():
        dut.clk.value = 1
        await Timer(10, unit="ns")
        dut.clk.value = 0
        await Timer(10, unit="ns")

    def comprobar(esperado):
        obtenido = int(dut.uo_out.value)
        assert obtenido == esperado, (
            f"Se esperaba {esperado:03b} y se obtuvo {obtenido:03b}"
        )

    # 1. Activa el reset con el reloj detenido. Debe mostrar 000.
    await Timer(10, unit="ns")
    dut.rst_n.value = 0
    await Timer(10, unit="ns")
    comprobar(0)

    dut.rst_n.value = 1
    await Timer(10, unit="ns")

    # 2. Cuenta de 001 a 111, vuelve a 000 y continúa hasta 011.
    for esperado in [1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3]:
        await pulso()
        comprobar(esperado)

    # 3. Activa PAUSA. Tres pulsos deben dejar la cuenta en 011.
    dut.ui_in.value = 0b10000000
    await Timer(10, unit="ns")
    for _ in range(3):
        await pulso()
        comprobar(3)

    # 4. Quita PAUSA. La cuenta debe avanzar de 011 a 100.
    dut.ui_in.value = 0
    await Timer(10, unit="ns")
    comprobar(3)
    await pulso()
    comprobar(4)

    # 5. Con PAUSA activa, el reset debe borrar la cuenta sin otro pulso.
    dut.ui_in.value = 0b10000000
    await Timer(10, unit="ns")
    dut.rst_n.value = 0
    await Timer(10, unit="ns")
    comprobar(0)
