#!/usr/bin/env python3

# Imports gerais de módulos padrão
from multiprocessing import Process, Queue

from model.traffic.controller import Controller
from system.optimization.scoot import EnumOptimizationMethods
import time
from typing import Dict
# Imports específicos da aplicação
from system.simulation import Simulation
from system.simulation import console


def apresentacao():
    """
    """
    desc = ("[bold]AVALIAÇÃO DE TÉCNICAS DE " +
            "[bold blue on white]CONTROLE SEMAFÓRICO" +
            "[bold white on black] :vertical_traffic_light: PARA " +
            "[bold white on blue]CONTROLE DE TRÁFEGO"
            + "[bold on black] :car:")
    console.print(desc)
    autor = ("AUTOR: [bold]ROGERIO JOSÉ MENEZES ALVES - " +
             "[bold white on blue]rogerioalves.ee@gmail.com")
    console.print(autor)
    propos = ("MESTRADO EM ENGENHARIA ELÉTRICA - " +
              "[bold]UFES. 2018 - 2020")
    console.print(propos)
    data = ("[underline]Vila Velha - ES - Brasil")
    console.print(data)
    console.rule("")


def inicia_controlador(id: str,
                       cfg: str,
                       q: Queue):
    """
    """
    ctrl = Controller(id)
    ctrl.start(cfg)
    q.get(block=True)




def main():
    console.rule("[bold]SIMULAÇÃO DE CONTROLE DE TRÁFEGO EM TEMPO REAL")
    apresentacao()
    # Importa os arquivos
    sim = Simulation("config/simulations/crossing.json",
                     EnumOptimizationMethods.FixedTime)
    # Inicia os controladores
    controllers: Dict[str, Controller] = {}
    processes: Dict[str, Process] = {}
    for ctrl_id, ctrl_cfg in sim.controller_configs.items():
        processes[ctrl_id] = Process(target=inicia_controlador,
                                     args=(ctrl_id,
                                           ctrl_cfg,
                                           ))
        processes[ctrl_id].start()
        # TODO - FALTA CRIAR AS FILAS E RESOLVER COMO VAI SER
        # DADO O JOIN EM CADA PROCESSO (SERÁ QUE SÓ DE MANDAR
        # MENSAGEM NA FILA FAZ ELE RETORNAR OU TEM QUE FORÇAR
        # O JOIN MESMO ASSIM?)
    # Aguarda um tempo até os controladores serem iniciados
    time.sleep(2)
    try:
        # Inicia a simulação
        sim.start()
        while sim.is_running():
            time.sleep(1.5e-3)
    finally:
        # Termina os controladores
        for _, p in processes.items():
            p.join()
        sim.export_histories()
        console.rule("[bold]FIM DA EXECUÇÃO")
        return 0


if __name__ == "__main__":
    main()
