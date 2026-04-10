try:
    from pydantic import BaseModel  # pip install pydantic
    HAS_PYDANTIC = True
except ImportError:
    class BaseModel:
        def model_dump(self):
            return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    HAS_PYDANTIC = False

from dataclasses import asdict, dataclass, is_dataclass


class Niveles:
    vacio = "Vacío"
    bajo = "Bajo"
    medio = "Medio"
    alto = "Alto"


# case 1: Usando Pydantic
class Extras(BaseModel):
    aire_acondicionado: bool = True
    radio: bool = True
    gps: bool = True
    asientos_calefaccionados: bool = False
    techo_solar: bool = False


class Car(BaseModel):
    marca: str
    modelo: str
    ano: int = 2020
    color: str = "Rojo"
    nivel_gasolina: str = Niveles.medio
    nivel_aceite: str = Niveles.medio
    nivel_neumaticos: str = Niveles.medio
    extras: Extras = Extras()


# case 2: Usando dataclass
@dataclass
class Extras2:
    aire_acondicionado: bool = True
    radio: bool = True
    gps: bool = True
    asientos_calefaccionados: bool = False
    techo_solar: bool = False


@dataclass
class Car2:
    marca: str
    modelo: str
    ano: int = 2020
    color: str = "Rojo"
    nivel_gasolina: str = Niveles.medio
    nivel_aceite: str = Niveles.medio
    nivel_neumaticos: str = Niveles.medio
    extras: Extras2 = None

    def __post_init__(self):
        if self.extras is None:
            self.extras = Extras2()


# case 3: Usando clase tradicional
class Extras3:
    def __init__(self):
        self.aire_acondicionado: bool = True
        self.radio: bool = True
        self.gps: bool = True
        self.asientos_calefaccionados: bool = False
        self.techo_solar: bool = False


class Car3:
    def __init__(
        self,
        marca: str,
        modelo: str,
        ano: int = 2020,
        color: str = "Rojo",
        nivel_gasolina: str = Niveles.medio,
        nivel_aceite: str = Niveles.medio,
        nivel_neumaticos: str = Niveles.medio,
        extras: Extras3 = None,
    ):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.color = color
        self.nivel_gasolina = nivel_gasolina
        self.nivel_aceite = nivel_aceite
        self.nivel_neumaticos = nivel_neumaticos
        self.extras = extras if extras is not None else Extras3()


# case 4: Usando dict tradicional
def tradicional_to_dict():
    return {
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 2021,
        "color": "Azul",
        "nivel_gasolina": Niveles.medio,
        "nivel_aceite": Niveles.medio,
        "nivel_neumaticos": Niveles.medio,
        "extras": {
            "aire_acondicionado": True,
            "radio": True,
            "gps": True,
            "asientos_calefaccionados": False,
            "techo_solar": False,
        },
    }


if __name__ == "__main__":
    from utils.dict2obj import to_dict

    car = Car(marca="Toyota", modelo="Corolla")
    car2 = Car2(marca="Toyota", modelo="Corolla")
    car3 = Car3(marca="Toyota", modelo="Corolla")
    car4 = tradicional_to_dict()

    cars = [car, car2, car3, car4]

    for i, c in enumerate(cars, 1):
        # print(f"\n--- Procesando Carro {i} ---")

        # Fallback para objetos genéricos que tengan __dict__
        try:
            car_dict = to_dict(c)
        except TypeError:
            raise ValueError(
                f"El objeto de tipo {type(c).__name__} no es compatible para conversión a dict"
            )

        # print(f"Tipo original: {type(c).__name__}")
        print(f"Resultado: {car_dict}")
        # print(f"Tipo resultado: {type(car_dict).__name__}")
