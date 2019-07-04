#importer_script_path="./home/chgue/projects/flower/backend/result/bin/flower-import" import_path="/home/chgue/projects/ctf/enowars19/flower_db/dumps"
import_path="/home/chgue/projects/ctf/enowars19/flower_db/dumps"

cd $import_path

while true 
do
    rsync -avzh root@[fd00:1337:120::1]:~/pcaps/old $import_path
    ultimo=$(find ./old -type f -printf '%T@ %p\n' | sort | tail -1 | cut -f2- -d" ")
    /home/chgue/projects/flower/backend/result/bin/flower-import $ultimo
    sleep 60
done
