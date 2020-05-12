# Classe de detector para simulação de tráfego com controle em tempo real
#
# Rogerio José Menezes Alves
# Mestrando em Engenharia Elétrica - Universidade Federal do Espírito Santo
# 18 de Março de 2020

# Imports gerais de módulos padrão
from typing import List, Tuple
# Imports de módulos específicos da aplicação


class Detection:
    """
    Classe que representa as detecções de um detector. Contém um instante de
    tempo no qual ocorreu a modificação e o estado para o qual o detector foi.
    """
    def __init__(self, time_instant: float, state: bool):
        self.time_instant = time_instant
        self.state = state

    def __str__(self):
        detection_str = ""
        for key, val in self.__dict__.items():
            detection_str += "        {}: {}\n".format(key, val)
        return detection_str


class Detector:
    """
    Classe que representa o objeto detector indutivo localizado em uma Lane
    do SUMO.
    """
    def __init__(self,
                 detector_id: str,
                 edge_id: str,
                 lane_id: str,
                 position: float):
        self.id = detector_id
        self.edge_id = edge_id
        self.lane_id = lane_id
        self.position = position
        self.detection_history: List[Detection] = []
        self.state = False
        # Adiciona, por default, um histórico inicial
        self.update_detection_history(0.0, False)

    def __str__(self):
        detector_str = ""
        for key, val in self.__dict__.items():
            if key == "detection_history":
                pass
            else:
                detector_str += "{}: {}\n".format(key, val)
        return detector_str

    def update_detection_history(self, time_instant: float, state: bool):
        """
        Adiciona uma detecção ao detector para formar o histórico.
        """
        self.state = state
        self.detection_history.append(Detection(time_instant, state))

    def export_detection_history(self) -> List[Tuple[float, int]]:
        """
        Exporta o histórico de detecção na forma de uma lista onde são
        mostrados os instantes de mudança de estado dos detectores. Cada
        objeto Detection é convertido em dois pontos: um no estado antigo e
        outro no estado atual, 1 centésimo de segundo depois.
        """
        detector_history: List[Tuple[float, int]] = []
        for history in self.detection_history:
            previous = (history.time_instant, int(not history.state))
            current = (history.time_instant + 0.01, int(history.state))
            detector_history += [previous, current]

        return detector_history


if __name__ == "__main__":
    # Cria um objeto detector para teste e printa
    test_det = Detector("MY_ID", "EDGE", "LANE", 100.0)
    print(test_det)
    test_det.update_detection_history(1.0, True)
    print(test_det)