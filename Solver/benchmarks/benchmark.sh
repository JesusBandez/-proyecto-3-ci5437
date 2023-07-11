cd ../

for i in {8..8}
    do
    echo "Ejecutando archivo ${i}.json" >> ./benchmarks/output.txt
    (time python3 main.py benchmarks/${i}.json) >> ./benchmarks/output.txt 2>&1
    echo "Fin de ejecucion de ${i}.json" >> ./benchmarks/output.txt
    echo "" >> ./benchmarks/output.txt
    echo "" >> ./benchmarks/output.txt
    done
