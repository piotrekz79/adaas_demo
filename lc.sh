echo "rcvd"
RCV=`sed "/\b\(error\|heartbeat\|EOT\)\b/d" ${1} | wc -l`
echo $RCV
echo "reconnects"
grep error < ${1} | wc -l

diff -u <(echo `cut -d " " -f 4 ${1} | sed "/\b\(error\|heartbeat\)\b/d"`) <(echo `seq ${RCV}`) && echo "seq OK"

#testvar=`ls test2017*` && for i in $testvar; do ./lc.sh ${i}; done


