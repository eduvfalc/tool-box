cd ../build

if [ -e in_file ]; then
    rm in_file
else
    touch in_file
fi
if [ -e out_file ]; then
    rm out_file
else
    touch out_file
fi

echo "this content should be in both files" >> in_file

./uds-server > out_file &
sleep 0.1
./uds-client < in_file

wait