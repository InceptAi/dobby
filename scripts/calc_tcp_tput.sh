if [ "$#" -ne 5 ]; then
  echo "./calc_tput.sh mss rtt_avg rtt_var losspkts totalpkts"
  exit 1
fi

mss=$1
rtt=$2
var=$3
losspkts=$4
totalpkts=$5

echo "RTT_AVG"
bc -l <<< "8 * ($mss * sqrt(3/2)) / ($rtt * sqrt($losspkts/$totalpkts) * 1024 * 1024)"
echo "RTT_AVG RTT_VAR" 
bc -l <<< "8 * ($mss * sqrt(3/2)) / (($rtt + $var) * sqrt($losspkts/$totalpkts) * 1024 * 1024)"
