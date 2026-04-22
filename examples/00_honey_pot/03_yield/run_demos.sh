#!/bin/bash

# Configuración: Tiempo de espera entre demos (segundos)
WAIT_TIME=0.1

# Colores para la consola
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}   🚀 INICIANDO TOUR DE APRENDIZAJE: WPipe ADAS     ${NC}"
echo -e "${BLUE}====================================================${NC}"

# Buscamos todos los archivos demo_level*.py y los ordenamos numéricamente
demos=$(ls demo_level*.py | sort -V)

for demo in $demos; do
    echo -e "\n${GREEN}▶️  Ejecutando: $demo ...${NC}"
    echo "----------------------------------------------------"
    
    # Ejecutamos el demo
    python3 "$demo"
    
    # Verificamos si la ejecución fue exitosa
    if [ $? -eq 0 ]; then
        echo "----------------------------------------------------"
        echo -e "${GREEN}✅ $demo finalizado correctamente.${NC}"
    else
        echo "----------------------------------------------------"
        echo -e "\033[0;31m❌ Error en $demo. Deteniendo el tour.\033[0m"
        exit 1
    fi

    echo -e "${BLUE}⏳ Esperando $WAIT_TIME segundos para el siguiente nivel...${NC}"
    sleep $WAIT_TIME
done

echo -e "\n${BLUE}====================================================${NC}"
echo -e "${BLUE}   🏁 TOUR COMPLETADO CON ÉXITO (130 NIVELES)       ${NC}"
echo -e "${BLUE}====================================================${NC}"
