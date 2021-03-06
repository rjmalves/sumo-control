# Gerador de relógio para a simulação de tráfego com controle em tempo real
#
# Rogerio José Menezes Alves
# Mestrando em Engenharia Elétrica - Universidade Federal do Espírito Santo
# 11 de Março de 2020

# Imports gerais de módulos padrão
import time
import pika  # type: ignore
import sys
# Imports de módulos específicos da aplicação


class ClockGenerator:
    """
    Gerador de relógio para os dispositivos da simulação. É responsável por:
      - Criar a queue de relógio (clock_tick)
      - Contar quantos passos da simulação já foram executados e, a partir
      deste dado e da duração do passo de tempo da simulação, emitir uma
      mensagem para avisar os dispositivos inscritos que se passou um segundo.
    """
    def __init__(self, simulation_time_step: float):
        # Define os parâmetros da conexão (local do broker RabbitMQ)
        self.parameters = pika.ConnectionParameters(host="localhost")
        # Cria uma conexão com o broker bloqueante
        self.connection = pika.BlockingConnection(self.parameters)
        # Cria um canal dentro da conexão
        self.channel = self.connection.channel()
        # Declara a exchange de relógio
        self.channel.exchange_declare(exchange="clock_tick",
                                      exchange_type="fanout")
        # Contador de passos de simulação e do instante de tempo
        # atual na simulação
        self.simulation_time_step = simulation_time_step
        self.num_simulation_steps: int = 0
        self.current_sim_time: float = 0.0

    def clock_tick(self):
        # Aumenta o contador de passos
        self.num_simulation_steps += 1
        # Guarda o valor, em segundos, do passo anterior
        old_sim_time_seconds = int(self.current_sim_time)
        # Atualiza o tempo atual na simulação
        self.current_sim_time += self.simulation_time_step
        # Se o valor do tempo atual, em segundos, é maior que o anterior
        if int(self.current_sim_time) > old_sim_time_seconds:
            self.channel.basic_publish(exchange="clock_tick",
                                       routing_key="",
                                       body=str(self.current_sim_time))


if __name__ == "__main__":
    # Executa testes básicos com passo de 1 segundo. Para conferir é
    # necessário executar algum dispositivo, como o controlador.

    # Valores default de teste
    sim_time_step = 1.0
    sim_step_duration = 1.0
    # Valores opcionais caso o usuário informe via linha de comando
    if len(sys.argv) == 2:
        sim_time_step = float(sys.argv[1])
        sim_step_duration = 1.0
    elif len(sys.argv) >= 3:
        sim_time_step = float(sys.argv[1])
        sim_step_duration = float(sys.argv[2])

    clock_gen = ClockGenerator(sim_time_step)
    try:
        print("Iniciando o teste do ClockGenerator!\n" +
              "Tempo na simulação a cada passo: {}\n".format(sim_time_step) +
              "Tempo para computar um passo: {}".format(sim_step_duration))
        reset_time = time.time()
        while True:
            current_time = time.time()
            if current_time - reset_time > sim_step_duration:
                clock_gen.clock_tick()
                reset_time = current_time
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("Finalizando o teste do ClockGenerator!")
        exit(0)
