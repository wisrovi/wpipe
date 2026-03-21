from wkafka.controller import Wkafka


# kafka_instance = Wkafka(server="192.168.1.60:9092")
kafka_instance = Wkafka(server="localhost:9092")


with kafka_instance.producer() as producer:
    producer.send(
        topic="mi_tema",
        value={
            "mensaje": "Hola Kafka!",
            #"a": 2,
            "x": 2,
        },
        key="clave1",
        value_type="json",
    )
