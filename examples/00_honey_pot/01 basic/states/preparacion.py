from wpipe.decorators import step, AutoRegister
from wpipe.parallel import ParallelExecutor, ExecutionMode


@step(name="A_abrir_coche", version="v1.1", tags=["preparacion"])
def A_abrir_coche(context):
    print("    [A] Abriendo el coche...")
    return {}


@step(name="B_inflar_neumaticos", version="v1.1", depends_on=["A_abrir_coche"], parallel=True)
def B_inflar_neumaticos(context):
    print("    [B] Inflando neumáticos (en paralelo)...")
    return {"neumaticos": "OK"}


@step(name="C_limpiar_parabrisas", version="v1.1", depends_on=["A_abrir_coche"], parallel=True)
def C_limpiar_parabrisas(context):
    print("    [C] Limpiando parabrisas (en paralelo)...")
    return {"parabrisas": "Limpio"}


@step(name="D_arrancar_motor", version="v1.1", depends_on=["B_inflar_neumaticos", "C_limpiar_parabrisas"])
def D_arrancar_motor(context):
    print("    [D] Arrancando motor... ¡Todo listo!")
    return {"motor": "ON"}


@step(name="fase_preparacion", version="v1.1")
def fase_preparacion(data):
    """
    Encapsula una ejecución en paralelo dentro de un paso del pipeline.
    Utiliza AutoRegister para cargar automáticamente los pasos decorados.
    """
    print("\n--- Iniciando Fase de Preparación Paralela (DAG) ---")
    
    # El ParallelExecutor es capaz de orquestar basándose en las dependencias de los @step
    executor = ParallelExecutor(max_workers=4)
    
    # En lugar de añadir manualmente, podemos usar el registro de @step
    # Para este ejemplo, añadimos los que tienen el tag 'preparacion' o dependencias directas
    executor.add_step("A_abrir_coche", A_abrir_coche)
    executor.add_step("B_inflar_neumaticos", B_inflar_neumaticos, mode=ExecutionMode.IO_BOUND)
    executor.add_step("C_limpiar_parabrisas", C_limpiar_parabrisas, mode=ExecutionMode.IO_BOUND)
    executor.add_step("D_arrancar_motor", D_arrancar_motor)
    
    # El ejecutor resuelve el grafo y corre B y C simultáneamente
    result = executor.execute(data)
    print("--- Fase de Preparación Completada ---\n")
    return result
